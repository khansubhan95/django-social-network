# Generated by Django 2.2.2 on 2019-06-14 01:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_post_post_owner'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-post_published']},
        ),
        migrations.AddField(
            model_name='post',
            name='post_image',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
    ]
