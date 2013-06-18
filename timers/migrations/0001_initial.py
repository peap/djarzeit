# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Category'
        db.create_table('timers_category', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['timers.Category'], blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.CharField')(null=True, blank=True, max_length=1000)),
        ))
        db.send_create_signal('timers', ['Category'])

        # Adding model 'Timer'
        db.create_table('timers_timer', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['timers.Category'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.CharField')(null=True, blank=True, max_length=1000)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('timers', ['Timer'])

        # Adding model 'Interval'
        db.create_table('timers_interval', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('timer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['timers.Timer'])),
            ('week', self.gf('django.db.models.fields.IntegerField')(db_index=True)),
            ('year', self.gf('django.db.models.fields.IntegerField')(db_index=True)),
            ('start', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('end', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('notes', self.gf('django.db.models.fields.CharField')(null=True, blank=True, max_length=1000)),
        ))
        db.send_create_signal('timers', ['Interval'])

        # Adding M2M table for field tags on 'Interval'
        m2m_table_name = db.shorten_name('timers_interval_tags')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('interval', models.ForeignKey(orm['timers.interval'], null=False)),
            ('tags', models.ForeignKey(orm['timers.tags'], null=False))
        ))
        db.create_unique(m2m_table_name, ['interval_id', 'tags_id'])

        # Adding model 'Tags'
        db.create_table('timers_tags', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('description', self.gf('django.db.models.fields.CharField')(null=True, blank=True, max_length=1000)),
        ))
        db.send_create_signal('timers', ['Tags'])


    def backwards(self, orm):
        # Deleting model 'Category'
        db.delete_table('timers_category')

        # Deleting model 'Timer'
        db.delete_table('timers_timer')

        # Deleting model 'Interval'
        db.delete_table('timers_interval')

        # Removing M2M table for field tags on 'Interval'
        db.delete_table(db.shorten_name('timers_interval_tags'))

        # Deleting model 'Tags'
        db.delete_table('timers_tags')


    models = {
        'timers.category': {
            'Meta': {'object_name': 'Category'},
            'description': ('django.db.models.fields.CharField', [], {'null': 'True', 'blank': 'True', 'max_length': '1000'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'to': "orm['timers.Category']", 'blank': 'True'})
        },
        'timers.interval': {
            'Meta': {'object_name': 'Interval'},
            'end': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('django.db.models.fields.CharField', [], {'null': 'True', 'blank': 'True', 'max_length': '1000'}),
            'start': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'null': 'True', 'to': "orm['timers.Tags']", 'symmetrical': 'False', 'db_index': 'True', 'blank': 'True'}),
            'timer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['timers.Timer']"}),
            'week': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'year': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'})
        },
        'timers.tags': {
            'Meta': {'object_name': 'Tags'},
            'description': ('django.db.models.fields.CharField', [], {'null': 'True', 'blank': 'True', 'max_length': '1000'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '25'})
        },
        'timers.timer': {
            'Meta': {'object_name': 'Timer'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['timers.Category']"}),
            'description': ('django.db.models.fields.CharField', [], {'null': 'True', 'blank': 'True', 'max_length': '1000'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['timers']