# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Question.qtext_en'
        db.add_column(u'survey_question', 'qtext_en',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Question.qtext_es'
        db.add_column(u'survey_question', 'qtext_es',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Answer.atext_en'
        db.add_column(u'survey_answer', 'atext_en',
                      self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Answer.atext_es'
        db.add_column(u'survey_answer', 'atext_es',
                      self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Page.page_title_en'
        db.add_column(u'survey_page', 'page_title_en',
                      self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Page.page_title_es'
        db.add_column(u'survey_page', 'page_title_es',
                      self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Page.page_subtitle_en'
        db.add_column(u'survey_page', 'page_subtitle_en',
                      self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Page.page_subtitle_es'
        db.add_column(u'survey_page', 'page_subtitle_es',
                      self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True),
                      keep_default=False)

        # Adding field 'SubjectID.language'
        db.add_column(u'survey_subjectid', 'language',
                      self.gf('django.db.models.fields.CharField')(default='en', max_length=20),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Question.qtext_en'
        db.delete_column(u'survey_question', 'qtext_en')

        # Deleting field 'Question.qtext_es'
        db.delete_column(u'survey_question', 'qtext_es')

        # Deleting field 'Answer.atext_en'
        db.delete_column(u'survey_answer', 'atext_en')

        # Deleting field 'Answer.atext_es'
        db.delete_column(u'survey_answer', 'atext_es')

        # Deleting field 'Page.page_title_en'
        db.delete_column(u'survey_page', 'page_title_en')

        # Deleting field 'Page.page_title_es'
        db.delete_column(u'survey_page', 'page_title_es')

        # Deleting field 'Page.page_subtitle_en'
        db.delete_column(u'survey_page', 'page_subtitle_en')

        # Deleting field 'Page.page_subtitle_es'
        db.delete_column(u'survey_page', 'page_subtitle_es')

        # Deleting field 'SubjectID.language'
        db.delete_column(u'survey_subjectid', 'language')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'survey.answer': {
            'Meta': {'object_name': 'Answer'},
            'aformat': ('django.db.models.fields.CharField', [], {'max_length': '2', 'blank': 'True'}),
            'atext': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'atext_en': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'atext_es': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'atype': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pretext': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['survey.Question']"}),
            'range_max': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'range_min': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'size': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'trigger': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['survey.Answer']", 'null': 'True', 'blank': 'True'})
        },
        u'survey.available_survey': {
            'Meta': {'unique_together': "(('record', 'survey'),)", 'object_name': 'Available_Survey'},
            'available': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'record': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['survey.Record']"}),
            'survey': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['survey.Survey']"})
        },
        u'survey.log': {
            'Meta': {'unique_together': "(('user', 'question'),)", 'object_name': 'Log'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['survey.Question']"}),
            'response': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'subjectid': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['survey.SubjectID']"}),
            'user': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'verbose_response': ('django.db.models.fields.CharField', [], {'max_length': '400', 'blank': 'True'})
        },
        u'survey.page': {
            'Meta': {'ordering': "['survey', 'page_number']", 'object_name': 'Page'},
            'final_page': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'page_number': ('django.db.models.fields.IntegerField', [], {}),
            'page_subtitle': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'page_subtitle_en': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'page_subtitle_es': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'page_title': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'page_title_en': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'page_title_es': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'survey': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['survey.Survey']"})
        },
        u'survey.question': {
            'Meta': {'ordering': "['survey', 'qnumber']", 'object_name': 'Question'},
            'condition_operator': ('django.db.models.fields.CharField', [], {'default': "'AND'", 'max_length': '3', 'blank': 'True'}),
            'conditions': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'newcolumn': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'page': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['survey.Page']"}),
            'qnumber': ('django.db.models.fields.IntegerField', [], {}),
            'qtext': ('django.db.models.fields.TextField', [], {}),
            'qtext_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'qtext_es': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'survey': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['survey.Survey']"}),
            'trigger': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'trigger_question'", 'null': 'True', 'to': u"orm['survey.Answer']"})
        },
        u'survey.record': {
            'Meta': {'object_name': 'Record'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'subjectid': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['survey.SubjectID']"})
        },
        u'survey.subjectid': {
            'Meta': {'ordering': "['subjectid']", 'object_name': 'SubjectID'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'default': "'en'", 'max_length': '20'}),
            'subjectid': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '5'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        },
        u'survey.survey': {
            'Meta': {'ordering': "['title']", 'object_name': 'Survey'},
            'acronym': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'auto_number': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['survey']