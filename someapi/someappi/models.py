from django.db import models


class User(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'user'

    def __str__(self):
        return self.name


class MuscleGroup(models.Model):
    name = models.CharField(max_length=255)
    body_part = models.CharField(max_length=255)

    class Meta:
        db_table = 'muscle_groups'

    def __str__(self):
        return self.name


class Exercise(models.Model):
    muscle_group = models.ForeignKey(MuscleGroup, on_delete=models.CASCADE, db_column='muscle_group_id')
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'exercises'

    def __str__(self):
        return self.name


class Workout(models.Model):
    date_time = models.DateTimeField()
    started_ad = models.CharField(max_length=255)
    duration_min = models.CharField(max_length=255)
    comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user_id')

    class Meta:
        db_table = 'workouts'

    def __str__(self):
        return f"Workout {self.id}"


class Set(models.Model):
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE, db_column='workout_id')
    set_number = models.IntegerField()
    exercises = models.ForeignKey(Exercise, on_delete=models.CASCADE, db_column='exercises_id')

    class Meta:
        db_table = 'sets'

    def __str__(self):
        return f"Set {self.id}"