# Generated by Django 4.2.1 on 2023-07-04 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polly', '0003_vote'),
    ]

    operations = [
        migrations.AddField(
            model_name='vote',
            name='answer',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]
