# Generated by Django 4.2.1 on 2023-07-03 11:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polly', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Survey',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.TextField()),
                ('answer1', models.TextField()),
                ('answer2', models.TextField()),
                ('answer3', models.TextField(blank=True)),
                ('answer4', models.TextField(blank=True)),
                ('timestamp', models.DateTimeField()),
                ('user', models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, related_name='author', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]