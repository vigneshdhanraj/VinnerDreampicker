# Generated by Django 3.0.4 on 2020-03-31 11:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('TeamPicker', '0003_delete_player_list'),
    ]

    operations = [
        migrations.CreateModel(
            name='Series',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Match', models.CharField(max_length=264)),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=264)),
                ('Role', models.CharField(max_length=264)),
                ('Credit', models.CharField(max_length=264)),
                ('Team', models.CharField(choices=[('Team1', 'Team1'), ('Team2', 'Team2')], max_length=264)),
                ('Series', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='series', to='TeamPicker.Series')),
            ],
        ),
    ]