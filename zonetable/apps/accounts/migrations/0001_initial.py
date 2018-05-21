# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'UserProfile'
        db.create_table(u'accounts_userprofile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], unique=True)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=45, null=True, blank=True)),
            ('birth_day', self.gf('django.db.models.fields.CharField')(max_length=2, null=True, blank=True)),
            ('birth_month', self.gf('django.db.models.fields.CharField')(max_length=2, null=True, blank=True)),
            ('birth_year', self.gf('django.db.models.fields.CharField')(max_length=4, null=True, blank=True)),
            ('state', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['home.State'])),
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['home.Country'])),
            ('language', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['home.Language'])),
            ('random', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('user_status', self.gf('django.db.models.fields.BooleanField')(default=False, max_length=1)),
            ('fb_id', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('fb_verify', self.gf('django.db.models.fields.BooleanField')(default=False, max_length=1)),
            ('gender', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('locale', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('birthday', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('newsletter', self.gf('django.db.models.fields.BooleanField')(default=True, max_length=1)),
            ('terms_conditions', self.gf('django.db.models.fields.BooleanField')(default=False, max_length=1)),
            ('referer', self.gf('django.db.models.fields.IntegerField')(max_length=11, null=True, blank=True)),
        ))
        db.send_create_signal(u'accounts', ['UserProfile'])

        # Adding M2M table for field category on 'UserProfile'
        m2m_table_name = db.shorten_name(u'accounts_userprofile_category')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('userprofile', models.ForeignKey(orm[u'accounts.userprofile'], null=False)),
            ('category', models.ForeignKey(orm[u'directory.category'], null=False))
        ))
        db.create_unique(m2m_table_name, ['userprofile_id', 'category_id'])

        # Adding model 'Recommendation'
        db.create_table(u'accounts_recommendation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('status', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=50)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'accounts', ['Recommendation'])


    def backwards(self, orm):
        # Deleting model 'UserProfile'
        db.delete_table(u'accounts_userprofile')

        # Removing M2M table for field category on 'UserProfile'
        db.delete_table(db.shorten_name(u'accounts_userprofile_category'))

        # Deleting model 'Recommendation'
        db.delete_table(u'accounts_recommendation')


    models = {
        u'accounts.recommendation': {
            'Meta': {'object_name': 'Recommendation'},
            'date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'status': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'})
        },
        u'accounts.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'birth_day': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'birth_month': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'birth_year': ('django.db.models.fields.CharField', [], {'max_length': '4', 'null': 'True', 'blank': 'True'}),
            'birthday': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'category': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['directory.Category']", 'symmetrical': 'False'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.Country']"}),
            'fb_id': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'fb_verify': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'max_length': '1'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.Language']"}),
            'locale': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'newsletter': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'max_length': '1'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '45', 'null': 'True', 'blank': 'True'}),
            'random': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'referer': ('django.db.models.fields.IntegerField', [], {'max_length': '11', 'null': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.State']"}),
            'terms_conditions': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'max_length': '1'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'unique': 'True'}),
            'user_status': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'max_length': '1'})
        },
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
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'directory.category': {
            'Meta': {'object_name': 'Category'},
            'id_category': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'url_name': ('django.db.models.fields.SlugField', [], {'max_length': '100'})
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

    complete_apps = ['accounts']