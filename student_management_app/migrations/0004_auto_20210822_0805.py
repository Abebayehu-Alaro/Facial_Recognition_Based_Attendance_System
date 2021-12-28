# Generated by Django 3.2.4 on 2021-08-22 15:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('student_management_app', '0003_alter_users_user_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='camera',
            name='batch',
            field=models.CharField(default='2020', max_length=10),
        ),
        migrations.AddField(
            model_name='camera',
            name='department_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='student_management_app.departments'),
        ),
        migrations.AddField(
            model_name='camera',
            name='section',
            field=models.CharField(default='A', max_length=4),
        ),
    ]