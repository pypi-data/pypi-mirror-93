from django.test import TestCase
from gn_places.utils import gn_get_or_create

GN_URL = "https://www.geonames.org/2772400/linz.html"
GN_ID = 2772400


class ConceptSchemeTest(TestCase):
    def setUp(self):
        self.item = gn_get_or_create(GN_URL)

    def test_001_gn_get_or_create_attr(self):
        self.assertEqual(getattr(self.item, 'gn_id'), f"{GN_ID}")

    def test_002_gn_get_or_create_attr(self):
        self.assertEqual(getattr(self.item, 'gn_country_code'), "AT")

    def test_003_gn_get_or_create_no_duplicates(self):
        item = gn_get_or_create(GN_URL)
        self.assertEqual(item.gn_id, GN_ID)
        self.assertEqual(self.item, item)
