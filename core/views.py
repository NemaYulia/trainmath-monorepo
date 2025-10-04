from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from core.models import ProblemType, ProblemInstance, Attempt, ShareResult
from exercises.arithmetic import ArithmeticProblem
from django.http import HttpResponse

# Реєстр генераторів задач
# Додавай нові генератори сюди
PROBLEM_REGISTRY = {
    'arithmetic': ArithmeticProblem(),
}


# =============================
# Home
# =============================
def home(request):
    """
    Домашня сторінка з вибором типу задач
    """
    types = ProblemType.objects.all()
    return render(request, 'core/home.html', {'types': types})


# =============================
# Start Session
# =============================
@require_http_methods(["GET"])
def start_session(request, slug):
    """
    Створює нову сесію задачі для обраного типу (slug).
    """
    difficulty = int(request.GET.get('difficulty', 1))

    # Вибрати генератор
    gen = PROBLEM_REGISTRY.get(slug)
    if not gen:
        return redirect('home')

    # Генеруємо дані задачі
    data = gen.generate(difficulty)

    # Зберегти в базу ProblemInstance
    pt = get_object_or_404(ProblemType, slug=slug)
    pi = ProblemInstance.objects.create(
        problem_type=pt,
        difficulty=difficulty,
        params=data['params'],
        question_text=data['question'],
        canonical_answer=data['canonical_answer']
    )

    # Зберегти час у сесії
    request.session['current_problem_id'] = pi.id
    request.session['start_time'] = timezone.now().timestamp()

    return redirect('show_question', pk=pi.id)


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

    # Обчислити час виконання
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

    return redirect('result', pk=attempt.id)


# =============================
# Result View
# =============================
def result_view(request, pk):
    """
    Показує результат спроби (Attempt).
    """
    attempt = get_object_or_404(Attempt, pk=pk)
    return render(request, 'core/result.html', {'attempt': attempt})


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
    return render(request, 'core/share_result.html', {'share': sr})
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

def about(request):
    return HttpResponse("Тут буде інформація про сайт.")