# Generated by Django 4.0.4 on 2022-05-21 21:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_expense_title_alter_expense_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='expense',
            old_name='user',
            new_name='Expense_User',
        ),
    ]
