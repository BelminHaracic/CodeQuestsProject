# Generated by Django 4.2 on 2023-04-25 19:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('CodeQuestsApp', '0003_task_name_alter_task_difficulty_level_solution_match_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Table',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
                ('level', models.IntegerField(default=1)),
            ],
        ),
        migrations.AlterField(
            model_name='task',
            name='difficulty_level',
            field=models.CharField(choices=[('V', 'Very Easy'), ('E', 'Easy'), ('M', 'Medium'), ('H', 'Hard'), ('R', 'Really Hard')], default='M', max_length=1),
        ),
        migrations.CreateModel(
            name='Ranking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rank', models.IntegerField()),
                ('points', models.IntegerField()),
                ('table', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CodeQuestsApp.table')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]