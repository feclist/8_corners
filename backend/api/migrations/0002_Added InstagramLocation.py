# Generated by Django 2.0.5 on 2018-05-23 00:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_Initial database model'),
    ]

    operations = [
        migrations.CreateModel(
            name='InstagramLocation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('instagram_id', models.IntegerField(unique=True)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('name', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='instagrampost',
            name='location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='api.InstagramLocation'),
        ),
    ]