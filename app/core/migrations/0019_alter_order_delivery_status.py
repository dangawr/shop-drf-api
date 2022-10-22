# Generated by Django 4.1.2 on 2022-10-19 19:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_remove_orderitem_delivery_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='delivery_status',
            field=models.CharField(choices=[('W', 'Waiting for payment'), ('C', 'Collecting order'), ('S', 'Sent')], default='Waiting for payment', max_length=1),
        ),
    ]
