from datetime import datetime, timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from someappi.models import User, MuscleGroup, Exercise, Workout, Set


class Command(BaseCommand):
    help = 'Заполняет базу тестовыми данными'

    def handle(self, *args, **options):
        self.stdout.write('Чистим старые данные...')
        Set.objects.all().delete()
        Workout.objects.all().delete()
        Exercise.objects.all().delete()
        MuscleGroup.objects.all().delete()
        User.objects.all().delete()

        self.stdout.write('Создаём пользователей...')
        users = [
            User.objects.create(name='Иван'),
            User.objects.create(name='Пётр'),
            User.objects.create(name='Анна'),
        ]


        self.stdout.write('Создаём группы мышц...')
        chest = MuscleGroup.objects.create(name='Грудь', body_part='Верх тела')
        back = MuscleGroup.objects.create(name='Спина', body_part='Верх тела')
        legs = MuscleGroup.objects.create(name='Ноги', body_part='Низ тела')
        arms = MuscleGroup.objects.create(name='Руки', body_part='Верх тела')


        self.stdout.write('Создаём упражнения...')
        bench = Exercise.objects.create(name='Жим лёжа', muscle_group=chest)
        pushups = Exercise.objects.create(name='Отжимания', muscle_group=chest)
        pullups = Exercise.objects.create(name='Подтягивания', muscle_group=back)
        rows = Exercise.objects.create(name='Тяга штанги', muscle_group=back)
        squats = Exercise.objects.create(name='Приседания', muscle_group=legs)
        deadlift = Exercise.objects.create(name='Становая тяга', muscle_group=legs)
        curl = Exercise.objects.create(name='Подъём на бицепс', muscle_group=arms)


        self.stdout.write('Создаём тренировки...')
        now = timezone.now()

        w1 = Workout.objects.create(
            date_time=now - timedelta(days=1),
            started_ad='10:00',
            duration_min='60',
            comment='Грудь и трицепс',
            user=users[0],
        )
        w2 = Workout.objects.create(
            date_time=now - timedelta(days=3),
            started_ad='18:30',
            duration_min='75',
            comment='Спина',
            user=users[0],
        )
        w3 = Workout.objects.create(
            date_time=now - timedelta(days=2),
            started_ad='08:00',
            duration_min='50',
            comment='Ноги',
            user=users[1],
        )
        w4 = Workout.objects.create(
            date_time=now - timedelta(days=5),
            started_ad='19:00',
            duration_min='90',
            comment='Full body',
            user=users[2],
        )


        self.stdout.write('Создаём подходы...')

        Set.objects.create(workout=w1, set_number=1, exercises=bench)
        Set.objects.create(workout=w1, set_number=2, exercises=bench)
        Set.objects.create(workout=w1, set_number=3, exercises=bench)
        Set.objects.create(workout=w1, set_number=4, exercises=pushups)

        Set.objects.create(workout=w2, set_number=1, exercises=pullups)
        Set.objects.create(workout=w2, set_number=2, exercises=pullups)
        Set.objects.create(workout=w2, set_number=3, exercises=rows)


        Set.objects.create(workout=w3, set_number=1, exercises=squats)
        Set.objects.create(workout=w3, set_number=2, exercises=squats)
        Set.objects.create(workout=w3, set_number=3, exercises=deadlift)


        Set.objects.create(workout=w4, set_number=1, exercises=bench)
        Set.objects.create(workout=w4, set_number=2, exercises=pullups)
        Set.objects.create(workout=w4, set_number=3, exercises=squats)
        Set.objects.create(workout=w4, set_number=4, exercises=curl)

        self.stdout.write(self.style.SUCCESS('Готово. База заполнена.'))
        self.stdout.write(f'  Пользователей: {User.objects.count()}')
        self.stdout.write(f'  Групп мышц:    {MuscleGroup.objects.count()}')
        self.stdout.write(f'  Упражнений:    {Exercise.objects.count()}')
        self.stdout.write(f'  Тренировок:    {Workout.objects.count()}')
        self.stdout.write(f'  Подходов:      {Set.objects.count()}')