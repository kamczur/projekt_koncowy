# Generated by Django 4.0.4 on 2022-06-23 18:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imprezy', '0021_remove_gift_party'),
    ]

    operations = [
        migrations.AddField(
            model_name='gift',
            name='party',
            field=models.ManyToManyField(to='imprezy.party'),
        ),
    ]
