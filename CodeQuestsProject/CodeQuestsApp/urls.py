from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.index, name="index"),
    path('registration', views.registration, name="registration"),
    path('login', views.login, name="login"),
    path('logout', views.logout, name="logout"),
    path('delete_acc', views.delete_acc, name="delete_acc"),
    path('view_courses', views.view_courses, name="view_courses"),
    path('attend_course/<int:course_id>', views.attend_course, name="attend_course"),
    path('search_tasks', views.search_tasks, name="search_tasks"),
    path('choose_task', views.choose_task, name="choose_task"),
    path('solve_task/<int:task_id>/<int:match_id>', views.solve_task, name="solve_task"),
    path('join_queue', views.join_queue, name="join_queue"),
    path('view_profile', views.view_profile, name="view_profile"),
    path('check_match_status', views.check_match_status, name='check_match_status'),
    path('match_history', views.match_history, name="match_history"),
    path('match_result/<int:match_id>', views.match_result, name="match_result"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL,
                                                                           document_root=settings.STATIC_ROOT)
