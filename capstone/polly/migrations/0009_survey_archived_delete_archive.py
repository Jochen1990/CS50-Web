# Generated by Django 4.2.1 on 2023-07-05 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polly', '0008_archive'),
    ]

    operations = [
        migrations.AddField(
            model_name='survey',
            name='archived',
            field=models.BooleanField(default=False),
        ),
        migrations.DeleteModel(
            name='Archive',
        ),
    ]
