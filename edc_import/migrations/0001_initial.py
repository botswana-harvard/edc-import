# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'UploadSkipDays'
        db.create_table(u'import_uploadskipdays', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac2-2.local', max_length=50)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('revision', self.gf('django.db.models.fields.CharField')(max_length=75, null=True, blank=True)),
            ('skip_date', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2016, 1, 9, 0, 0))),
            ('skip_until_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('identifier', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('import', ['UploadSkipDays'])

        # Adding unique constraint on 'UploadSkipDays', fields ['skip_date', 'identifier']
        db.create_unique(u'import_uploadskipdays', ['skip_date', 'identifier'])

        # Adding model 'UploadTransactionFile'
        db.create_table(u'import_uploadtransactionfile', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac2-2.local', max_length=50)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('revision', self.gf('django.db.models.fields.CharField')(max_length=75, null=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('transaction_file', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('file_name', self.gf('django.db.models.fields.CharField')(max_length=50, unique=True, null=True)),
            ('file_date', self.gf('django.db.models.fields.DateField')(null=True)),
            ('identifier', self.gf('django.db.models.fields.CharField')(max_length=50, null=True)),
            ('consume', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('total', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('consumed', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('not_consumed', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('producer', self.gf('django.db.models.fields.TextField')(max_length=1000, null=True)),
        ))
        db.send_create_signal('import', ['UploadTransactionFile'])

        # Adding model 'UploadExportReceiptFile'
        db.create_table(u'import_uploadexportreceiptfile', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac2-2.local', max_length=50)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('revision', self.gf('django.db.models.fields.CharField')(max_length=75, null=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('export_receipt_file', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('file_name', self.gf('django.db.models.fields.CharField')(max_length=50, unique=True, null=True)),
            ('app_label', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('object_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('accepted', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('duplicate', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('total', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('errors', self.gf('django.db.models.fields.TextField')(null=True)),
            ('receipt_datetime', self.gf('django.db.models.fields.DateTimeField')(null=True)),
        ))
        db.send_create_signal('import', ['UploadExportReceiptFile'])


    def backwards(self, orm):
        # Removing unique constraint on 'UploadSkipDays', fields ['skip_date', 'identifier']
        db.delete_unique(u'import_uploadskipdays', ['skip_date', 'identifier'])

        # Deleting model 'UploadSkipDays'
        db.delete_table(u'import_uploadskipdays')

        # Deleting model 'UploadTransactionFile'
        db.delete_table(u'import_uploadtransactionfile')

        # Deleting model 'UploadExportReceiptFile'
        db.delete_table(u'import_uploadexportreceiptfile')


    models = {
        'import.uploadexportreceiptfile': {
            'Meta': {'ordering': "('-created',)", 'object_name': 'UploadExportReceiptFile'},
            'accepted': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'duplicate': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'errors': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'export_receipt_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'file_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'unique': 'True', 'null': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac2-2.local'", 'max_length': '50'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'object_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'receipt_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'total': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'user_created': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'import.uploadskipdays': {
            'Meta': {'ordering': "('-created',)", 'unique_together': "(('skip_date', 'identifier'),)", 'object_name': 'UploadSkipDays'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac2-2.local'", 'max_length': '50'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'skip_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2016, 1, 9, 0, 0)'}),
            'skip_until_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'import.uploadtransactionfile': {
            'Meta': {'ordering': "('-created',)", 'object_name': 'UploadTransactionFile'},
            'consume': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'consumed': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'file_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'file_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'unique': 'True', 'null': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac2-2.local'", 'max_length': '50'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'not_consumed': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'producer': ('django.db.models.fields.TextField', [], {'max_length': '1000', 'null': 'True'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'total': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'transaction_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'user_created': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['import']