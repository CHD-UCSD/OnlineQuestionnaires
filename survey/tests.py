"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.contrib.auth.models import User
from django.test import TestCase

import survey.survey_views
from survey.models import Question
from survey.models import Answer
from survey.models import Survey
from survey.models import Log
from survey.models import Page

class TestSurveyViews(TestCase):
    fixtures = ['db',]

    def test_get_qlist_new(self):
        # Activities survey pg 3, which conditionally asks cello questions
        page = Survey.objects.get(acronym='AQ').page_set.get(page_number=3)
        user = User.objects.get(username='howeik')

        expected = survey.survey_views.get_qlist(user, page)
        actual = survey.survey_views.get_qlist_new(user, page)

        self.assertSequenceEqual(actual, expected)