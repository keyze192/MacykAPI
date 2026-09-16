from django.urls import path
from . import views

urlpatterns = [
    path('user', views.user_list),
    path('user/<int:pk>', views.user_detail),

    path('muscle_groups', views.muscle_group_list),
    path('muscle_groups/<int:pk>', views.muscle_group_detail),

    path('exercises', views.exercise_list),
    path('exercises/<int:pk>', views.exercise_detail),

    path('workouts', views.workout_list),
    path('workouts/filter', views.workout_filter),
    path('workouts/<int:pk>', views.workout_detail),

    path('sets', views.set_list),
    path('sets/<int:pk>', views.set_detail),

    path('stats/regularity/all', views.stats_regularity_all),
    path('stats/regularity/<int:muscle_id>', views.stats_regularity_muscle),
]