# Generated by Django 5.1.1 on 2024-09-29 15:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_role_role_level'),
        ('workspaces', '0002_alter_categoryrole_unique_together_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Role',
        ),
    ]
