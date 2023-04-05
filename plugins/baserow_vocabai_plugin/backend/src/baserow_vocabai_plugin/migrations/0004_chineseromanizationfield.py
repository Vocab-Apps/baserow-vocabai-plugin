# Generated by Django 3.2.13 on 2023-01-20 12:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0093_add_auto_number_to_webhook_log'),
        ('baserow_vocabai_plugin', '0003_vocabailanguagedata'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChineseRomanizationField',
            fields=[
                ('field_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='database.field')),
                ('transformation', models.CharField(choices=[('pinyin', 'Pinyin'), ('jyutping', 'Jyutping')], default='pinyin', help_text='Pinyin or Jyutping', max_length=64)),
                ('tone_numbers', models.BooleanField(default=False, help_text='Whether to use tone numbers in pinyin/jyutping')),
                ('spaces', models.BooleanField(default=False, help_text='Whether to use space between each syllable')),
                ('correction_table', models.ForeignKey(blank=True, help_text='The correction table for pinyin/jyutping', null=True, on_delete=django.db.models.deletion.CASCADE, to='database.table')),
                ('source_field', models.ForeignKey(blank=True, help_text='The field to transliterate.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='baserow_vocabai_plugin.languagefield')),
            ],
            options={
                'abstract': False,
            },
            bases=('database.field',),
        ),
    ]