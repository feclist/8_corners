# Generated by Django 2.0.5 on 2018-05-24 17:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_Added InstagramLocation'),
    ]

    operations = [
        migrations.CreateModel(
            name='InstagramImages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('thumbnail_width', models.IntegerField()),
                ('thumbnail_height', models.IntegerField()),
                ('thumbnail_url', models.URLField()),
                ('low_res_width', models.IntegerField()),
                ('low_res_height', models.IntegerField()),
                ('low_res_url', models.URLField()),
                ('standard_res_width', models.IntegerField()),
                ('standard_res_height', models.IntegerField()),
                ('standard_res_url', models.URLField()),
            ],
        ),
        migrations.AddField(
            model_name='instagrampost',
            name='images',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='api.InstagramImages'),
            preserve_default=False,
        ),
    ]
