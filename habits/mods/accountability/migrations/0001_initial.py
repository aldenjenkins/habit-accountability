# Generated by Django 3.1.6 on 2021-02-03 02:59

from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Habit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_ts', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='Created')),
                ('update_ts', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='Modified')),
                ('name', models.CharField(max_length=256)),
            ],
            options={
                'ordering': ('-update_ts', '-create_ts'),
                'get_latest_by': 'update_ts',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='HabitCompletion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_ts', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='Created')),
                ('update_ts', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='Modified')),
                ('did_complete', models.BooleanField(default=False)),
                ('habit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accountability.habit')),
            ],
            options={
                'ordering': ('-update_ts', '-create_ts'),
                'get_latest_by': 'update_ts',
                'abstract': False,
            },
        ),
    ]
