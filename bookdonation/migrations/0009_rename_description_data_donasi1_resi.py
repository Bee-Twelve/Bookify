# Generated by Django 4.2.6 on 2023-10-26 05:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookdonation', '0008_rename_amount_data_donasi1_total_buku'),
    ]

    operations = [
        migrations.RenameField(
            model_name='data_donasi1',
            old_name='description',
            new_name='resi',
        ),
    ]
