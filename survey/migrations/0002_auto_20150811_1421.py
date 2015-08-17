# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='condition_answers',
            field=models.ManyToManyField(related_name='survey_question_condition', to='survey.Answer', blank=True),
        ),
        migrations.AddField(
            model_name='question',
            name='condition_questions',
            field=models.ManyToManyField(to='survey.Question', blank=True),
        ),
    ]
