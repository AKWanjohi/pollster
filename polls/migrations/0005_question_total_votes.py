# Generated by Django 3.2.9 on 2021-11-22 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0004_questionvoter'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='total_votes',
            field=models.IntegerField(default=0),
        ),
    ]