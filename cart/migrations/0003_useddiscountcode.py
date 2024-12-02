# Generated by Django 5.1.3 on 2024-11-22 19:54

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0002_order_orderitem'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UsedDiscountCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('discount_code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='UsedDiscountCodes', to='cart.discountcode')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='UsedDiscountCodes', to='cart.order')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='UsedDiscountCodes', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]