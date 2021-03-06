# Generated by Django 2.2.6 on 2019-11-25 08:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tweet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=150)),
                ('created_at', models.DateTimeField()),
                ('tweet', models.TextField()),
                ('retweet_count', models.PositiveIntegerField()),
                ('location', models.CharField(max_length=150, null=True)),
            ],
            options={
                'verbose_name': 'Tweet',
                'verbose_name_plural': 'Tweets',
            },
        ),
    ]
