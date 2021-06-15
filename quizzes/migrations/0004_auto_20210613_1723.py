# Generated by Django 3.1.5 on 2021-06-13 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizzes', '0003_lesson'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='is_free',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='quiz',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5),
        ),
    ]