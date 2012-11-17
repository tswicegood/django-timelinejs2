import json
import random

from django.test import TestCase

from timelinejs import models


class AssetTestCase(TestCase):
    def test_to_json(self):
        """
        Verify that to_json returns appropriate JSON object
        """
        url = 'some-asset-%d.png' % random.randint(1000, 2000)
        credit = 'Some Random Credit %d' % random.randint(100, 200)
        caption = '<p>I\'m an HTML caption!</p>'
        m = models.Asset(url=url, credit=credit, caption=caption)

        expected = json.dumps({'url': url, 'credit': credit,
                'caption': caption})
        self.assertEqual(expected, m.to_json())
