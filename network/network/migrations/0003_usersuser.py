# Generated by Django 4.2.1 on 2023-06-23 11:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0002_post'),
    ]

    operations = [
        migrations.CreateModel(
            name='UsersUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('followers', models.IntegerField(default=0)),
                ('following', models.IntegerField(default=0)),
                ('posts', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_posts', to='network.post')),
                ('user', models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
