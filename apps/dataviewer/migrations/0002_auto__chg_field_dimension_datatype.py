# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Dimension.datatype'
        db.alter_column(u'dataviewer_dimension', 'datatype', self.gf('django.db.models.fields.CharField')(max_length=10))

    def backwards(self, orm):

        # Changing field 'Dimension.datatype'
        db.alter_column(u'dataviewer_dimension', 'datatype', self.gf('django.db.models.fields.CharField')(max_length=5))

    models = {
        u'dataviewer.aggregator': {
            'Meta': {'object_name': 'Aggregator'},
            'async_function': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interval_in_seconds': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'metadata': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'dataviewer.basetemplate': {
            'Meta': {'object_name': 'BaseTemplate'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'dimensions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['dataviewer.Dimension']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'metadata': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'dataviewer.calculator': {
            'Meta': {'object_name': 'Calculator'},
            'async_function': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'custom_code': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'input_dimensions': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'inputs'", 'symmetrical': 'False', 'to': u"orm['dataviewer.Dimension']"}),
            'metadata': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'output_dimension': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'output'", 'to': u"orm['dataviewer.Dimension']"})
        },
        u'dataviewer.dimension': {
            'Meta': {'object_name': 'Dimension'},
            'datatype': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'metadata': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'ts_column': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'units': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        u'dataviewer.filter': {
            'Meta': {'object_name': 'Filter'},
            'async_function': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'input_dimensions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['dataviewer.Dimension']", 'symmetrical': 'False'}),
            'metadata': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['dataviewer']