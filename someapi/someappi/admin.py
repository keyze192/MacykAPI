from django.contrib import admin
from .models import MuscleGroup, Exercise, Workout, Set


@admin.register(MuscleGroup)
class MuscleGroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'body_part')


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'muscle_group')


@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    list_display = ('id', 'date_time', 'user', 'duration_min')
    list_filter = ('user',)


@admin.register(Set)
class SetAdmin(admin.ModelAdmin):
    list_display = ('id', 'workout', 'set_number', 'exercises')