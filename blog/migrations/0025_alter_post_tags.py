# Generated by Django 4.1 on 2024-01-13 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0024_category_tag_post_category_post_tags'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='tags',
            field=models.ManyToManyField(to='blog.tag'),
        ),
    ]
