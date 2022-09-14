from django.db import models

from baserow.contrib.database.fields.models import Field

# migrations
# docker container exec baserow-vocabai-plugin /baserow.sh backend-cmd manage makemigrations baserow_vocabai_plugin
# docker container exec baserow-vocabai-plugin /baserow.sh backend-cmd manage migrate baserow_vocabai_plugin

# undoing a migration:
# docker container exec baserow-vocabai-plugin /baserow.sh backend-cmd manage migrate baserow_vocabai_plugin 0001

class LanguageField(Field):
    language = models.CharField(
        max_length=255,
        blank=True,
        default="",
        help_text="Language",
    )    


class TranslationField(Field):
    source_field = models.ForeignKey(
        LanguageField,
        on_delete=models.CASCADE,
        help_text="The field to translate.",
        null=True,
        blank=True,
        related_name='+'
    )    
    target_language = models.CharField(
        max_length=255,
        blank=True,
        default="",
        help_text="Target Language",
    )        
    service = models.CharField(
        max_length=255,
        blank=True,
        default="",
        help_text="Translation Service",
    )            

class TransliterationField(Field):
    source_field = models.ForeignKey(
        LanguageField,
        on_delete=models.CASCADE,
        help_text="The field to transliterate.",
        null=True,
        blank=True,
        related_name='+'
    )    
    transliteration_id = models.CharField(
        max_length=2048,
        blank=True,
        default="",
        help_text="Transliteration key for this service",
    )        

class DictionaryLookupField(Field):
    source_field = models.ForeignKey(
        LanguageField,
        on_delete=models.CASCADE,
        help_text="The field to do dictionary lookup for.",
        null=True,
        blank=True,
        related_name='+'
    )    
    lookup_id = models.CharField(
        max_length=2048,
        blank=True,
        default="",
        help_text="Dictionary lookup key for this service",
    )            

from django.contrib.auth import get_user_model
User = get_user_model()

# usage tracking
# ==============

USAGE_PERIOD_MONTHLY = "MONTHLY"
USAGE_PERIOD_DAILY = "DAILY"
USAGE_PERIOD_CHOICES = (
    (USAGE_PERIOD_MONTHLY, "Monthly"),
    (USAGE_PERIOD_DAILY, "Member"),
)

class VocabAiUsage(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        help_text="The user for which this usage entry is for",
    )
    
    # character usage
    characters = models.IntegerField()

    # indicate daily or monthly
    period = models.CharField(
        default=USAGE_PERIOD_DAILY,
        max_length=8,
        choices=USAGE_PERIOD_CHOICES
    )    

    # will contain 202209 or 20220914
    period_time = models.IntegerField()

    # keep track of when this record was modified
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['user', 'period', 'period_time']),
            models.Index(fields=['updated_time']),
        ]