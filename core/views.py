from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from core.models import ProblemType, ProblemInstance, Attempt, ShareResult
from exercises.arithmetic import ArithmeticProblem
from exercises.algebraic import AlgebraicIdentitiesProblem
from exercises.equations import EquationsProblem
from exercises.calculus import DerivativesProblem, IntegralsProblem
from django.http import HttpResponse

# Реєстр генераторів задач
# Додавай нові генератори сюди
PROBLEM_REGISTRY = {
    'arithmetic': ArithmeticProblem(),
    'algebraic': AlgebraicIdentitiesProblem(),
    'equations': EquationsProblem(),  # Linear only
    'derivatives': DerivativesProblem(),
    'integrals': IntegralsProblem(),
}


# =============================
# Home
# =============================
def home(request):
    """
    Домашня сторінка з вибором типу задач
    """
    # Show only active problem types present in the registry
    active_slugs = set(PROBLEM_REGISTRY.keys())
    types = ProblemType.objects.filter(slug__in=active_slugs)
    return render(request, 'core/home.html', {'types': types})


# =============================
# Start Session
# =============================
@require_http_methods(["GET"])
def start_session(request, slug):
    """
    Створює нову сесію з 12 задач для обраного типу (slug).
    """
    difficulty = int(request.GET.get('difficulty', 1))

    # Вибрати генератор
    gen = PROBLEM_REGISTRY.get(slug)
    if not gen:
        return redirect('home')

    # Генеруємо 12 задач
    pt = get_object_or_404(ProblemType, slug=slug)
    problem_instances = []
    
    ensure_division = True if slug in ['arithmetic'] else False
    for i in range(12):
        if ensure_division and i == 0:
            # Guarantee at least one division with whole result
            if hasattr(gen, 'generate_division'):
                data = gen.generate_division(difficulty)
            else:
                data = gen.generate(difficulty)
        else:
            data = gen.generate(difficulty)
        pi = ProblemInstance.objects.create(
            problem_type=pt,
            difficulty=difficulty,
            params=data['params'],
            question_text=data['question'],
            canonical_answer=data['canonical_answer'],
            multiple_choice_options=data.get('multiple_choice', None)
        )
        problem_instances.append(pi)

    # Зберегти інформацію про сесію
    request.session['session_problems'] = [pi.id for pi in problem_instances]
    request.session['current_problem_index'] = 0
    request.session['session_start_time'] = timezone.now().timestamp()
    request.session['session_type'] = slug
    request.session['session_difficulty'] = difficulty

    # Перенаправити на перше питання
    return redirect('show_question', pk=problem_instances[0].id)


# =============================
# Show Question
# =============================
def show_question(request, pk):
    """
    Відображає питання користувачу
    """
    pi = get_object_or_404(ProblemInstance, pk=pk)
    return render(request, 'core/question.html', {'problem': pi})


# =============================
# Submit Answer
# =============================
@require_http_methods(["POST"])
@csrf_exempt  # можна прибрати, якщо не хочеш спрощення CSRF
def submit_answer(request, pk):
    """
    Приймає відповідь користувача, перевіряє правильність
    і створює Attempt (спробу).
    """
    pi = get_object_or_404(ProblemInstance, pk=pk)
    user_input = request.POST.get('answer', '').strip()

    # Обчислити час виконання для цього питання
    start_time = request.session.get('start_time')
    time_taken_ms = 0
    if start_time:
        time_taken_ms = int((timezone.now().timestamp() - float(start_time)) * 1000)

    # Перевірити відповідь через генератор
    gen = PROBLEM_REGISTRY.get(pi.problem_type.slug)
    is_correct, feedback = gen.check(user_input, pi.canonical_answer, pi.params)

    # Хто користувач: автентифікований чи гість?
    user = request.user if request.user.is_authenticated else None
    if not request.session.session_key:
        request.session.create()
    session_id = None if user else request.session.session_key

    # Створити Attempt
    attempt = Attempt.objects.create(
        user=user,
        session_id=session_id,
        problem=pi,
        user_answer=user_input,
        is_correct=is_correct,
        time_taken_ms=time_taken_ms,
    )

    # Зберегти останній attempt у сесію
    request.session['last_attempt_id'] = attempt.id

    # Перевірити, чи це останнє питання в сесії
    session_problems = request.session.get('session_problems', [])
    current_index = request.session.get('current_problem_index', 0)
    
    if current_index + 1 < len(session_problems):
        # Є ще питання, перейти до наступного
        request.session['current_problem_index'] = current_index + 1
        next_problem_id = session_problems[current_index + 1]
        request.session['start_time'] = timezone.now().timestamp()  # Reset timer for next question
        return redirect('show_question', pk=next_problem_id)
    else:
        # Сесія завершена, показати результати
        return redirect('result', pk=attempt.id)


# =============================
# Result View
# =============================
def result_view(request, pk):
    """
    Показує результат спроби (Attempt).
    """
    attempt = get_object_or_404(Attempt, pk=pk)
    # Collect all attempts in this session for this user/guest
    # Determine the latest session for this user (or guest session id)
    if attempt.user:
        last_session = Attempt.objects.filter(user=attempt.user).order_by('-timestamp').values_list('session_id', flat=True).first()
    else:
        last_session = Attempt.objects.filter(session_id=attempt.session_id).order_by('-timestamp').values_list('session_id', flat=True).first()

    attempts_list = Attempt.objects.filter(
        session_id=last_session,
        user=attempt.user,
    ).order_by('timestamp')
    total_ms = sum(a.time_taken_ms for a in attempts_list)
    return render(request, 'core/result.html', {
        'attempt': attempt,
        'attempts_list': attempts_list,
        'total_time_ms': total_ms,
    })


# =============================
# Share Attempt
# =============================
def share_attempt(request, attempt_id):
    """
    Створює унікальне посилання для поширення результату.
    """
    attempt = get_object_or_404(Attempt, pk=attempt_id)
    sr = ShareResult.objects.create(attempt=attempt)
    return redirect('share_public', uuid=sr.uuid)


# =============================
# Share Public
# =============================
def share_public(request, uuid):
    """
    Відображає результат за унікальним посиланням (для шарингу).
    """
    sr = get_object_or_404(ShareResult, uuid=uuid)
    # Use the latest session for that user
    if sr.attempt.user:
        last_session = Attempt.objects.filter(user=sr.attempt.user).order_by('-timestamp').values_list('session_id', flat=True).first()
    else:
        last_session = sr.attempt.session_id
    attempts_list = Attempt.objects.filter(
        session_id=last_session,
        user=sr.attempt.user,
    ).order_by('timestamp')
    total_ms = sum(a.time_taken_ms for a in attempts_list)
    return render(request, 'core/share_result.html', {
        'share': sr,
        'attempts_list': attempts_list,
        'total_time_ms': total_ms,
    })
# =============================
# About page
# =============================
def about(request):
    """
    Інформаційна сторінка про проект Trainmath.
    """
    return render(request, "core/about.html")


def question_list(request):
    return HttpResponse("Тут буде список питань.")