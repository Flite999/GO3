# Generated by Django 4.2.11 on 2024-03-21 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0016_alter_memberpreferences_calendar_show_only_committed_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='display_name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='member',
            name='images',
            field=models.TextField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='member',
            name='nickname',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='member',
            name='phone',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='member',
            name='statement',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
