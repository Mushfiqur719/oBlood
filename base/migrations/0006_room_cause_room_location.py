# Generated by Django 4.0.2 on 2022-03-02 04:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_alter_message_id_alter_room_id_alter_topic_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='cause',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='room',
            name='location',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
    ]