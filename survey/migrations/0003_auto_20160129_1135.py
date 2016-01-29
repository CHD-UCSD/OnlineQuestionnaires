# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0002_auto_20150811_1421'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='condition_answers',
        ),
        migrations.RemoveField(
            model_name='question',
            name='condition_questions',
        ),
        migrations.AddField(
            model_name='question',
            name='condition_answer',
            field=models.ForeignKey(related_name='survey_question_condition', blank=True, to='survey.Answer', null=True),
        ),
        migrations.AddField(
            model_name='question',
            name='condition_question',
            field=models.ForeignKey(blank=True, to='survey.Question', null=True),
        ),
    ]
