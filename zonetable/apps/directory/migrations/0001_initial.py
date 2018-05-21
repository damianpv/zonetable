# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Category'
        db.create_table(u'directory_category', (
            ('id_category', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('status', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('url_name', self.gf('django.db.models.fields.SlugField')(max_length=100)),
        ))
        db.send_create_signal(u'directory', ['Category'])

        # Adding model 'Service'
        db.create_table(u'directory_service', (
            ('id_service', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('status', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'directory', ['Service'])

        # Adding model 'Payment'
        db.create_table(u'directory_payment', (
            ('id_service', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('status', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('initials', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('pay_in_gm', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'directory', ['Payment'])

        # Adding model 'Currency'
        db.create_table(u'directory_currency', (
            ('id_currency', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('status', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'directory', ['Currency'])

        # Adding model 'Style'
        db.create_table(u'directory_style', (
            ('id_style', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('status', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'directory', ['Style'])

        # Adding model 'Directory'
        db.create_table(u'directory_directory', (
            ('id_directory', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('status', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('postal_code', self.gf('django.db.models.fields.CharField')(max_length=5, null=True, blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('state', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['home.State'])),
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['home.Country'])),
            ('language', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['home.Language'])),
            ('currency', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['directory.Currency'])),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=45, null=True)),
            ('cell', self.gf('django.db.models.fields.CharField')(max_length=45, null=True, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=100, null=True, blank=True)),
            ('email_user', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('website', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('keywords', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('content', self.gf('django.db.models.fields.TextField')(null=True)),
            ('comment', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('logo', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('geo_location', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('twitter', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('facebook', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('google_plus', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('url_name', self.gf('django.db.models.fields.SlugField')(max_length=255, null=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('date_create', self.gf('django.db.models.fields.DateTimeField')()),
            ('date_update', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'directory', ['Directory'])

        # Adding M2M table for field category on 'Directory'
        m2m_table_name = db.shorten_name(u'directory_directory_category')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('directory', models.ForeignKey(orm[u'directory.directory'], null=False)),
            ('category', models.ForeignKey(orm[u'directory.category'], null=False))
        ))
        db.create_unique(m2m_table_name, ['directory_id', 'category_id'])

        # Adding M2M table for field service on 'Directory'
        m2m_table_name = db.shorten_name(u'directory_directory_service')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('directory', models.ForeignKey(orm[u'directory.directory'], null=False)),
            ('service', models.ForeignKey(orm[u'directory.service'], null=False))
        ))
        db.create_unique(m2m_table_name, ['directory_id', 'service_id'])

        # Adding M2M table for field payment on 'Directory'
        m2m_table_name = db.shorten_name(u'directory_directory_payment')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('directory', models.ForeignKey(orm[u'directory.directory'], null=False)),
            ('payment', models.ForeignKey(orm[u'directory.payment'], null=False))
        ))
        db.create_unique(m2m_table_name, ['directory_id', 'payment_id'])

        # Adding M2M table for field style on 'Directory'
        m2m_table_name = db.shorten_name(u'directory_directory_style')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('directory', models.ForeignKey(orm[u'directory.directory'], null=False)),
            ('style', models.ForeignKey(orm[u'directory.style'], null=False))
        ))
        db.create_unique(m2m_table_name, ['directory_id', 'style_id'])

        # Adding model 'Hours'
        db.create_table(u'directory_hours', (
            ('id_hours', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('status', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('directory', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['directory.Directory'])),
            ('day_week', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('hour_in', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('hour_out', self.gf('django.db.models.fields.CharField')(max_length=5)),
        ))
        db.send_create_signal(u'directory', ['Hours'])

        # Adding model 'Stat'
        db.create_table(u'directory_stat', (
            ('id_stat', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('directory', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['directory.Directory'])),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('count', self.gf('django.db.models.fields.CharField')(max_length=10)),
        ))
        db.send_create_signal(u'directory', ['Stat'])

        # Adding model 'Reserve'
        db.create_table(u'directory_reserve', (
            ('id_reserve', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('status', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('type', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('directory', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['directory.Directory'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=100, null=True, blank=True)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('people', self.gf('django.db.models.fields.IntegerField')(max_length=2)),
            ('date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('time', self.gf('django.db.models.fields.TimeField')(null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('score', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=8, decimal_places=2, blank=True)),
            ('point', self.gf('django.db.models.fields.IntegerField')(max_length=4, null=True, blank=True)),
            ('date_create', self.gf('django.db.models.fields.DateTimeField')()),
            ('date_update', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'directory', ['Reserve'])

        # Adding model 'Comment'
        db.create_table(u'directory_comment', (
            ('id_comment', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('status', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('directory', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['directory.Directory'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=100)),
            ('comment', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('date_create', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'directory', ['Comment'])

        # Adding model 'Rate'
        db.create_table(u'directory_rate', (
            ('id_rate', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('directory', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['directory.Directory'])),
            ('value', self.gf('django.db.models.fields.IntegerField')(max_length=1)),
            ('date_create', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'directory', ['Rate'])

        # Adding model 'Package'
        db.create_table(u'directory_package', (
            ('id_package', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('status', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('price', self.gf('django.db.models.fields.DecimalField')(max_digits=5, decimal_places=2)),
            ('order', self.gf('django.db.models.fields.IntegerField')(default=0, max_length=2)),
            ('date_create', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'directory', ['Package'])

        # Adding model 'Pay'
        db.create_table(u'directory_pay', (
            ('id_pay', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('payment', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['directory.Payment'])),
            ('directory', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['directory.Directory'], null=True, blank=True)),
            ('pay_status', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('txn_id', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('receiver_id', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('subtotal', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('pay_months', self.gf('django.db.models.fields.IntegerField')(max_length=5)),
            ('price', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('concept', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('date_create', self.gf('django.db.models.fields.DateTimeField')()),
            ('date_begin', self.gf('django.db.models.fields.DateTimeField')()),
            ('date_end', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'directory', ['Pay'])

        # Adding M2M table for field package on 'Pay'
        m2m_table_name = db.shorten_name(u'directory_pay_package')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('pay', models.ForeignKey(orm[u'directory.pay'], null=False)),
            ('package', models.ForeignKey(orm[u'directory.package'], null=False))
        ))
        db.create_unique(m2m_table_name, ['pay_id', 'package_id'])


    def backwards(self, orm):
        # Deleting model 'Category'
        db.delete_table(u'directory_category')

        # Deleting model 'Service'
        db.delete_table(u'directory_service')

        # Deleting model 'Payment'
        db.delete_table(u'directory_payment')

        # Deleting model 'Currency'
        db.delete_table(u'directory_currency')

        # Deleting model 'Style'
        db.delete_table(u'directory_style')

        # Deleting model 'Directory'
        db.delete_table(u'directory_directory')

        # Removing M2M table for field category on 'Directory'
        db.delete_table(db.shorten_name(u'directory_directory_category'))

        # Removing M2M table for field service on 'Directory'
        db.delete_table(db.shorten_name(u'directory_directory_service'))

        # Removing M2M table for field payment on 'Directory'
        db.delete_table(db.shorten_name(u'directory_directory_payment'))

        # Removing M2M table for field style on 'Directory'
        db.delete_table(db.shorten_name(u'directory_directory_style'))

        # Deleting model 'Hours'
        db.delete_table(u'directory_hours')

        # Deleting model 'Stat'
        db.delete_table(u'directory_stat')

        # Deleting model 'Reserve'
        db.delete_table(u'directory_reserve')

        # Deleting model 'Comment'
        db.delete_table(u'directory_comment')

        # Deleting model 'Rate'
        db.delete_table(u'directory_rate')

        # Deleting model 'Package'
        db.delete_table(u'directory_package')

        # Deleting model 'Pay'
        db.delete_table(u'directory_pay')

        # Removing M2M table for field package on 'Pay'
        db.delete_table(db.shorten_name(u'directory_pay_package'))


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
        u'directory.comment': {
            'Meta': {'object_name': 'Comment'},
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'date_create': ('django.db.models.fields.DateTimeField', [], {}),
            'directory': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': u"orm['directory.Directory']"}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '100'}),
            'id_comment': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'})
        },
        u'directory.currency': {
            'Meta': {'object_name': 'Currency'},
            'id_currency': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'directory.directory': {
            'Meta': {'object_name': 'Directory'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'category': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['directory.Category']", 'symmetrical': 'False'}),
            'cell': ('django.db.models.fields.CharField', [], {'max_length': '45', 'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'comment': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'content': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.Country']"}),
            'currency': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['directory.Currency']"}),
            'date_create': ('django.db.models.fields.DateTimeField', [], {}),
            'date_update': ('django.db.models.fields.DateTimeField', [], {}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'email_user': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'facebook': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'geo_location': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'google_plus': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'id_directory': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keywords': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'language': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.Language']"}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'payment': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['directory.Payment']", 'symmetrical': 'False'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '45', 'null': 'True'}),
            'postal_code': ('django.db.models.fields.CharField', [], {'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'service': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['directory.Service']", 'null': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['home.State']"}),
            'status': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'style': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['directory.Style']", 'symmetrical': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'twitter': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'url_name': ('django.db.models.fields.SlugField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'website': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        u'directory.hours': {
            'Meta': {'object_name': 'Hours'},
            'day_week': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'directory': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['directory.Directory']"}),
            'hour_in': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'hour_out': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'id_hours': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        u'directory.package': {
            'Meta': {'object_name': 'Package'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'date_create': ('django.db.models.fields.DateTimeField', [], {}),
            'id_package': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '2'}),
            'price': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'status': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'directory.pay': {
            'Meta': {'object_name': 'Pay'},
            'concept': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'date_begin': ('django.db.models.fields.DateTimeField', [], {}),
            'date_create': ('django.db.models.fields.DateTimeField', [], {}),
            'date_end': ('django.db.models.fields.DateTimeField', [], {}),
            'directory': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['directory.Directory']", 'null': 'True', 'blank': 'True'}),
            'id_pay': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'package': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['directory.Package']", 'symmetrical': 'False'}),
            'pay_months': ('django.db.models.fields.IntegerField', [], {'max_length': '5'}),
            'pay_status': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'payment': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['directory.Payment']"}),
            'price': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'receiver_id': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'subtotal': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'txn_id': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'directory.payment': {
            'Meta': {'object_name': 'Payment'},
            'id_service': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'initials': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'pay_in_gm': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'status': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'directory.rate': {
            'Meta': {'object_name': 'Rate'},
            'date_create': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'directory': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': u"orm['directory.Directory']"}),
            'id_rate': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('django.db.models.fields.IntegerField', [], {'max_length': '1'})
        },
        u'directory.reserve': {
            'Meta': {'object_name': 'Reserve'},
            'date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_create': ('django.db.models.fields.DateTimeField', [], {}),
            'date_update': ('django.db.models.fields.DateTimeField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'directory': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': u"orm['directory.Directory']"}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'id_reserve': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'people': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'point': ('django.db.models.fields.IntegerField', [], {'max_length': '4', 'null': 'True', 'blank': 'True'}),
            'score': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '2', 'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'time': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'})
        },
        u'directory.service': {
            'Meta': {'object_name': 'Service'},
            'id_service': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'directory.stat': {
            'Meta': {'object_name': 'Stat'},
            'count': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'directory': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['directory.Directory']"}),
            'id_stat': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'directory.style': {
            'Meta': {'object_name': 'Style'},
            'id_style': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'})
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

    complete_apps = ['directory']