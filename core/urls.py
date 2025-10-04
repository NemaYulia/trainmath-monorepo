# core/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("start/<slug:slug>/", views.start_session, name="start_session"),
    path("question/<int:pk>/", views.show_question, name="show_question"),
    path("submit/<int:pk>/", views.submit_answer, name="submit_answer"),
    path("result/<int:pk>/", views.result_view, name="result"),

    # шарінг результатів
    path("share/<int:attempt_id>/", views.share_attempt, name="share_attempt"),
    path("s/<uuid:uuid>/", views.share_public, name="share_public"),

    # інфо-сторінка
    path("about/", views.about, name="about"),
]
