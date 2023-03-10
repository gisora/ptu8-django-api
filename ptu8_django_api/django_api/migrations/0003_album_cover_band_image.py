# Generated by Django 4.1.7 on 2023-03-07 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_api', '0002_alter_albumreview_score'),
    ]

    operations = [
        migrations.AddField(
            model_name='album',
            name='cover',
            field=models.ImageField(blank=True, null=True, upload_to='django_api/covers'),
        ),
        migrations.AddField(
            model_name='band',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='django_api/images'),
        ),
    ]
