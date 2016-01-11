from datetime import date, timedelta

from django.db import models
from django.conf import settings

from edc_base.model.models import BaseUuidModel
from edc_sync.models import IncomingTransaction

from .upload_skip_days import UploadSkipDays


class UploadTransactionFile(BaseUuidModel):

    transaction_file = models.FileField(upload_to=settings.MEDIA_ROOT)

    file_name = models.CharField(max_length=50, null=True, editable=False, unique=True)

    file_date = models.DateField(null=True, editable=False)

    identifier = models.CharField(max_length=50, null=True)

    consume = models.BooleanField(default=True)

    total = models.IntegerField(editable=False, default=0)

    consumed = models.IntegerField(editable=False, default=0)

    not_consumed = models.IntegerField(editable=False, default=0, help_text='duplicates')

    producer = models.TextField(
        max_length=1000,
        null=True,
        editable=False,
        help_text='List of producers detected from the file.')

    objects = models.Manager()

    def save(self, *args, **kwargs):
        if not self.id:
            self.file_name = self.transaction_file.name.replace('\\', '/').split('/')[-1]
            date_string = self.file_name.split('_')[2].split('.')[0][:8]
            self.file_date = date(int(date_string[:4]), int(date_string[4:6]), int(date_string[6:8]))
            self.identifier = self.file_name.split('_')[1]
            if self.consume:
                self.consume_transactions()
        super(UploadTransactionFile, self).save(*args, **kwargs)

    def consume_transactions(self):
        """NOT HERE!!, this is edc_sync code!!"""
        if self.today_set_as_skip_day():
            raise TypeError(
                'Date \'{0}\' for \'{1}\' is already added to the skip table. '
                'So cannot upload on a date set to be skipped.'.format(self.file_date, self.identifier))
        if self.file_already_uploaded():
            raise TypeError(
                'File covering date of \'{0}\' for \'{1}\' is already uploaded.'.format(
                    self.file_date, self.identifier))
        if (not self.is_previous_day_file_uploaded() and not self.skip_previous_day() and not self.first_upload_or_skip_day()):
            raise TypeError('Missing Upload file from the previous day for \'{0}\'. Previous day is not set as a SKIP date.'.format(self.identifier))
        if self.today_within_skip_untill():
            raise TypeError('Cannot upload a file for this date \'{}\'. This date is covered by a skip until date for \'{}\'.'.format(self.file_date, self.identifier))
        deserializer = DeserializeFromTransaction()
        index = 0
        self.transaction_file.open()
        producer_list = []
        for index, outgoing in enumerate(deserializer.deserialize_json_file(self.transaction_file)):
            if not IncomingTransaction.objects.filter(pk=outgoing.get('pk')).exists():
                if outgoing.get('fields'):
                    self.consumed += 1
                    IncomingTransaction.objects.create(
                        pk=outgoing.get('pk'),
                        tx_name=outgoing.get('fields').get('tx_name'),
                        tx_pk=outgoing.get('fields').get('tx_pk'),
                        tx=outgoing.get('fields').get('tx'),
                        timestamp=outgoing.get('fields').get('timestamp'),
                        producer=outgoing.get('fields').get('producer'),
                        action=outgoing.get('fields').get('action'))
                    if outgoing.get('fields').get('producer') not in producer_list:
                        producer_list.append(outgoing.get('fields').get('producer'))
            else:
                self.not_consumed += 1
        self.total = index
        producer_list.sort()
        self.producer = ','.join(producer_list)

    def file_already_uploaded(self):
        if self.__class__.objects.filter(file_date=self.file_date, identifier__iexact=self.identifier).exists():
            return True
        return False

    def is_previous_day_file_uploaded(self):
        yesterday = self.file_date - timedelta(1)
        if self.__class__.objects.filter(file_date=yesterday, identifier__iexact=self.identifier).exists():
            return True
        return False

    def first_upload_or_skip_day(self):
        # This is the first upload or skip day record. Specific to a particular identifier
        if ((self.__class__.objects.filter(identifier__iexact=self.identifier).count() == 0)
            and (UploadSkipDays.objects.filter(identifier__iexact=self.identifier).count() == 0)):
            return True
        return False

    def skip_previous_day(self):
        yesterday = self.file_date - timedelta(1)
        if (UploadSkipDays.objects.filter(skip_date=yesterday, identifier__iexact=self.identifier).exists()
            or UploadSkipDays.objects.filter(skip_until_date=yesterday, identifier__iexact=self.identifier).exists()):
            return True
        return False

    def today_set_as_skip_day(self):
        if (UploadSkipDays.objects.filter(skip_date=self.file_date, identifier__iexact=self.identifier).exists() or
            UploadSkipDays.objects.filter(skip_until_date__gt=self.file_date, identifier__iexact=self.identifier).exists()):
            return True
        return False

    def today_within_skip_untill(self):
        if UploadSkipDays.objects.filter(skip_until_date__gt=self.file_date, identifier__iexact=self.identifier).exists():
            return True
        return False

    def __unicode__(self):
        return unicode(self.file_name)

    class Meta:
        app_label = 'edc_import'
        ordering = ('-created',)
