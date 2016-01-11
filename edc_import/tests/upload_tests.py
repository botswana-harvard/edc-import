from datetime import date, timedelta

from django.conf import settings
from django.test import TestCase
from django.core.files import File
from django.db.utils import IntegrityError

from ..models import UploadSkipDays, UploadTransactionFile

from .factories import UploadSkipDaysFactory, UploadTransactionFileFactory


class UploadTests(TestCase):

    def setUp(self):
        pass

    def test_create_initial_skip(self):
        self.assertEqual(UploadSkipDays.objects.count(), 0)
        skip_day = UploadSkipDaysFactory(skip_date=date.today() - timedelta(1))
        self.assertEqual(UploadSkipDays.objects.count(), 1)
        UploadSkipDays.objects.all().delete()

    def test_initial_upload_file(self):
        self.assertEqual(UploadTransactionFile.objects.count(), 0)
        upload_file = UploadTransactionFileFactory(transaction_file=File(open(settings.MEDIA_ROOT+'/bcpp_lentswe_201412081525.json', 'r')), file_name='bcpp_lentswe_201412081525.json')
        self.assertEqual(UploadTransactionFile.objects.count(), 1)
        UploadTransactionFile.objects.all().delete()

    def test_skip_upload_logic(self):
        # Ensure that you initially have zero uploaded transaction files.
        self.assertEqual(UploadTransactionFile.objects.count(), 0)
        # Ensure that you initially have zero skip days defined
        self.assertEqual(UploadSkipDays.objects.count(), 0)
        # create initial upload file, all should work ok.
        upload_file_1 = UploadTransactionFileFactory(transaction_file=File(open(settings.MEDIA_ROOT+'/bcpp_lentswe_201412081525.json', 'r')), file_name='bcpp_lentswe_201412081525.json', identifier='lentswe')
        # Attempting to create another upload file for the same day and identifier(lentswe) should raise an error.
        #self.assertRaises(IntegrityError, UploadTransactionFileFactory(transaction_file=File(open(settings.MEDIA_ROOT+'/bcpp_lentswe_201412081525.json', 'r')), file_name='bcpp_lentswe_201412081525.json', identifier='lentswe'))
        # Creating another upload file with a different identifier(letlha) should work fine
        upload_file_2 = UploadTransactionFileFactory(transaction_file=File(open(settings.MEDIA_ROOT+'/bcpp_letlha_201410131525.json', 'r')), file_name='bcpp_letlha_201410131525.json', identifier='letlha')
        # Attempting to create a skip day for an identifier(lentswe) with an existing upload file should raise an error.
        with self.assertRaises(TypeError):
            UploadSkipDaysFactory(skip_date=date(2014, 12, 8), identifier='lentswe')
        # creating the next day as a skip day for lentswe should be ok.
        skip_day_1 = UploadSkipDaysFactory(skip_date=date(2014, 12, 8) + timedelta(1), identifier='lentswe')
        # Attempting to create another upload two days from now for letlha should fail i.e no previous day upload or skip day found.
#         with self.assertRaises(TypeError):
#             UploadTransactionFileFactory(transaction_file=File(open(settings.MEDIA_ROOT+'/bcpp_letlha_201410151525.json', 'r')), file_name='bcpp_letlha_201410151525.json', identifier='letlha')
        # Creating an upload for two days later for lentswe should work as there is a skip day from previous day.
        UploadTransactionFileFactory(transaction_file=File(open(settings.MEDIA_ROOT+'/bcpp_lentswe_201412111525.json', 'r')), file_name='bcpp_lentswe_201412111525.json', identifier='lentswe')
        # Attempting to create a skip day for two days later for letlha should fail i.e no previous date skip or upload
        with self.assertRaises(TypeError):
            UploadSkipDaysFactory(skip_date=date(2014, 10, 13) + timedelta(2), identifier='letlha')
        # Uploading skip day 1 day later for letlha should work as upload file exists for today.
        UploadSkipDaysFactory(skip_date=date(2014, 10, 13) + timedelta(1), skip_until_date=date(2014, 10, 13) + timedelta(5), identifier='letlha')
        # Uploading another skip day 2 days later for letlha should fail as current skip day has ignore until for next 5days.
        with self.assertRaises(TypeError):
            UploadSkipDaysFactory(skip_date=date(2014, 10, 13) + timedelta(2), identifier='letlha')
        # Uploading another skip day 6 days later for letlha should work as ignore until expires after 5 days..
        UploadSkipDaysFactory(skip_date=date(2014, 10, 13) + timedelta(6), skip_until_date=date(2014, 10, 19) + timedelta(4), identifier='letlha')
        with self.assertRaises(TypeError):
            file3 = UploadTransactionFile(transaction_file=File(open(settings.MEDIA_ROOT+'/bcpp_letlha_201410201525.json', 'r')), file_name='bcpp_letlha_201410201525.json', identifier='letlha')
            file3.save()
            #UploadTransactionFileFactory(transaction_file=File(open(settings.MEDIA_ROOT+'/bcpp_letlha_201410201525.json', 'r')), file_name='bcpp_letlha_201410201525.json', identifier='letlha')
        file4 = UploadTransactionFile(transaction_file=File(open(settings.MEDIA_ROOT+'/bcpp_letlha_201410241525.json', 'r')), file_name='bcpp_letlha_201410241525.json', identifier='letlha')
        file4.save()
        #UploadTransactionFileFactory(transaction_file=File(open(settings.MEDIA_ROOT+'/bcpp_letlha_201410241525.json', 'r')), file_name='bcpp_letlha_201410241525.json', identifier='letlha')
