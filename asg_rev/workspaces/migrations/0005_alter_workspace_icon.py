# Generated by Django 5.1.1 on 2024-12-19 20:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workspaces', '0004_iteration_status_alter_iteration_reviewee_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workspace',
            name='icon',
            field=models.URLField(default='https://api.dicebear.com/9.x/identicon/png?seed=Wyatt', max_length=250),
        ),
    ]
