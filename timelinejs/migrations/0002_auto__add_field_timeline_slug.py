# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Timeline.slug'
        db.add_column('timelinejs_timeline', 'slug',
                      self.gf('django.db.models.fields.SlugField')(default='', max_length=50),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Timeline.slug'
        db.delete_column('timelinejs_timeline', 'slug')


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
            'slug': ('django.db.models.fields.SlugField', [], {'default': "''", 'max_length': '50'}),
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