from optparse import make_option

from django.db.models import get_model
from django.core.files import File

from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    """ Exports currently unsynchronized outgoing transactions to json file
    """
    args = ('--path <full_qualified_path>')

    help = 'Upload transactions json file to incoming transactions table'

    option_list = BaseCommand.option_list + (
        make_option(
            '--path',
            dest='path',
            action='store_true',
            default=False,
            help=('Fully qualified path.')),
        )
    
    def handle(self, *args, **options):
        if options['path']:
            if not args or len(args) != 1:
                CommandError('Make sure you provide a single <path> argument')
            path = args[0]
            print path
            uploaded, duplicates = self.upload_transaction_file(path)
            print "Uploaded {0} incoming transactions from {1}, {2} where duplicates".format(uploaded, path, duplicates)
        else:
            raise CommandError('Unknown option, Try --help for a list of valid options')

    def upload_transaction_file(self, path):
        UploadTransactionFile = get_model('import', 'UploadTransactionFile')
        f = open(path, 'r')
        djangoFile = File(f)
        UploadTransactionFile.objects.create(transaction_file=djangoFile, consume=True)
        filename = path.split('/')[-1]
        uploaded = UploadTransactionFile.objects.get(file_name=filename)
        return (uploaded.consumed, uploaded.not_consumed)