# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'ShortURL'
        db.create_table('urlshortener_shorturl', (
            ('id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=2048)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('urlshortener', ['ShortURL'])


    def backwards(self, orm):
        
        # Deleting model 'ShortURL'
        db.delete_table('urlshortener_shorturl')


    models = {
        'urlshortener.shorturl': {
            'Meta': {'object_name': 'ShortURL'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '2048'})
        }
    }

    complete_apps = ['urlshortener']
