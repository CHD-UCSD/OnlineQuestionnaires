# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'SubjectID'
        db.create_table(u'survey_subjectid', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('subjectid', self.gf('django.db.models.fields.CharField')(unique=True, max_length=5)),
        ))
        db.send_create_signal(u'survey', ['SubjectID'])

        # Adding model 'Survey'
        db.create_table(u'survey_survey', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('acronym', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('auto_number', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'survey', ['Survey'])

        # Adding model 'Record'
        db.create_table(u'survey_record', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('subjectid', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['survey.SubjectID'])),
        ))
        db.send_create_signal(u'survey', ['Record'])

        # Adding model 'Available_Survey'
        db.create_table(u'survey_available_survey', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('record', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['survey.Record'])),
            ('survey', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['survey.Survey'])),
            ('available', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'survey', ['Available_Survey'])

        # Adding unique constraint on 'Available_Survey', fields ['record', 'survey']
        db.create_unique(u'survey_available_survey', ['record_id', 'survey_id'])

        # Adding model 'Page'
        db.create_table(u'survey_page', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('survey', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['survey.Survey'])),
            ('page_number', self.gf('django.db.models.fields.IntegerField')()),
            ('page_title', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('page_subtitle', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('final_page', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'survey', ['Page'])

        # Adding model 'Question'
        db.create_table(u'survey_question', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('page', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['survey.Page'])),
            ('survey', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['survey.Survey'])),
            ('qtext', self.gf('django.db.models.fields.TextField')()),
            ('qnumber', self.gf('django.db.models.fields.IntegerField')()),
            ('conditions', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('condition_operator', self.gf('django.db.models.fields.CharField')(default='AND', max_length=3, blank=True)),
            ('newcolumn', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('required', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('trigger', self.gf('django.db.models.fields.related.ForeignKey')(related_name='trigger_question', null=True, to=orm['survey.Answer'])),
        ))
        db.send_create_signal(u'survey', ['Question'])

        # Adding model 'Answer'
        db.create_table(u'survey_answer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['survey.Question'])),
            ('atype', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('aformat', self.gf('django.db.models.fields.CharField')(max_length=2, blank=True)),
            ('atext', self.gf('django.db.models.fields.CharField')(max_length=250, blank=True)),
            ('range_min', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('range_max', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('pretext', self.gf('django.db.models.fields.CharField')(max_length=250, blank=True)),
            ('trigger', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['survey.Answer'], null=True, blank=True)),
            ('size', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'survey', ['Answer'])

        # Adding model 'Log'
        db.create_table(u'survey_log', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('subjectid', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['survey.SubjectID'])),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['survey.Question'])),
            ('response', self.gf('django.db.models.fields.CharField')(max_length=250, blank=True)),
            ('verbose_response', self.gf('django.db.models.fields.CharField')(max_length=400, blank=True)),
        ))
        db.send_create_signal(u'survey', ['Log'])

        # Adding unique constraint on 'Log', fields ['user', 'question']
        db.create_unique(u'survey_log', ['user', 'question_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'Log', fields ['user', 'question']
        db.delete_unique(u'survey_log', ['user', 'question_id'])

        # Removing unique constraint on 'Available_Survey', fields ['record', 'survey']
        db.delete_unique(u'survey_available_survey', ['record_id', 'survey_id'])

        # Deleting model 'SubjectID'
        db.delete_table(u'survey_subjectid')

        # Deleting model 'Survey'
        db.delete_table(u'survey_survey')

        # Deleting model 'Record'
        db.delete_table(u'survey_record')

        # Deleting model 'Available_Survey'
        db.delete_table(u'survey_available_survey')

        # Deleting model 'Page'
        db.delete_table(u'survey_page')

        # Deleting model 'Question'
        db.delete_table(u'survey_question')

        # Deleting model 'Answer'
        db.delete_table(u'survey_answer')

        # Deleting model 'Log'
        db.delete_table(u'survey_log')


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
            'page_title': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
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