from datetime import timedelta

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.utils.dateparse import parse_date
from django.contrib.auth.models import User

from .models import MuscleGroup, Exercise, Workout, Set




def user_list(request):
    data = [{'id': u.id, 'username': u.username} for u in User.objects.all()]
    return JsonResponse(data, safe=False)


def user_detail(request, pk):
    u = get_object_or_404(User, pk=pk)
    return JsonResponse({'id': u.id, 'username': u.username})




def muscle_group_list(request):
    data = [{'id': g.id, 'name': g.name, 'body_part': g.body_part}
            for g in MuscleGroup.objects.all()]
    return JsonResponse(data, safe=False)


def muscle_group_detail(request, pk):
    g = get_object_or_404(MuscleGroup, pk=pk)
    return JsonResponse({'id': g.id, 'name': g.name, 'body_part': g.body_part})



def exercise_list(request):
    qs = Exercise.objects.all()
    mg_id = request.GET.get('muscle_group_id')
    if mg_id:
        qs = qs.filter(muscle_group_id=mg_id)
    data = [{'id': e.id, 'name': e.name, 'muscle_group_id': e.muscle_group_id}
            for e in qs]
    return JsonResponse(data, safe=False)


def exercise_detail(request, pk):
    e = get_object_or_404(Exercise, pk=pk)
    return JsonResponse({'id': e.id, 'name': e.name, 'muscle_group_id': e.muscle_group_id})



def workout_list(request):
    qs = Workout.objects.all().order_by('-date_time')
    user_id = request.GET.get('user_id')
    if user_id:
        qs = qs.filter(user_id=user_id)
    data = [{'id': w.id, 'date_time': w.date_time.isoformat(),
             'started_ad': w.started_ad, 'duration_min': w.duration_min,
             'comment': w.comment, 'user_id': w.user_id} for w in qs]
    return JsonResponse(data, safe=False)


def workout_detail(request, pk):
    w = get_object_or_404(Workout, pk=pk)
    sets = Set.objects.filter(workout=w).order_by('set_number')
    sets_data = [{'id': s.id, 'set_number': s.set_number,
                  'exercise_id': s.exercises_id,
                  'exercise_name': s.exercises.name} for s in sets]
    return JsonResponse({
        'id': w.id, 'date_time': w.date_time.isoformat(),
        'started_ad': w.started_ad, 'duration_min': w.duration_min,
        'comment': w.comment, 'user_id': w.user_id, 'sets': sets_data,
    })


def workout_filter(request):
    from_str = request.GET.get('from')
    to_str = request.GET.get('to')

    if not from_str or not to_str:
        return JsonResponse({'error': 'нужны from и to'}, status=400)

    from_date = parse_date(from_str)
    to_date = parse_date(to_str)
    if not from_date or not to_date:
        return JsonResponse({'error': 'формат YYYY-MM-DD'}, status=400)

    qs = Workout.objects.filter(
        date_time__date__gte=from_date,
        date_time__date__lte=to_date,
    ).order_by('date_time')

    data = [{'id': w.id, 'date_time': w.date_time.isoformat(),
             'started_ad': w.started_ad, 'duration_min': w.duration_min,
             'comment': w.comment, 'user_id': w.user_id} for w in qs]
    return JsonResponse(data, safe=False)



def set_list(request):
    qs = Set.objects.all().order_by('workout_id', 'set_number')
    workout_id = request.GET.get('workout_id')
    if workout_id:
        qs = qs.filter(workout_id=workout_id)
    data = [{'id': s.id, 'workout_id': s.workout_id,
             'set_number': s.set_number, 'exercises_id': s.exercises_id}
            for s in qs]
    return JsonResponse(data, safe=False)


def set_detail(request, pk):
    s = get_object_or_404(Set, pk=pk)
    return JsonResponse({'id': s.id, 'workout_id': s.workout_id,
                         'set_number': s.set_number, 'exercises_id': s.exercises_id})



def stats_regularity_muscle(request, muscle_id):
    days = int(request.GET.get('days', 30))
    mg = get_object_or_404(MuscleGroup, pk=muscle_id)

    start = timezone.now() - timedelta(days=days)
    qs = Workout.objects.filter(
        date_time__gte=start,
        set__exercises__muscle_group_id=muscle_id,
    ).distinct()

    days_count = qs.dates('date_time', 'day').count()
    weeks = days / 7
    avg = round(days_count / weeks, 2) if weeks else 0

    return JsonResponse({
        'muscle_group_id': mg.id,
        'muscle_group_name': mg.name,
        'period_days': days,
        'total_workout_days': days_count,
        'average_per_week': avg,
    })


def stats_regularity_all(request):
    days = int(request.GET.get('days', 7))
    start = timezone.now() - timedelta(days=days)
    weeks = days / 7

    result = []
    for mg in MuscleGroup.objects.all():
        qs = Workout.objects.filter(
            date_time__gte=start,
            set__exercises__muscle_group_id=mg.id,
        ).distinct()
        days_count = qs.dates('date_time', 'day').count()
        avg = round(days_count / weeks, 2) if weeks else 0
        result.append({
            'muscle_group_id': mg.id,
            'muscle_group_name': mg.name,
            'total_workout_days': days_count,
            'average_per_week': avg,
        })

    return JsonResponse({'period_days': days, 'stats': result})