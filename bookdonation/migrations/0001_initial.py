# Generated by Django 4.2.6 on 2023-10-29 18:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='data_donasi1',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('judul_buku', models.CharField(max_length=255)),
                ('total_buku', models.IntegerField()),
                ('resi', models.TextField()),
                ('status', models.CharField(max_length=255)),
            ],
        ),
    ]
