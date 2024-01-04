# Generated by Django 4.2.7 on 2024-01-02 07:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appmart', '0013_productoffer_alter_cartorder_order_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('image', models.ImageField(upload_to='banners/')),
                ('link', models.URLField()),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
    ]