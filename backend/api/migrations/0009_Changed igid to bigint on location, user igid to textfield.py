# Generated by Django 2.0.5 on 2018-05-26 21:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_User delete cascade rule on caption'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instagramlocation',
            name='instagram_id',
            field=models.BigIntegerField(unique=True),
        ),
        migrations.AlterField(
            model_name='instagramuser',
            name='instagram_id',
            field=models.TextField(unique=True),
        ),
    ]
