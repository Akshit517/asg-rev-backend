# Generated by Django 5.1.1 on 2024-10-15 06:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workspaces', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment',
            name='description',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
