# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Dimension'
        db.create_table(u'dataviewer_dimension', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('metadata', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('units', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('datatype', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('ts_column', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'dataviewer', ['Dimension'])

        # Adding model 'BaseTemplate'
        db.create_table(u'dataviewer_basetemplate', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('metadata', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'dataviewer', ['BaseTemplate'])

        # Adding M2M table for field dimensions on 'BaseTemplate'
        m2m_table_name = db.shorten_name(u'dataviewer_basetemplate_dimensions')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('basetemplate', models.ForeignKey(orm[u'dataviewer.basetemplate'], null=False)),
            ('dimension', models.ForeignKey(orm[u'dataviewer.dimension'], null=False))
        ))
        db.create_unique(m2m_table_name, ['basetemplate_id', 'dimension_id'])

        # Adding model 'Aggregator'
        db.create_table(u'dataviewer_aggregator', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('metadata', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('async_function', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('interval_in_seconds', self.gf('django.db.models.fields.IntegerField')(default=2)),
        ))
        db.send_create_signal(u'dataviewer', ['Aggregator'])

        # Adding model 'Calculator'
        db.create_table(u'dataviewer_calculator', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('metadata', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('async_function', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('output_dimension', self.gf('django.db.models.fields.related.ForeignKey')(related_name='output', to=orm['dataviewer.Dimension'])),
            ('custom_code', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'dataviewer', ['Calculator'])

        # Adding M2M table for field input_dimensions on 'Calculator'
        m2m_table_name = db.shorten_name(u'dataviewer_calculator_input_dimensions')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('calculator', models.ForeignKey(orm[u'dataviewer.calculator'], null=False)),
            ('dimension', models.ForeignKey(orm[u'dataviewer.dimension'], null=False))
        ))
        db.create_unique(m2m_table_name, ['calculator_id', 'dimension_id'])

        # Adding model 'Filter'
        db.create_table(u'dataviewer_filter', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('metadata', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('async_function', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'dataviewer', ['Filter'])

        # Adding M2M table for field input_dimensions on 'Filter'
        m2m_table_name = db.shorten_name(u'dataviewer_filter_input_dimensions')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('filter', models.ForeignKey(orm[u'dataviewer.filter'], null=False)),
            ('dimension', models.ForeignKey(orm[u'dataviewer.dimension'], null=False))
        ))
        db.create_unique(m2m_table_name, ['filter_id', 'dimension_id'])


    def backwards(self, orm):
        # Deleting model 'Dimension'
        db.delete_table(u'dataviewer_dimension')

        # Deleting model 'BaseTemplate'
        db.delete_table(u'dataviewer_basetemplate')

        # Removing M2M table for field dimensions on 'BaseTemplate'
        db.delete_table(db.shorten_name(u'dataviewer_basetemplate_dimensions'))

        # Deleting model 'Aggregator'
        db.delete_table(u'dataviewer_aggregator')

        # Deleting model 'Calculator'
        db.delete_table(u'dataviewer_calculator')

        # Removing M2M table for field input_dimensions on 'Calculator'
        db.delete_table(db.shorten_name(u'dataviewer_calculator_input_dimensions'))

        # Deleting model 'Filter'
        db.delete_table(u'dataviewer_filter')

        # Removing M2M table for field input_dimensions on 'Filter'
        db.delete_table(db.shorten_name(u'dataviewer_filter_input_dimensions'))


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
            'datatype': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
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