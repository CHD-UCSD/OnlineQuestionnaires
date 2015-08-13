# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def partition(l, p):
    return reduce(lambda x, y: x[not p(y)].append(y) or x, l, ([], []))

def update_conditions(apps, schema_editor):
    Question = apps.get_model('survey', 'Question')
    Answer = apps.get_model('survey', 'Answer')

    questions = (q for q in Question.objects.all() if q.conditions)
    for q in questions:
        condition_questions, condition_answers = partition(
            eval(q.conditions).iteritems(), 
            lambda (_, required_answers): required_answers == 'any'
        )

        q.condition_questions.add(*{
            Question.objects.get(survey=q.survey, qnumber=qnumber)
            for (qnumber, _) in condition_questions
        })

        # sometimes, answers are specified as an id; other times, [id]
        # this turns the answers specified as an id to [id]
        condition_answers = [
            (_, [answers]) if type(answers) is int else (_, answers)
            for (_, answers) in condition_answers
        ]

        q.condition_answers.add(*{
            Question.objects.get(
                survey=q.survey, 
                qnumber=qnumber
            ).answer_set.all()[answer]
            for (qnumber, answers) in condition_answers
            for answer in answers
        })

        q.save()

class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0002_auto_20150811_1421'),
    ]

    operations = [
        migrations.RunPython(update_conditions),
    ]
