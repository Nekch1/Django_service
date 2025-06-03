from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

class Service(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название услуги")
    description = models.TextField(verbose_name="Описание")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('service_detail', kwargs={'pk': self.pk})
    
    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"


class Appointment(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Ожидает подтверждения'),
        ('confirmed', 'Подтверждено'),
        ('completed', 'Выполнено'),
        ('cancelled', 'Отменено'),
    )
    
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='appointments', verbose_name="Услуга")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments', verbose_name="Клиент")
    car_model = models.CharField(max_length=100, verbose_name="Модель автомобиля")
    car_year = models.PositiveIntegerField(verbose_name="Год выпуска")
    appointment_date = models.DateField(verbose_name="Дата записи")
    appointment_time = models.TimeField(verbose_name="Время записи")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Статус")
    
    def __str__(self):
        return f"{self.user.username} - {self.service.name} - {self.appointment_date}"
    
    class Meta:
        verbose_name = "Запись на обслуживание"
        verbose_name_plural = "Записи на обслуживание"
        ordering = ['-appointment_date', '-appointment_time']