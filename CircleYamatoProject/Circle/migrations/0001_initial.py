# Generated by Django 3.0.5 on 2020-05-02 08:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Members',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(verbose_name='name')),
                ('sex', models.TextField(verbose_name='sex')),
                ('age', models.IntegerField(verbose_name='age')),
                ('update_date', models.DateTimeField(verbose_name='update_date')),
                ('commit_date', models.DateTimeField(verbose_name='commit_date')),
            ],
            options={
                'verbose_name': 'メンバー',
                'verbose_name_plural': 'メンバー',
                'db_table': 'MEMBERS',
            },
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('schedule_date', models.DateField(verbose_name='schedule_date')),
                ('start_time', models.TimeField(verbose_name='start_time')),
                ('end_time', models.TimeField(verbose_name='end_time')),
                ('summary', models.TextField(max_length=50, verbose_name='summary')),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('update_date', models.DateTimeField(verbose_name='update_date')),
                ('commit_date', models.DateTimeField(verbose_name='commit_date')),
            ],
            options={
                'verbose_name': 'スケジュール',
                'verbose_name_plural': 'スケジュール',
                'db_table': 'SCHEDULE',
            },
        ),
        migrations.CreateModel(
            name='Forum',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('posted_date', models.DateTimeField(verbose_name='posted_date')),
                ('name', models.TextField(verbose_name='name')),
                ('contents', models.TextField(verbose_name='contents')),
                ('good_count', models.IntegerField(verbose_name='good_count')),
                ('update_date', models.DateTimeField(verbose_name='update_date')),
                ('commit_date', models.DateTimeField(verbose_name='commit_date')),
            ],
            options={
                'verbose_name': '掲示板',
                'verbose_name_plural': '掲示板',
                'db_table': 'FORUM',
            },
        ),
    ]
