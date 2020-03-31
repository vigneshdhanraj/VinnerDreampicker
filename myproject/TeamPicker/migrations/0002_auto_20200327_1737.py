# Generated by Django 3.0.4 on 2020-03-27 17:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TeamPicker', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Player_List',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Team', models.CharField(max_length=264)),
                ('Name', models.CharField(max_length=264)),
                ('Role', models.CharField(max_length=264)),
                ('Credit', models.CharField(max_length=264)),
            ],
        ),
        migrations.DeleteModel(
            name='Team1',
        ),
        migrations.DeleteModel(
            name='Team2',
        ),
    ]