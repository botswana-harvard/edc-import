import factory

from datetime import date

from ...models import UploadExportReceiptFile


class UploadExportReceiptFileFactory(factory.DjangoModelFactory):
    class Meta:
        model = UploadExportReceiptFile

    file_name = factory.Sequence(lambda n: 'file_name{0}'.format(n))
    receipt_datetime = date.today()
