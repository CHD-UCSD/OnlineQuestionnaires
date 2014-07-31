# Create your views here.
from django.http import HttpResponseRedirect
from django.views import generic
from django.shortcuts import render, get_object_or_404, render_to_response
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from survey.survey_forms import AuthenticationFormWithInactiveUsersOkay
from survey.models import Question, Answer, Survey, Page, Log

def logout_page(request):
	"""
	Log users out and redirect to main page
	"""
	logout(request)
	return HttpResponseRedirect(reverse('survey:index'))