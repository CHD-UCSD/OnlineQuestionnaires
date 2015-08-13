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

    def test_get_qlist(self):
        for page in Survey.objects.get(acronym='AQ').page_set.all():
            print "Testing page: " + str(page.page_number)

            user = User.objects.get(username='howeik')

            expected = survey.survey_views.get_qlist_old(user, page)
            actual = survey.survey_views.get_qlist(user, page)

            self.assertSequenceEqual(actual, expected)
