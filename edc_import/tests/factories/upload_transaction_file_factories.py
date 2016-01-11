import factory

from django.db import models

from ...models import UploadTransactionFile


class UploadTransactionFileFactory(factory.DjangoModelFactory):
    FACTORY_FOR = UploadTransactionFile

    file_name = factory.Sequence(lambda n: 'file_name{0}'.format(n))
    transaction_file = models.FileField(name=file_name)
    identifier = factory.Sequence(lambda n: 'identifier{0}'.format(n))
    consume = False
    producer = factory.Sequence(lambda n: 'producer{0}'.format(n))
