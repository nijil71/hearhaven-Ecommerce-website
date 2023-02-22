# Generated by Django 4.0.4 on 2023-02-15 04:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopurban', '0009_customerdetails'),
    ]

    operations = [
        migrations.CreateModel(
            name='CardDetailsModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cardnumber', models.CharField(max_length=100)),
                ('cardname', models.CharField(max_length=100)),
                ('cardexpiry', models.CharField(max_length=100)),
                ('cardcvv', models.CharField(max_length=100)),
            ],
        ),
        migrations.DeleteModel(
            name='CustomerDetails',
        ),
    ]