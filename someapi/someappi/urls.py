from django.urls import path
from . import views

urlpatterns = [
    path('user', views.UserList.as_view()),
    path('user/<int:pk>', views.UserDetail.as_view()),

    path('muscle_groups', views.MuscleGroupList.as_view()),
    path('muscle_groups/<int:pk>', views.MuscleGroupDetail.as_view()),

    path('exercises', views.ExerciseList.as_view()),
    path('exercises/<int:pk>', views.ExerciseDetail.as_view()),

    path('workouts', views.WorkoutList.as_view()),
    path('workouts/filter', views.WorkoutFilter.as_view()),
    path('workouts/<int:pk>', views.WorkoutDetail.as_view()),

    path('sets', views.SetList.as_view()),
    path('sets/<int:pk>', views.SetDetail.as_view()),

    path('stats/regularity/all', views.StatsRegularityAll.as_view()),
    path('stats/regularity/<int:muscle_id>', views.StatsRegularityMuscle.as_view()),
]