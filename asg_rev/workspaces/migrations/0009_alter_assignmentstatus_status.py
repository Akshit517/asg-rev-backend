# Generated by Django 5.1.1 on 2024-12-24 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workspaces', '0008_remove_iteration_status_remove_team_team_leader_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignmentstatus',
            name='status',
            field=models.CharField(choices=[('completed', 'Completed'), ('ongoing', 'Ongoing'), ('incomplete', 'Incomplete')], default='incomplete', max_length=10),
        ),
    ]
