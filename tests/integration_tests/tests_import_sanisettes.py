import pytest
from django.core.management import call_command

from locator.models import Sanisette


@pytest.mark.integration
@pytest.mark.django_db
def test_import_sanisettes_command_real_api():
    call_command("import_sanisettes")
    count = Sanisette.objects.count()
    assert count > 0
    s = Sanisette.objects.first()
    assert s.latitude is not None
    assert s.longitude is not None
    assert s.adresse != ""
