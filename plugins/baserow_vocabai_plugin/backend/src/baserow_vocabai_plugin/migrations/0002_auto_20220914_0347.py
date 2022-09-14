# Generated by Django 3.2.13 on 2022-09-14 03:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('baserow_vocabai_plugin', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='VocabAiUsage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('characters', models.IntegerField()),
                ('period', models.CharField(choices=[('MONTHLY', 'Monthly'), ('DAILY', 'Member')], default='DAILY', max_length=8)),
                ('period_time', models.IntegerField()),
                ('updated_time', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(help_text='The user for which this usage entry is for', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddIndex(
            model_name='vocabaiusage',
            index=models.Index(fields=['user', 'period', 'period_time'], name='baserow_voc_user_id_09df35_idx'),
        ),
        migrations.AddIndex(
            model_name='vocabaiusage',
            index=models.Index(fields=['updated_time'], name='baserow_voc_updated_99e346_idx'),
        ),
    ]
