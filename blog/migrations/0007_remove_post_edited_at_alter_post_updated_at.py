# Generated by Django 4.1 on 2023-12-27 21:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_comment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='edited_at',
        ),
        migrations.AlterField(
            model_name='post',
            name='updated_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
