# Generated by Django 4.0.4 on 2022-05-21 21:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='expense',
            name='Title',
            field=models.CharField(default='Maintainance invoice', max_length=40),
        ),
        migrations.AlterField(
            model_name='expense',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='expense_user', to='app.tenant'),
        ),
    ]