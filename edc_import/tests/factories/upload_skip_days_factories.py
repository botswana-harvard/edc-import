import factory

from datetime import date

from ...models import UploadSkipDays


class UploadSkipDaysFactory(factory.DjangoModelFactory):
    class Meta:
        model = UploadSkipDays

    skip_date = date.today()
    skip_until_date = None
    identifier = factory.Sequence(lambda n: 'identifier{0}'.format(n))
