# Generated by Django 4.1.2 on 2022-11-03 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('regbot', '0002_rename_chat_temp_tgid'),
    ]

    operations = [
        migrations.AddField(
            model_name='temp',
            name='state',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
    ]