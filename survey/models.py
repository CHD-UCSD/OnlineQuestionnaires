from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

# User extension
class SubjectID(models.Model):
    user = models.OneToOneField(User)
    subjectid = models.CharField('Subject ID', max_length=5, unique=True)
    language = models.CharField("Subject's Preferred Language", max_length=20, choices=settings.LANGUAGES, default=settings.LANGUAGES[0][0])
    class Meta:
        ordering = ['subjectid']
    def __unicode__(self):
        return self.subjectid

# Survey object
class Survey(models.Model):
    title = models.CharField('Survey Title', max_length=200)
    acronym = models.CharField('Survey Acronym', max_length=20)
    auto_number = models.BooleanField('Dynamically create and present question numbers?', default=True)
    class Meta:
        ordering = ['title']
    def __unicode__(self):
        return self.title

# Record - needed to keep PI info separate from SubjectID in admin interface
class Record(models.Model):
    subjectid = models.ForeignKey(SubjectID)
    def __unicode__(self):
        return self.subjectid.subjectid

# To keep track of a survey's availability to individual users
class Available_Survey(models.Model):
    record = models.ForeignKey(Record)
    survey = models.ForeignKey(Survey)
    available = models.BooleanField('Is this survey available to this user?', default=True)
    class Meta:
        unique_together = ('record','survey')
    def __unicode__(self):
        return '%s - %s' %(self.record, self.survey.acronym)

# Page object
class Page(models.Model):
    survey = models.ForeignKey(Survey)
    page_number = models.IntegerField('Page Number')
    page_title = models.CharField('Page Title', max_length=50)
    page_subtitle = models.CharField('Page Subtitle', max_length=50, blank=True)
    final_page = models.BooleanField('Is this the final page?', default = False)
    class Meta:
        ordering = ['survey','page_number']
    def __unicode__(self):
        return u"%s Page %d: %s" %(self.survey.acronym, self.page_number, self.page_title)

# Question object
class Question(models.Model):
    page = models.ForeignKey(Page)
    survey = models.ForeignKey(Survey)
    qtext = models.TextField('Question Text')
    qnumber = models.IntegerField('Question Number', help_text='Needs to be an integer unique to this survey')
    conditions = models.CharField('Dependent Conditions', help_text='Takes a python dictionary, e.g. "{3:0, 4:2}".', max_length=100, blank=True)
    operators = (('AND','AND'),('OR','OR'))
    condition_operator = models.CharField('Conditional Operator', help_text='The logical statement used for multiple conditions', choices = operators, default='AND', blank=True, max_length=3)
    newcolumn = models.BooleanField('New Column', default=False)
    required = models.BooleanField('Response Required', default=False)
    trigger = models.ForeignKey("Answer", related_name='trigger_question', null=True)
    class Meta:
        unique_together = ('page','qnumber')
    class Meta:
        ordering = ['survey','qnumber']
    def __unicode__(self):
        if len(self.qtext)>50: qtext = self.qtext[:50]+'...'
        else: qtext = self.qtext
        return '%s %d. %s' %(self.survey.acronym, self.qnumber, qtext)

# Answer object 
class Answer(models.Model):
    question = models.ForeignKey(Question)
    atypes = (
        ('Fr','Free'),
        ('Ra','Radio'),
        ('Ch','Check'),
        ('Tx','Text'),
        ('Tf','TextField')
        )
    atype = models.CharField('Answer Type', max_length=10, choices=atypes)
    aformats = (
        ('Dt','Date'),
        ('Nm','Numerical'),
        ('In','Integer')
        )
    aformat = models.CharField('Answer Format', help_text='Applicable only for "Free" Answer Types', max_length=2, choices = aformats, blank=True)
    atext = models.CharField('Answer Text', help_text='Treated as posttext for "Free" Answer Types', max_length=250, blank=True)
    range_min = models.FloatField('Minimum Value', help_text='Applicable only for "Free" Answer Types', blank=True, null=True)
    range_max = models.FloatField('Maximum Value', help_text='Applicable only for "Free" Answer Types', blank=True, null=True)
    pretext = models.CharField('Text inserted above answer', max_length=250, blank=True)
    trigger = models.ForeignKey("self", verbose_name='Trigger Answer', help_text='The answer that triggers this answer to be shown', blank=True, null=True)
    size = models.IntegerField('Size of text box', help_text='Applicable only for "Free" Answer Types', blank=True, null=True)
    def __unicode__(self):
        if self.atext: return self.atext[:30]
        else: return 'Question %d: Answer ID %d' %(self.question.qnumber, self.pk)

# Log object
class Log(models.Model):
    user = models.CharField('User', max_length=50)
    subjectid = models.ForeignKey(SubjectID)
    question = models.ForeignKey(Question)
    response = models.CharField('Response', max_length=250, blank=True)
    verbose_response = models.CharField('Verbose Response', help_text='Human readable response to be used in output', max_length=400, blank=True)
    class Meta:
        unique_together = ('user','question')
    def __unicode__(self):
        return 'User: %s, Question: %s, Response: %s' %(self.user, self.question.qtext, self.response)
