# Generated by Django 4.1 on 2024-01-12 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0021_user_alter_comment_user_alter_post_author_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='cover',
            field=models.ImageField(blank=True, default='', upload_to='recipes/covers/%Y/%m/%d/'),
        ),
    ]
