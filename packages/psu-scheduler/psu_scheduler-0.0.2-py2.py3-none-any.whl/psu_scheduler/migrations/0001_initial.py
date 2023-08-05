# Generated by Django 2.2.15 on 2021-01-27 09:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='JobDefinition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('app_code', models.CharField(db_index=True, help_text='Application that this job belongs to.', max_length=15, verbose_name='Application Code')),
                ('status_ind', models.CharField(default='A', max_length=1)),
                ('title', models.CharField(db_index=True, max_length=80)),
                ('endpoint', models.CharField(db_index=True, max_length=200)),
                ('performer', models.CharField(blank=True, help_text='This holds the username of the job performer, if applicable', max_length=30, null=True)),
                ('start_date', models.DateTimeField(blank=True, null=True)),
                ('end_date', models.DateTimeField(blank=True, null=True)),
                ('run_days', models.CharField(blank=True, default='', max_length=7)),
                ('run_times_csv', models.CharField(blank=True, default='', max_length=30)),
                ('run_frequency', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='JobExecution',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('key', models.CharField(db_index=True, max_length=20)),
                ('status', models.CharField(default='init', max_length=30)),
                ('output', models.TextField(blank=True, null=True)),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='psu_scheduler.JobDefinition')),
            ],
        ),
    ]
