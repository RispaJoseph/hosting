# Generated by Django 4.2.6 on 2023-11-16 05:48

from django.db import migrations
import shortuuid.django_fields


class Migration(migrations.Migration):

    dependencies = [
        ('appmart', '0003_tags_alter_category_cid_alter_category_title_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Tags',
        ),
        migrations.AlterField(
            model_name='category',
            name='cid',
            field=shortuuid.django_fields.ShortUUIDField(alphabet='abcdefgh12345', length=22, max_length=20, prefix='cat', unique=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='pid',
            field=shortuuid.django_fields.ShortUUIDField(alphabet=None, length=10, max_length=20, prefix='', unique=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='sku',
            field=shortuuid.django_fields.ShortUUIDField(alphabet=None, length=22, max_length=20, prefix='', unique=True),
        ),
    ]