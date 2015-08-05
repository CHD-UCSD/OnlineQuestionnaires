# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('atype', models.CharField(max_length=10, verbose_name=b'Answer Type', choices=[(b'Fr', b'Free'), (b'Ra', b'Radio'), (b'Ch', b'Check'), (b'Tx', b'Text'), (b'Tf', b'TextField')])),
                ('aformat', models.CharField(blank=True, help_text=b'Applicable only for "Free" Answer Types', max_length=2, verbose_name=b'Answer Format', choices=[(b'Dt', b'Date'), (b'Nm', b'Numerical'), (b'In', b'Integer')])),
                ('atext', models.CharField(help_text=b'Treated as posttext for "Free" Answer Types', max_length=250, verbose_name=b'Answer Text', blank=True)),
                ('atext_en', models.CharField(help_text=b'Treated as posttext for "Free" Answer Types', max_length=250, null=True, verbose_name=b'Answer Text', blank=True)),
                ('atext_es', models.CharField(help_text=b'Treated as posttext for "Free" Answer Types', max_length=250, null=True, verbose_name=b'Answer Text', blank=True)),
                ('range_min', models.FloatField(help_text=b'Applicable only for "Free" Answer Types', null=True, verbose_name=b'Minimum Value', blank=True)),
                ('range_max', models.FloatField(help_text=b'Applicable only for "Free" Answer Types', null=True, verbose_name=b'Maximum Value', blank=True)),
                ('pretext', models.CharField(max_length=250, verbose_name=b'Text inserted above answer', blank=True)),
                ('pretext_en', models.CharField(max_length=250, null=True, verbose_name=b'Text inserted above answer', blank=True)),
                ('pretext_es', models.CharField(max_length=250, null=True, verbose_name=b'Text inserted above answer', blank=True)),
                ('size', models.IntegerField(help_text=b'Applicable only for "Free" Answer Types', null=True, verbose_name=b'Size of text box', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Available_Survey',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('available', models.BooleanField(default=True, verbose_name=b'Is this survey available to this user?')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user', models.CharField(max_length=50, verbose_name=b'User')),
                ('response', models.CharField(max_length=250, verbose_name=b'Response', blank=True)),
                ('verbose_response', models.CharField(help_text=b'Human readable response to be used in output', max_length=400, verbose_name=b'Verbose Response', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('page_number', models.IntegerField(verbose_name=b'Page Number')),
                ('page_title', models.CharField(max_length=50, verbose_name=b'Page Title')),
                ('page_title_en', models.CharField(max_length=50, null=True, verbose_name=b'Page Title')),
                ('page_title_es', models.CharField(max_length=50, null=True, verbose_name=b'Page Title')),
                ('page_subtitle', models.CharField(max_length=50, verbose_name=b'Page Subtitle', blank=True)),
                ('page_subtitle_en', models.CharField(max_length=50, null=True, verbose_name=b'Page Subtitle', blank=True)),
                ('page_subtitle_es', models.CharField(max_length=50, null=True, verbose_name=b'Page Subtitle', blank=True)),
                ('final_page', models.BooleanField(default=False, verbose_name=b'Is this the final page?')),
            ],
            options={
                'ordering': ['survey', 'page_number'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('qtext', models.TextField(verbose_name=b'Question Text')),
                ('qtext_en', models.TextField(null=True, verbose_name=b'Question Text')),
                ('qtext_es', models.TextField(null=True, verbose_name=b'Question Text')),
                ('qnumber', models.IntegerField(help_text=b'Needs to be an integer unique to this survey', verbose_name=b'Question Number')),
                ('conditions', models.CharField(help_text=b'Takes a python dictionary, e.g. "{3:0, 4:2}".', max_length=100, verbose_name=b'Dependent Conditions', blank=True)),
                ('condition_operator', models.CharField(default=b'AND', choices=[(b'AND', b'AND'), (b'OR', b'OR')], max_length=3, blank=True, help_text=b'The logical statement used for multiple conditions', verbose_name=b'Conditional Operator')),
                ('newcolumn', models.BooleanField(default=False, verbose_name=b'New Column')),
                ('required', models.BooleanField(default=False, verbose_name=b'Response Required')),
                ('page', models.ForeignKey(to='survey.Page')),
            ],
            options={
                'ordering': ['survey', 'qnumber'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SubjectID',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('subjectid', models.CharField(unique=True, max_length=5, verbose_name=b'Subject ID')),
                ('language', models.CharField(default=b'en', max_length=20, verbose_name=b"Subject's Preferred Language", choices=[(b'en', b'English'), (b'es', b'Spanish')])),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['subjectid'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Survey',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200, verbose_name=b'Survey Title')),
                ('acronym', models.CharField(max_length=20, verbose_name=b'Survey Acronym')),
                ('auto_number', models.BooleanField(default=True, verbose_name=b'Dynamically create and present question numbers?')),
            ],
            options={
                'ordering': ['title'],
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='record',
            name='subjectid',
            field=models.ForeignKey(to='survey.SubjectID'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='question',
            name='survey',
            field=models.ForeignKey(to='survey.Survey'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='question',
            name='trigger',
            field=models.ForeignKey(related_name=b'trigger_question', to='survey.Answer', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='page',
            name='survey',
            field=models.ForeignKey(to='survey.Survey'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='log',
            name='question',
            field=models.ForeignKey(to='survey.Question'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='log',
            name='subjectid',
            field=models.ForeignKey(to='survey.SubjectID'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='log',
            unique_together=set([('user', 'question')]),
        ),
        migrations.AddField(
            model_name='available_survey',
            name='record',
            field=models.ForeignKey(to='survey.Record'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='available_survey',
            name='survey',
            field=models.ForeignKey(to='survey.Survey'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='available_survey',
            unique_together=set([('record', 'survey')]),
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(to='survey.Question'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='answer',
            name='trigger',
            field=models.ForeignKey(blank=True, to='survey.Answer', help_text=b'The answer that triggers this answer to be shown', null=True, verbose_name=b'Trigger Answer'),
            preserve_default=True,
        ),
    ]
