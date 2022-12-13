# Generated by Django 2.2.16 on 2022-12-13 08:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20221206_2350'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='follow',
            name='unique_combination',
        ),
        migrations.AddConstraint(
            model_name='follow',
            constraint=models.UniqueConstraint(fields=('user', 'author'), name='unique__follow'),
        ),
    ]