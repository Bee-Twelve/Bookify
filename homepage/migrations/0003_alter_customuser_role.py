# Generated by Django 4.2.6 on 2023-10-27 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0002_alter_customuser_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='role',
            field=models.CharField(choices=[('member', 'Member'), ('moderator', 'Moderator'), ('guest', 'Guest')], default='guest', max_length=10),
        ),
    ]
