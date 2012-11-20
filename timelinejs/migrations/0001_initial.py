# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Asset'
        db.create_table('timelinejs_asset', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('media', self.gf('django.db.models.fields.TextField')()),
            ('credit', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('caption', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
        ))
        db.send_create_signal('timelinejs', ['Asset'])

        # Adding model 'Timeline'
        db.create_table('timelinejs_timeline', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('headline', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('start_date', self.gf('django.db.models.fields.DateField')()),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('asset', self.gf('django.db.models.fields.related.ForeignKey')(related_name='timelines', to=orm['timelinejs.Asset'])),
        ))
        db.send_create_signal('timelinejs', ['Timeline'])

        # Adding model 'TimelineEntry'
        db.create_table('timelinejs_timelineentry', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('timeline', self.gf('django.db.models.fields.related.ForeignKey')(related_name='entries', to=orm['timelinejs.Timeline'])),
            ('start_date', self.gf('django.db.models.fields.DateField')()),
            ('headline', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('asset', self.gf('django.db.models.fields.related.ForeignKey')(related_name='timeline_entries', to=orm['timelinejs.Asset'])),
        ))
        db.send_create_signal('timelinejs', ['TimelineEntry'])


    def backwards(self, orm):
        # Deleting model 'Asset'
        db.delete_table('timelinejs_asset')

        # Deleting model 'Timeline'
        db.delete_table('timelinejs_timeline')

        # Deleting model 'TimelineEntry'
        db.delete_table('timelinejs_timelineentry')


    models = {
        'timelinejs.asset': {
            'Meta': {'object_name': 'Asset'},
            'caption': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'credit': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'media': ('django.db.models.fields.TextField', [], {})
        },
        'timelinejs.timeline': {
            'Meta': {'object_name': 'Timeline'},
            'asset': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'timelines'", 'to': "orm['timelinejs.Asset']"}),
            'headline': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'start_date': ('django.db.models.fields.DateField', [], {}),
            'text': ('django.db.models.fields.TextField', [], {})
        },
        'timelinejs.timelineentry': {
            'Meta': {'object_name': 'TimelineEntry'},
            'asset': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'timeline_entries'", 'to': "orm['timelinejs.Asset']"}),
            'headline': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'start_date': ('django.db.models.fields.DateField', [], {}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'timeline': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'entries'", 'to': "orm['timelinejs.Timeline']"})
        }
    }

    complete_apps = ['timelinejs']