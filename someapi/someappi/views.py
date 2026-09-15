import json
from datetime import timedelta

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.utils.dateparse import parse_date

from .models import User, MuscleGroup, Exercise, Workout, Set


def parse_body(request):
    try:
        return json.loads(request.body or '{}')
    except json.JSONDecodeError:
        return None



@csrf_exempt
def user_list(request):
    if request.method == 'GET':
        users = User.objects.all()
        data = [{'id': u.id, 'name': u.name} for u in users]
        return JsonResponse(data, safe=False)

    if request.method == 'POST':
        body = parse_body(request)
        if body is None or 'name' not in body:
            return JsonResponse({'error': 'нужно поле name'}, status=400)
        user = User.objects.create(name=body['name'])
        return JsonResponse({'id': user.id, 'name': user.name}, status=201)

    return JsonResponse({'error': 'метод не поддерживается'}, status=405)


@csrf_exempt
def user_detail(request, pk):
    user = get_object_or_404(User, pk=pk)

    if request.method == 'GET':
        return JsonResponse({'id': user.id, 'name': user.name})

    if request.method == 'PUT':
        body = parse_body(request)
        if body is None or 'name' not in body:
            return JsonResponse({'error': 'нужно поле name'}, status=400)
        user.name = body['name']
        user.save()
        return JsonResponse({'id': user.id, 'name': user.name})

    if request.method == 'DELETE':
        user.delete()
        return JsonResponse({'status': 'deleted'})

    return JsonResponse({'error': 'метод не поддерживается'}, status=405)



@csrf_exempt
def muscle_group_list(request):
    if request.method == 'GET':
        groups = MuscleGroup.objects.all()
        data = [{'id': g.id, 'name': g.name, 'body_part': g.body_part} for g in groups]
        return JsonResponse(data, safe=False)

    if request.method == 'POST':
        body = parse_body(request)
        if body is None or 'name' not in body or 'body_part' not in body:
            return JsonResponse({'error': 'нужны name и body_part'}, status=400)
        group = MuscleGroup.objects.create(name=body['name'], body_part=body['body_part'])
        return JsonResponse({'id': group.id, 'name': group.name, 'body_part': group.body_part}, status=201)

    return JsonResponse({'error': 'метод не поддерживается'}, status=405)


@csrf_exempt
def muscle_group_detail(request, pk):
    group = get_object_or_404(MuscleGroup, pk=pk)

    if request.method == 'GET':
        return JsonResponse({'id': group.id, 'name': group.name, 'body_part': group.body_part})

    if request.method == 'PUT':
        body = parse_body(request)
        if body is None:
            return JsonResponse({'error': 'некорректный JSON'}, status=400)
        if 'name' in body:
            group.name = body['name']
        if 'body_part' in body:
            group.body_part = body['body_part']
        group.save()
        return JsonResponse({'id': group.id, 'name': group.name, 'body_part': group.body_part})

    if request.method == 'DELETE':
        group.delete()
        return JsonResponse({'status': 'deleted'})

    return JsonResponse({'error': 'метод не поддерживается'}, status=405)



@csrf_exempt
def exercise_list(request):
    if request.method == 'GET':
        muscle_group_id = request.GET.get('muscle_group_id')
        exercises = Exercise.objects.all()
        if muscle_group_id:
            exercises = exercises.filter(muscle_group_id=muscle_group_id)
        data = [{
            'id': e.id,
            'name': e.name,
            'muscle_group_id': e.muscle_group_id,
        } for e in exercises]
        return JsonResponse(data, safe=False)

    if request.method == 'POST':
        body = parse_body(request)
        if body is None or 'name' not in body or 'muscle_group_id' not in body:
            return JsonResponse({'error': 'нужны name и muscle_group_id'}, status=400)
        exercise = Exercise.objects.create(
            name=body['name'],
            muscle_group_id=body['muscle_group_id'],
        )
        return JsonResponse({'id': exercise.id, 'name': exercise.name}, status=201)

    return JsonResponse({'error': 'метод не поддерживается'}, status=405)


@csrf_exempt
def exercise_detail(request, pk):
    exercise = get_object_or_404(Exercise, pk=pk)

    if request.method == 'GET':
        return JsonResponse({
            'id': exercise.id,
            'name': exercise.name,
            'muscle_group_id': exercise.muscle_group_id,
        })

    if request.method == 'PUT':
        body = parse_body(request)
        if body is None:
            return JsonResponse({'error': 'некорректный JSON'}, status=400)
        if 'name' in body:
            exercise.name = body['name']
        if 'muscle_group_id' in body:
            exercise.muscle_group_id = body['muscle_group_id']
        exercise.save()
        return JsonResponse({'id': exercise.id, 'name': exercise.name})

    if request.method == 'DELETE':
        exercise.delete()
        return JsonResponse({'status': 'deleted'})

    return JsonResponse({'error': 'метод не поддерживается'}, status=405)




@csrf_exempt
def workout_list(request):
    if request.method == 'GET':
        user_id = request.GET.get('user_id')
        workouts = Workout.objects.all().order_by('-date_time')
        if user_id:
            workouts = workouts.filter(user_id=user_id)
        data = [{
            'id': w.id,
            'date_time': w.date_time.isoformat(),
            'started_ad': w.started_ad,
            'duration_min': w.duration_min,
            'comment': w.comment,
            'user_id': w.user_id,
        } for w in workouts]
        return JsonResponse(data, safe=False)

    if request.method == 'POST':
        body = parse_body(request)
        if body is None:
            return JsonResponse({'error': 'некорректный JSON'}, status=400)
        for field in ['date_time', 'started_ad', 'duration_min', 'comment', 'user_id']:
            if field not in body:
                return JsonResponse({'error': f'нужно поле {field}'}, status=400)
        workout = Workout.objects.create(
            date_time=body['date_time'],
            started_ad=body['started_ad'],
            duration_min=body['duration_min'],
            comment=body['comment'],
            user_id=body['user_id'],
        )
        return JsonResponse({'id': workout.id}, status=201)

    return JsonResponse({'error': 'метод не поддерживается'}, status=405)


@csrf_exempt
def workout_detail(request, pk):
    workout = get_object_or_404(Workout, pk=pk)

    if request.method == 'GET':
        sets = Set.objects.filter(workout=workout).order_by('set_number')
        sets_data = [{
            'id': s.id,
            'set_number': s.set_number,
            'exercise_id': s.exercises_id,
            'exercise_name': s.exercises.name,
        } for s in sets]
        return JsonResponse({
            'id': workout.id,
            'date_time': workout.date_time.isoformat(),
            'started_ad': workout.started_ad,
            'duration_min': workout.duration_min,
            'comment': workout.comment,
            'user_id': workout.user_id,
            'sets': sets_data,
        })

    if request.method == 'PUT':
        body = parse_body(request)
        if body is None:
            return JsonResponse({'error': 'некорректный JSON'}, status=400)
        if 'date_time' in body:
            workout.date_time = body['date_time']
        if 'started_ad' in body:
            workout.started_ad = body['started_ad']
        if 'duration_min' in body:
            workout.duration_min = body['duration_min']
        if 'comment' in body:
            workout.comment = body['comment']
        if 'user_id' in body:
            workout.user_id = body['user_id']
        workout.save()
        return JsonResponse({'id': workout.id, 'status': 'updated'})

    if request.method == 'DELETE':
        workout.delete()
        return JsonResponse({'status': 'deleted'})

    return JsonResponse({'error': 'метод не поддерживается'}, status=405)


def workout_filter(request):
    from_str = request.GET.get('from')
    to_str = request.GET.get('to')

    if not from_str or not to_str:
        return JsonResponse({'error': 'нужны from и to'}, status=400)

    from_date = parse_date(from_str)
    to_date = parse_date(to_str)
    if not from_date or not to_date:
        return JsonResponse({'error': 'формат YYYY-MM-DD'}, status=400)

    workouts = Workout.objects.filter(
        date_time__date__gte=from_date,
        date_time__date__lte=to_date
    ).order_by('date_time')

    data = [{
        'id': w.id,
        'date_time': w.date_time.isoformat(),
        'started_ad': w.started_ad,
        'duration_min': w.duration_min,
        'comment': w.comment,
        'user_id': w.user_id,
    } for w in workouts]

    return JsonResponse(data, safe=False)



@csrf_exempt
def set_list(request):
    if request.method == 'GET':
        workout_id = request.GET.get('workout_id')
        sets = Set.objects.all().order_by('workout_id', 'set_number')
        if workout_id:
            sets = sets.filter(workout_id=workout_id)
        data = [{
            'id': s.id,
            'workout_id': s.workout_id,
            'set_number': s.set_number,
            'exercises_id': s.exercises_id,
        } for s in sets]
        return JsonResponse(data, safe=False)

    if request.method == 'POST':
        body = parse_body(request)
        if body is None:
            return JsonResponse({'error': 'некорректный JSON'}, status=400)
        for field in ['workout_id', 'set_number', 'exercises_id']:
            if field not in body:
                return JsonResponse({'error': f'нужно поле {field}'}, status=400)
        s = Set.objects.create(
            workout_id=body['workout_id'],
            set_number=body['set_number'],
            exercises_id=body['exercises_id'],
        )
        return JsonResponse({'id': s.id}, status=201)

    return JsonResponse({'error': 'метод не поддерживается'}, status=405)


@csrf_exempt
def set_detail(request, pk):
    s = get_object_or_404(Set, pk=pk)

    if request.method == 'GET':
        return JsonResponse({
            'id': s.id,
            'workout_id': s.workout_id,
            'set_number': s.set_number,
            'exercises_id': s.exercises_id,
        })

    if request.method == 'PUT':
        body = parse_body(request)
        if body is None:
            return JsonResponse({'error': 'некорректный JSON'}, status=400)
        if 'workout_id' in body:
            s.workout_id = body['workout_id']
        if 'set_number' in body:
            s.set_number = body['set_number']
        if 'exercises_id' in body:
            s.exercises_id = body['exercises_id']
        s.save()
        return JsonResponse({'id': s.id, 'status': 'updated'})

    if request.method == 'DELETE':
        s.delete()
        return JsonResponse({'status': 'deleted'})

    return JsonResponse({'error': 'метод не поддерживается'}, status=405)



def stats_regularity_muscle(request, muscle_id):
    days = int(request.GET.get('days', 30))
    muscle = get_object_or_404(MuscleGroup, pk=muscle_id)

    start = timezone.now() - timedelta(days=days)
    workouts = Workout.objects.filter(
        date_time__gte=start,
        set__exercises__muscle_group_id=muscle_id
    ).distinct()

    days_count = workouts.dates('date_time', 'day').count()
    weeks = days / 7
    avg = round(days_count / weeks, 2) if weeks else 0

    return JsonResponse({
        'muscle_group_id': muscle.id,
        'muscle_group_name': muscle.name,
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
        workouts = Workout.objects.filter(
            date_time__gte=start,
            set__exercises__muscle_group_id=mg.id
        ).distinct()
        days_count = workouts.dates('date_time', 'day').count()
        avg = round(days_count / weeks, 2) if weeks else 0

        result.append({
            'muscle_group_id': mg.id,
            'muscle_group_name': mg.name,
            'total_workout_days': days_count,
            'average_per_week': avg,
        })

    return JsonResponse({'period_days': days, 'stats': result})