# Generated by Django 2.2.24 on 2021-12-23 12:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('item_id', models.AutoField(primary_key=True, serialize=False)),
                ('item_name', models.CharField(max_length=200)),
                ('category', models.CharField(choices=[('Beverage', 'beverage'), ('Dairy_products', 'Dairy_products')], max_length=200)),
                ('required_quantity', models.IntegerField()),
                ('quantity', models.IntegerField()),
                ('price', models.FloatField()),
                ('carted', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('item_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='grocery_shop.Inventory')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'item_id')},
            },
        ),
    ]
