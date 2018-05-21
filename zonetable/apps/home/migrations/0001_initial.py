# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Language'
        db.create_table(u'home_language', (
            ('id_language', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('status', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('language', self.gf('django.db.models.fields.CharField')(max_length=45)),
        ))
        db.send_create_signal(u'home', ['Language'])

        # Adding model 'Country'
        db.create_table(u'home_country', (
            ('id_country', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('status', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=45)),
            ('fips104', self.gf('django.db.models.fields.CharField')(max_length=7)),
            ('iso2', self.gf('django.db.models.fields.CharField')(max_length=4)),
            ('iso3', self.gf('django.db.models.fields.CharField')(max_length=4)),
            ('ison', self.gf('django.db.models.fields.CharField')(max_length=4)),
            ('internet', self.gf('django.db.models.fields.CharField')(max_length=8)),
            ('capital', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('map_ref', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('nac_singular', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('nac_plural', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('currency', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('currency_code', self.gf('django.db.models.fields.CharField')(max_length=12)),
            ('population', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'home', ['Country'])

        # Adding model 'State'
        db.create_table(u'home_state', (
            ('id_state', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('status', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['home.Country'])),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=45)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=4)),
            ('adm1code', self.gf('django.db.models.fields.CharField')(max_length=8)),
        ))
        db.send_create_signal(u'home', ['State'])

        # Adding model 'City'
        db.create_table(u'home_city', (
            ('id_city', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('status', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['home.Country'])),
            ('state', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['home.State'])),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=45)),
            ('latitude', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('longitude', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('timezone', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('dmald', self.gf('django.db.models.fields.CharField')(max_length=5, null=True, blank=True)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=6, null=True, blank=True)),
        ))
        db.send_create_signal(u'home', ['City'])

        # Adding model 'Contact'
        db.create_table(u'home_contact', (
            ('id_contact', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('status', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=45)),
            ('email', self.gf('django.db.models.fields.CharField')(max_length=45)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=45, null=True)),
            ('language', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['home.Language'])),
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['home.Country'])),
            ('how_know', self.gf('django.db.models.fields.CharField')(max_length=45)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=45)),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('date_create', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'home', ['Contact'])

        # Adding model 'Content'
        db.create_table(u'home_content', (
            ('id_content', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('status', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=45)),
            ('content', self.gf('django.db.models.fields.TextField')(null=True)),
            ('url_name', self.gf('django.db.models.fields.CharField')(max_length=45)),
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['home.Country'])),
            ('language', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['home.Language'])),
            ('date_create', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'home', ['Content'])

        # Adding model 'Newsletter'
        db.create_table(u'home_newsletter', (
            ('id_newsletter', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('status', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('email', self.gf('django.db.models.fields.CharField')(max_length=45)),
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['home.Country'])),
            ('language', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['home.Language'])),
            ('date_create', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'home', ['Newsletter'])

        # Adding model 'Recommend'
        db.create_table(u'home_recommend', (
            ('id_recommend', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('status', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('name_remitter', self.gf('django.db.models.fields.CharField')(max_length=45)),
            ('email_remitter', self.gf('django.db.models.fields.CharField')(max_length=45)),
            ('name_receiver1', self.gf('django.db.models.fields.CharField')(max_length=45)),
            ('email_receiver1', self.gf('django.db.models.fields.CharField')(max_length=45)),
            ('name_receiver2', self.gf('django.db.models.fields.CharField')(max_length=45, null=True)),
            ('email_receiver2', self.gf('django.db.models.fields.CharField')(max_length=45, null=True)),
            ('name_receiver3', self.gf('django.db.models.fields.CharField')(max_length=45, null=True)),
            ('email_receiver3', self.gf('django.db.models.fields.CharField')(max_length=45, null=True)),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('language', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['home.Language'])),
            ('date_create', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'home', ['Recommend'])


    def backwards(self, orm):
        # Deleting model 'Language'
        db.delete_table(u'home_language')

        # Deleting model 'Country'
        db.delete_table(u'home_country')

        # Deleting model 'State'
        db.delete_table(u'home_state')

        # Deleting model 'City'
        db.delete_table(u'home_city')

        # Deleting model 'Contact'
        db.delete_table(u'home_contact')

        # Deleting model 'Content'
        db.delete_table(u'home_content')

        # Deleting model 'Newsletter'
        db.delete_table(u'home_newsletter')

        # Deleting model 'Recommend'
        db.delete_table(u'home_recommend')


    models = {
        u'home.city': {
            'Meta': {'object_name': 'City'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '6', 'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.Country']"}),
            'dmald': ('django.db.models.fields.CharField', [], {'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'id_city': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.State']"}),
            'status': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'timezone': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'})
        },
        u'home.contact': {
            'Meta': {'object_name': 'Contact'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.Country']"}),
            'date_create': ('django.db.models.fields.DateTimeField', [], {}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'how_know': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'id_contact': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.Language']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '45', 'null': 'True'}),
            'status': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '45'})
        },
        u'home.content': {
            'Meta': {'object_name': 'Content'},
            'content': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.Country']"}),
            'date_create': ('django.db.models.fields.DateTimeField', [], {}),
            'id_content': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.Language']"}),
            'status': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'url_name': ('django.db.models.fields.CharField', [], {'max_length': '45'})
        },
        u'home.country': {
            'Meta': {'object_name': 'Country'},
            'capital': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'currency': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'currency_code': ('django.db.models.fields.CharField', [], {'max_length': '12'}),
            'fips104': ('django.db.models.fields.CharField', [], {'max_length': '7'}),
            'id_country': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'internet': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'iso2': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'iso3': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'ison': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'map_ref': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'nac_plural': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'nac_singular': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'population': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'status': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'home.language': {
            'Meta': {'object_name': 'Language'},
            'id_language': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'status': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        u'home.newsletter': {
            'Meta': {'object_name': 'Newsletter'},
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.Country']"}),
            'date_create': ('django.db.models.fields.DateTimeField', [], {}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'id_newsletter': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.Language']"}),
            'status': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        u'home.recommend': {
            'Meta': {'object_name': 'Recommend'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'date_create': ('django.db.models.fields.DateTimeField', [], {}),
            'email_receiver1': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'email_receiver2': ('django.db.models.fields.CharField', [], {'max_length': '45', 'null': 'True'}),
            'email_receiver3': ('django.db.models.fields.CharField', [], {'max_length': '45', 'null': 'True'}),
            'email_remitter': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'id_recommend': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.Language']"}),
            'name_receiver1': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'name_receiver2': ('django.db.models.fields.CharField', [], {'max_length': '45', 'null': 'True'}),
            'name_receiver3': ('django.db.models.fields.CharField', [], {'max_length': '45', 'null': 'True'}),
            'name_remitter': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'status': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        u'home.state': {
            'Meta': {'object_name': 'State'},
            'adm1code': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.Country']"}),
            'id_state': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'status': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        }
    }

    complete_apps = ['home']