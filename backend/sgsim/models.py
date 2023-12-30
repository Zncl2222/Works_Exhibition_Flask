from django.db import models
from users.models import User


class SgsimParams(models.Model):
    realizations_number = models.PositiveIntegerField()
    cov_model = models.CharField(max_length=20)
    kernel = models.CharField(
        max_length=10,
        choices=(
            ('Python', 'Python'),
            ('C', 'C'),
        ),
    )
    bandwidth = models.FloatField()
    bandwidth_step = models.FloatField()
    x_size = models.IntegerField()
    y_size = models.IntegerField()
    randomseed = models.IntegerField()
    krige_range = models.FloatField()
    krige_sill = models.FloatField()


class SgsimHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    parameters = models.ForeignKey(
        'SgsimParams',
        on_delete=models.CASCADE,
    )
    results = models.JSONField()
    create_date = models.DateTimeField(auto_now_add=True)
    run_time = models.FloatField()
