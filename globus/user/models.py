from django.db import models
# Импорт необходимых библиотек и модулей
import os  # Модуль для работы с операционной системой
import random  # Модуль для генерации случайных чисел
import qrcode  # Библиотека для создания QR-кодов

from django.contrib.auth.models import AbstractUser  # Базовая модель пользователя Django
from django.db import models  # Модуль для определения моделей базы данных
from django.conf import settings  # Настройки Django
from django.dispatch import receiver  # Декоратор для обработки сигналов Django
from django.db.models.signals import post_save  # Сигнал после сохранения объекта

# Импорт настроенного менеджера пользователя и набора выборов
from .managers import CustomUserManager
from .choices import *

# Модель пользователя
class User(AbstractUser):
    # Заменяем поле "имя пользователя" полем "телефон"
    username = None
    phone = models.CharField("Номер телефона", unique=True)  # Уникальный номер телефона

    # Дополнительные поля пользователя
    code = models.IntegerField("Код активации", null=True, blank=True)  # Код активации
    activated = models.BooleanField("Активировано", default=False)  # Флаг активации
    bonus_id = models.CharField("Бонусный ID", null=True, blank=True)  # Уникальный бонусный идентификатор
    bonus = models.DecimalField("Бонус пользователя", max_digits=10, decimal_places=2, null=True, blank=True)  # Бонус пользователя
    qrimg = models.ImageField("QR-код пользователя", null=True, blank=True)  # QR-код пользователя

    # Настройки уведомлений
    notification = models.BooleanField("Получать уведомления", default=False)  # Флаг получения уведомлений
    auto_brightness = models.BooleanField("Автояркость", default=False)  # Флаг автоматической яркости
    email = models.EmailField("Электронная почта", max_length=254, blank=True, null=True)  # Электронная почта

    # Дополнительные характеристики пользователя
    USER_CHOICE = [('1', 'Клиент'), ('2', 'Оптовик')]  # Выбор роли пользователя
    user_roll = models.CharField('Роль', max_length=100, choices=USER_CHOICE, default='1')  # Роль пользователя
    roll_request = models.BooleanField("Запрос на контрагент уже есть", default=False)  # Флаг запроса на изменение роли
    birthday = models.DateField("Дата рождения", null=True, blank=True)  # Дата рождения
    gender = models.CharField("Пол", max_length=50, choices=GENDERS_CHOICES, null=True, blank=True)  # Пол
    language = models.CharField("Родной язык", max_length=50, choices=LANGUAGE_CHOICES, null=True, blank=True)  # Родной язык
    married = models.CharField("Семейное положение", max_length=100, choices=MARRIED_CHOICES, null=True, blank=True)  # Семейное положение
    status = models.CharField("Социальный статус", max_length=100, choices=SOCIAL_STATUS_CHOICES, null=True, blank=True)  # Социальный статус
    city = models.CharField("Город проживания", max_length=100, choices=CITY_CHOICES, null=True, blank=True)  # Город проживания
    children = models.BooleanField("Наличие детей", default=False)  # Флаг наличия детей
    animal = models.BooleanField("Наличие домашних животных", default=False)  # Флаг наличия домашних животных
    car = models.BooleanField("Наличие автомобиля", default=False)  # Флаг наличия автомобиля

    # Устанавливаем номер телефона как основное поле и используем настроенный менеджер
    USERNAME_FIELD = "phone"
    objects = CustomUserManager()

    # Переопределение метода сохранения для добавления бонуса и QR-кода
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        bonus_id = f"{1000200030004000 + int(self.id)}"
        self.bonus_id = bonus_id
        self.code = random.randint(100_000, 999_999)
        qr = qrcode.make(str(bonus_id), border=2)
        qr_path = f"user/bonus-qr/{bonus_id}.png"
        qr.save(os.path.join(settings.MEDIA_ROOT, qr_path))
        self.qrimg.name = qr_path
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

# Модель запроса на изменение роли пользователя
class RollRequest(models.Model):
    # Варианты ролей
    USER_CHOICE = [('1', 'Клиент'), ('2', 'Оптовик')]

    # Связь с пользователем и характеристики запроса
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    roll = models.CharField('Роль', max_length=100, choices=USER_CHOICE, default='1')
    name = models.CharField('Имя', max_length=100, null=True, blank=True)
    surname = models.CharField('Фамилия', max_length=100, null=True, blank=True)
    date_time = models.CharField('Дата и Время', max_length=100, null=True, blank=True)

    # Переопределение метода сохранения для изменения роли пользователя
    def save(self, *args, **kwargs):
        if self.roll == '2':
            self.user.user_roll = '2'
            
            
