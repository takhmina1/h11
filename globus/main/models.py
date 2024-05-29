from django.db import models
from django.db import models
from django.utils.translation import gettext_lazy as _
from ckeditor.fields import RichTextField
from datetime import datetime

class Stories(models.Model):
    created_at = models.DateTimeField(_("Дата и время"), auto_now_add=True)
    img = models.ImageField(_("Изображение"), upload_to="story_images")
    link = models.URLField(_('Ссылка'), max_length=500, blank=True, null=True, help_text='Если есть')

    class Meta:
        verbose_name = _("История")
        verbose_name_plural = _("Истории")

    def __str__(self):
        return f"История {self.created_at.strftime('%d %B %Y г. %H:%M')}"

class StoryVideos(models.Model):
    story = models.ForeignKey(Stories, on_delete=models.CASCADE, related_name="videos")
    url = models.FileField(_("История"), upload_to="stories")
    created_at = models.DateTimeField(_("Дата и время"), auto_now_add=True)

    class Meta:
        verbose_name = _("Видео к истории")
        verbose_name_plural = _("Видео к историям")

    def __str__(self):
        return f"Видео к истории {self.story.created_at.strftime('%d %B %Y г. %H:%M')}"

class Cards(models.Model):
    TYPE_CHOICES = [
        (1, 'Специальные предложения'),
        (2, 'Акция')
    ]

    type = models.IntegerField('Тип', choices=TYPE_CHOICES)
    text = models.TextField('Описание', blank=True, null=True)
    title = models.CharField('Название', max_length=150, help_text='Успей купить!')
    datefrom = models.DateField('Дата начала акции')
    dateto = models.DateField('Дата окончания акции')
    date = models.CharField(blank=True, null=True, max_length=150, editable=False)
    img = models.ImageField('Картинка', upload_to='promotions/%Y_%m')

    class Meta:
        verbose_name = 'Карточка'
        verbose_name_plural = 'Карточки (Акция/Предложения)'

    def __str__(self):
        return self.title

    def delete(self, using=None, keep_parents=False):
        if int(self.dateto.strftime('%d')) < int(datetime.today().strftime("%d")):
            if int(self.dateto.strftime('%m')) == int(datetime.today().strftime("%m")):
                super().delete()

class Notifications(models.Model):
    title = models.CharField(_('Уведомление'), max_length=1000)
    description = RichTextField(_("Описание"), blank=True, null=True)
    date = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = 'Уведомление'
        verbose_name_plural = 'Уведомления'

    def __str__(self):
        return self.title

class NotificationsImg(models.Model):
    notification = models.ForeignKey(Notifications, on_delete=models.CASCADE, related_name='images')
    img = models.ImageField(_("Картинка"), upload_to='notifications/%Y_%m')

    class Meta:
        verbose_name = 'Картинка для уведомления'
        verbose_name_plural = 'Картинки для уведомлений'

class Versions(models.Model):
    version = models.CharField(_("Версия"), max_length=255)
    appstore = models.URLField(_("App Store"))
    googleplay = models.URLField(_("Google Play"))
    date = models.DateTimeField(_("Дата"), auto_now_add=True)

    class Meta:
        verbose_name = _("Версия приложения")
        verbose_name_plural = _("Версии приложения")

    def __str__(self):
        return f"Версия {self.version}"

