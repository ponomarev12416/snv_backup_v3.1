# Generated by Django 4.0.5 on 2022-07-14 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backup', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='repository',
            options={'ordering': ['modified']},
        ),
        migrations.AddField(
            model_name='job',
            name='run_only_once',
            field=models.BooleanField(default=False),
        ),
    ]
