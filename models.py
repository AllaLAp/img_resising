from django.db import models
from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from django.contrib.auth import get_user_model


User = get_user_model()


class Advertisement(models.Model):
    title = models.CharField('НАЗВАНИЕ', max_length=128)
    description = models.TextField('Описание')
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2)
    auction = models.BooleanField('Торг', help_text='отметьте, если торг уместен')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    image = models.ImageField('Изображения', upload_to='advertisements/',eight_field=125, width_field=125)

    @admin.display(description='Дата создания')
    def created_date(self):
        if self.created_at.date()== timezone.now().date():
            created_time = self.created_at.time().strftime('%H:%M:%S')
            return format_html(
                '<span style="color:green; font-weigh:bold;"> Сегодня в {} </span>', created_time
            )
        return self.created_at.strftime('%d.%m.%y в %H:%M:%S')

    @admin.display(description='Дата последнего обновления')
    def check_update(self):
        if self.updated_at.date() == timezone.now().date():
            created_date = self.updated_at.time().strftime('%H:%M:%S')
            return format_html(
                '<span style="color:blue; font-weigh:bold;"> Сегодня в {} </span>', created_date
            )
        return self.updated_at.strftime('%d.%m.%y в %H:%M:%S')
    
    @admin.display(description='Изображение')
    def show_image(self):
        if self.image:
            return format_html(
                u'<img src="%s" />' % self.image.url
            )
        else:
            return 'have not image'
    show_image.short_description = 'Изображение'
    
    
    def __str__(self): 
        return f"Advertisemenet(id={str(self.id)}, title={self.title}, price={self.price})"

    class Meta:
        db_table = 'advertisements'
