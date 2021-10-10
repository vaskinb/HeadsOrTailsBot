from django.db import models


class Profile(models.Model):
    external_id = models.PositiveIntegerField(
        verbose_name='ID игрока ',
        unique=True,
    )
    name = models.TextField(
        verbose_name='Имя игрока',
    )
    balance = models.IntegerField(
        verbose_name='Баланс'
    )

    def __str__(self):
        return f' {self.name} {self.balance}'

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'
