# Generated by Django 3.2.9 on 2021-11-21 11:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('student_management_app', '0002_auto_20211121_1752'),
    ]

    operations = [
        migrations.AddField(
            model_name='leavereportstudent',
            name='subject_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='student_management_app.subjects'),
        ),
    ]
