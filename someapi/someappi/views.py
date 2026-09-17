from json import loads
from datetime import timedelta
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View
from django.utils import timezone
from django.utils.dateparse import parse_date
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from .models import MuscleGroup, Exercise, Workout, Set


def body_of(request):
    try:
        return loads(request.body or '{}')
    except ValueError:
        return None



@method_decorator(csrf_exempt, 'dispatch')
class UserList(View):
    def get(self, request):
        data = [{'id': u.id, 'username': u.username} for u in User.objects.all()]
        return JsonResponse(data, safe=False)

    def post(self, request):
        body = body_of(request)
        if not body or 'username' not in body:
            return JsonResponse({'error': 'нужен username'}, status=400)
        u = User.objects.create_user(username=body['username'])
        return JsonResponse({'id': u.id, 'username': u.username}, status=201)


@method_decorator(csrf_exempt, 'dispatch')
class UserDetail(View):
    def get(self, request, pk):
        u = get_object_or_404(User, pk=pk)
        return JsonResponse({'id': u.id, 'username': u.username})

    def post(self, request, pk):
        u = get_object_or_404(User, pk=pk)
        body = body_of(request)
        if not body or 'username' not in body:
            return JsonResponse({'error': 'нужен username'}, status=400)
        u.username = body['username']
        u.save()
        return JsonResponse({'id': u.id, 'username': u.username})

@method_decorator(csrf_exempt, 'dispatch')
class MuscleGroupList(View):
    def get(self, request):
        data = [{'id': g.id, 'name': g.name, 'body_part': g.body_part}
                for g in MuscleGroup.objects.all()]
        return JsonResponse(data, safe=False)

    def post(self, request):
        body = body_of(request)
        if not body or 'name' not in body or 'body_part' not in body:
            return JsonResponse({'error': 'нужны name и body_part'}, status=400)
        g = MuscleGroup.objects.create(name=body['name'], body_part=body['body_part'])
        return JsonResponse({'id': g.id, 'name': g.name, 'body_part': g.body_part}, status=201)


@method_decorator(csrf_exempt, 'dispatch')
class MuscleGroupDetail(View):
    def get(self, request, pk):
        g = get_object_or_404(MuscleGroup, pk=pk)
        return JsonResponse({'id': g.id, 'name': g.name, 'body_part': g.body_part})

    def post(self, request, pk):
        g = get_object_or_404(MuscleGroup, pk=pk)
        body = body_of(request)
        if not body:
            return JsonResponse({'error': 'плохой JSON'}, status=400)
        if 'name' in body:
            g.name = body['name']
        if 'body_part' in body:
            g.body_part = body['body_part']
        g.save()
        return JsonResponse({'id': g.id, 'name': g.name, 'body_part': g.body_part})


@method_decorator(csrf_exempt, 'dispatch')
class ExerciseList(View):
    def get(self, request):
        qs = Exercise.objects.all()
        mg_id = request.GET.get('muscle_group_id')
        if mg_id:
            qs = qs.filter(muscle_group_id=mg_id)
        data = [{'id': e.id, 'name': e.name, 'muscle_group_id': e.muscle_group_id}
                for e in qs]
        return JsonResponse(data, safe=False)

    def post(self, request):
        body = body_of(request)
        if not body or 'name' not in body or 'muscle_group_id' not in body:
            return JsonResponse({'error': 'нужны name и muscle_group_id'}, status=400)
        e = Exercise.objects.create(name=body['name'], muscle_group_id=body['muscle_group_id'])
        return JsonResponse({'id': e.id, 'name': e.name}, status=201)


@method_decorator(csrf_exempt, 'dispatch')
class ExerciseDetail(View):
    def get(self, request, pk):
        e = get_object_or_404(Exercise, pk=pk)
        return JsonResponse({'id': e.id, 'name': e.name, 'muscle_group_id': e.muscle_group_id})

    def post(self, request, pk):
        e = get_object_or_404(Exercise, pk=pk)
        body = body_of(request)
        if not body:
            return JsonResponse({'error': 'плохой JSON'}, status=400)
        if 'name' in body:
            e.name = body['name']
        if 'muscle_group_id' in body:
            e.muscle_group_id = body['muscle_group_id']
        e.save()
        return JsonResponse({'id': e.id, 'name': e.name})


@method_decorator(csrf_exempt, 'dispatch')
class WorkoutList(View):
    def get(self, request):
        qs = Workout.objects.all().order_by('-date_time')
        user_id = request.GET.get('user_id')
        if user_id:
            qs = qs.filter(user_id=user_id)
        data = [{'id': w.id, 'date_time': w.date_time.isoformat(),
                 'started_ad': w.started_ad, 'duration_min': w.duration_min,
                 'comment': w.comment, 'user_id': w.user_id} for w in qs]
        return JsonResponse(data, safe=False)

    def post(self, request):
        body = body_of(request)
        if not body:
            return JsonResponse({'error': 'плохой JSON'}, status=400)
        for f in ['date_time', 'started_ad', 'duration_min', 'comment', 'user_id']:
            if f not in body:
                return JsonResponse({'error': f'нужно {f}'}, status=400)
        w = Workout.objects.create(
            date_time=body['date_time'], started_ad=body['started_ad'],
            duration_min=body['duration_min'], comment=body['comment'],
            user_id=body['user_id'],
        )
        return JsonResponse({'id': w.id}, status=201)


@method_decorator(csrf_exempt, 'dispatch')
class WorkoutDetail(View):
    def get(self, request, pk):
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

    def post(self, request, pk):
        w = get_object_or_404(Workout, pk=pk)
        body = body_of(request)
        if not body:
            return JsonResponse({'error': 'плохой JSON'}, status=400)
        for f in ['date_time', 'started_ad', 'duration_min', 'comment', 'user_id']:
            if f in body:
                setattr(w, f, body[f])
        w.save()
        return JsonResponse({'id': w.id, 'status': 'updated'})


@method_decorator(csrf_exempt, 'dispatch')
class WorkoutFilter(View):
    def get(self, request):
        return self.run_filter(request.GET.get('from'), request.GET.get('to'))

    def post(self, request):
        body = body_of(request) or {}
        return self.run_filter(body.get('from'), body.get('to'))

    def run_filter(self, from_str, to_str):
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

@method_decorator(csrf_exempt, 'dispatch')
class SetList(View):
    def get(self, request):
        qs = Set.objects.all().order_by('workout_id', 'set_number')
        workout_id = request.GET.get('workout_id')
        if workout_id:
            qs = qs.filter(workout_id=workout_id)
        data = [{'id': s.id, 'workout_id': s.workout_id,
                 'set_number': s.set_number, 'exercises_id': s.exercises_id}
                for s in qs]
        return JsonResponse(data, safe=False)

    def post(self, request):
        body = body_of(request)
        if not body:
            return JsonResponse({'error': 'плохой JSON'}, status=400)
        for f in ['workout_id', 'set_number', 'exercises_id']:
            if f not in body:
                return JsonResponse({'error': f'нужно {f}'}, status=400)
        s = Set.objects.create(
            workout_id=body['workout_id'], set_number=body['set_number'],
            exercises_id=body['exercises_id'],
        )
        return JsonResponse({'id': s.id}, status=201)

@method_decorator(csrf_exempt, 'dispatch')
class SetDetail(View):
    def get(self, request, pk):
        s = get_object_or_404(Set, pk=pk)
        return JsonResponse({'id': s.id, 'workout_id': s.workout_id,
                             'set_number': s.set_number, 'exercises_id': s.exercises_id})

    def post(self, request, pk):
        s = get_object_or_404(Set, pk=pk)
        body = body_of(request)
        if not body:
            return JsonResponse({'error': 'плохой JSON'}, status=400)
        for f in ['workout_id', 'set_number', 'exercises_id']:
            if f in body:
                setattr(s, f, body[f])
        s.save()
        return JsonResponse({'id': s.id, 'status': 'updated'})



@method_decorator(csrf_exempt, 'dispatch')
class StatsRegularityMuscle(View):
    def get(self, request, muscle_id):
        days = int(request.GET.get('days', 30))
        return self.calc(muscle_id, days)

    def post(self, request, muscle_id):
        body = body_of(request) or {}
        days = int(body.get('days', 30))
        return self.calc(muscle_id, days)

    def calc(self, muscle_id, days):
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


@method_decorator(csrf_exempt, 'dispatch')
class StatsRegularityAll(View):
    def get(self, request):
        days = int(request.GET.get('days', 7))
        return self.calc(days)

    def post(self, request):
        body = body_of(request) or {}
        days = int(body.get('days', 7))
        return self.calc(days)

    def calc(self, days):
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