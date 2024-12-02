# Generated by Django 5.1.3 on 2024-12-02 19:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0010_color_size_remove_product_country_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='size',
            field=models.ManyToManyField(blank=True, null=True, related_name='products', to='product.size'),
        ),
    ]