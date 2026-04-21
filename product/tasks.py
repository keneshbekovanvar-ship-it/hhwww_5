from celery import shared_task
from .models import Product
from django.core.mail import send_mail


@shared_task
def create_test_product():
    Product.objects.create(name="Test Product", price=100)
    return "Продукт создан"


@shared_task
def delete_cheap_products():
    Product.objects.filter(price__lt=50).delete()
    return "Удалены дешевые продукты"


@shared_task
def send_test_email():
    send_mail(
        'Тестовое письмо',
        'Это сообщение отправлено через Celery',
        'your_email@gmail.com',
        ['test@gmail.com'],
        fail_silently=False,
    )
    return "Письмо отправлено"