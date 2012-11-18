import datetime
import json
import random

from django.test import TestCase
import factory

from timelinejs import models

seq = lambda s: factory.Sequence(lambda n: s.format(n))


def generate_random_start_date(*args):
    now = datetime.datetime.now()
    r = random.randint(-10, 10)
    return (now - datetime.timedelta(days=r)).date()


class AssetFactory(factory.Factory):
    FACTORY_FOR = models.Asset

    media = seq('media-{0}.png')
    credit = seq('credit-{0}')
    caption = seq('caption-{0}')


class TimelineFactory(factory.Factory):
    FACTORY_FOR = models.Timeline

    headline = seq('headline-{0}')
    start_date = factory.LazyAttribute(generate_random_start_date)
    text = seq('<p>Random Text{0}</p>')
    asset = factory.SubFactory(AssetFactory)


class TimelineEntryFactory(factory.Factory):
    FACTORY_FOR = models.TimelineEntry

    timeline = factory.SubFactory(TimelineFactory)
    start_date = factory.LazyAttribute(generate_random_start_date)
    headline = seq('timeline-entry-headline-{0}')
    text = seq('<p>Timeline Entry Text {0}</p>')
    asset = factory.SubFactory(AssetFactory)


def generate_random_asset(save=True):
    return AssetFactory.create() if save else AssetFactory.build()


def generate_random_timeline(save=True):
    return TimelineFactory.create() if save else TimelineFactory.build()


def generate_random_timeline_entry(timeline, save=True):
    return TimelineEntryFactory.create() if save else \
        TimelineFactory.build()


class AssetTestCase(TestCase):
    def test_unicode_shows_caption(self):
        asset = AssetFactory.build()
        self.assertEqual(asset.caption, str(asset))

    def test_to_json(self):
        """
        Verify that to_json returns appropriate JSON object
        """
        media = 'some-asset-%d.png' % random.randint(1000, 2000)
        credit = 'Some Random Credit %d' % random.randint(100, 200)
        caption = '<p>I\'m an HTML caption!</p>'
        m = models.Asset(media=media, credit=credit, caption=caption)

        expected = json.dumps({'media': media, 'credit': credit,
                'caption': caption})
        self.assertEqual(expected, m.to_json())


class TimelineEntryTestCase(TestCase):
    @property
    def timeline_entry_kwargs(self):
        return TimelineFactory.attributes()

    def test_unicode_shows_timeline_plus_headline(self):
        entry = TimelineEntryFactory.build()
        expected = '{0}: {1}'.format(entry.timeline, entry.headline)
        self.assertEqual(expected, str(entry))

    def test_to_json_dict(self):
        kwargs = self.timeline_entry_kwargs
        entry = models.TimelineEntry(**kwargs)
        expected = {
            'startDate': kwargs['start_date'].strftime('%Y,%m,%d'),
            'headline': kwargs['headline'],
            'text': kwargs['text'],
            'asset': kwargs['asset'].to_json_dict(),
        }
        self.assertEqual(expected, entry.to_json_dict())

    def test_to_json(self):
        kwargs = self.timeline_entry_kwargs
        entry = models.TimelineEntry(**kwargs)
        expected = json.dumps({
            'startDate': kwargs['start_date'].strftime('%Y,%m,%d'),
            'headline': kwargs['headline'],
            'text': kwargs['text'],
            'asset': kwargs['asset'].to_json_dict()
        })
        self.assertEqual(expected, entry.to_json())

    def test_can_convert_to_json_with_string_dates(self):
        kwargs = self.timeline_entry_kwargs
        kwargs['start_date'] = kwargs['start_date'].strftime('%Y-%m-%d')
        entry = models.TimelineEntry(**kwargs)
        entry.to_json()


class TimelineTestCase(TestCase):
    @property
    def timeline_kwargs(self):
        return TimelineFactory.attributes()

    def test_unicode_shows_headline(self):
        timeline = TimelineFactory.build()
        self.assertEqual(timeline.headline, str(timeline))

    def test_to_json(self):
        kwargs = self.timeline_kwargs
        timeline = models.Timeline(**kwargs)
        expected = json.dumps({'timeline': {
            'headline': kwargs['headline'],
            'type': 'default',
            'startDate': kwargs['start_date'].strftime('%Y,%m,%d'),
            'text': kwargs['text'],
            'asset': kwargs['asset'].to_json_dict(),
            'date': [],
        }})
        self.assertEqual(expected, timeline.to_json())

    def test_can_convert_to_json_with_string_dates(self):
        kwargs = self.timeline_kwargs
        kwargs['start_date'] = kwargs['start_date'].strftime('%Y-%m-%d')
        timeline = models.Timeline(**kwargs)
        timeline.to_json()

    def test_to_json_with_one_date(self):
        entry = TimelineEntryFactory.create()
        timeline = entry.timeline

        expected = [entry.to_json_dict()]
        actual = json.loads(timeline.to_json())['timeline']['date']
        self.assertEqual(expected, actual)

    def test_to_json_with_two_dates(self):
        timeline = TimelineFactory.create()
        entry_a = TimelineEntryFactory.create(timeline=timeline)
        entry_b = TimelineEntryFactory.create(timeline=timeline)

        expected = [entry_a.to_json_dict(), entry_b.to_json_dict()]
        actual = json.loads(timeline.to_json())['timeline']['date']
        self.assertEqual(expected, actual)
