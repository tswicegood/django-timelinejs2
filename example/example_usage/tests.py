import datetime
import json
import random

from django.test import TestCase

from timelinejs import models


def generate_random_headline():
    return 'random-headline-%d' % random.randint(1000, 2000)


def generate_random_start_date():
    now = datetime.datetime.now()
    r = random.randint(-10, 10)
    return (now - datetime.timedelta(days=r)).date()


def generate_random_text():
    return 'random text %d' % random.randint(1000, 2000)


def generate_random_media():
    return 'some-asset-%d.png' % random.randint(1000, 2000)


def generate_random_credit():
    return 'Some Random Credit %d' % random.randint(1000, 2000)


def generate_random_caption():
    return '<p>Some HTML caption, %d!</p>' % random.randint(1000, 2000)


def generate_random_asset(save=True):
    m = models.Asset(media=generate_random_media(),
            credit=generate_random_credit(),
            caption=generate_random_caption())
    if save:
        m.save()
    return m


def generate_random_timeline(save=True):
    m = models.Timeline(headline=generate_random_headline(),
            start_date=generate_random_start_date(),
            text=generate_random_text(),
            asset=generate_random_asset())
    if save:
        m.save()
    return m


def generate_random_timeline_entry(timeline, save=True):
    m = models.TimelineEntry(timeline=timeline,
            headline=generate_random_headline(),
            start_date=generate_random_start_date(),
            text=generate_random_text(),
            asset=generate_random_asset(save=save))
    if save:
        m.save()
    return m


class AssetTestCase(TestCase):
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
        return {
            'start_date': generate_random_start_date(),
            'headline': generate_random_headline(),
            'text': generate_random_text(),
            'asset': generate_random_asset(),
            'timeline': generate_random_timeline(),
        }

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


class TimelineTestCase(TestCase):
    @property
    def timeline_kwargs(self):
        return {
            'headline': generate_random_headline(),
            'start_date': generate_random_start_date(),
            'text': generate_random_text(),
            'asset': generate_random_asset(),
        }

    def test_to_json(self):
        kwargs = self.timeline_kwargs
        timeline = models.Timeline(**kwargs)
        expected = json.dumps({
            'headline': kwargs['headline'],
            'startDate': kwargs['start_date'].strftime('%Y,%m,%d'),
            'text': kwargs['text'],
            'asset': kwargs['asset'].to_json_dict(),
            'date': [],
        })
        self.assertEqual(expected, timeline.to_json())

    def test_to_json_with_one_date(self):
        kwargs = self.timeline_kwargs
        timeline = models.Timeline.objects.create(**kwargs)
        entry = generate_random_timeline_entry(timeline, save=True)

        expected = json.dumps({
            'headline': kwargs['headline'],
            'startDate': kwargs['start_date'].strftime('%Y,%m,%d'),
            'text': kwargs['text'],
            'asset': kwargs['asset'].to_json_dict(),
            'date': [entry.to_json_dict()],
        })
        self.assertEqual(expected, timeline.to_json())

    def test_to_json_with_two_dates(self):
        kwargs = self.timeline_kwargs
        timeline = models.Timeline.objects.create(**kwargs)
        entry_a = generate_random_timeline_entry(timeline, save=True)
        entry_b = generate_random_timeline_entry(timeline, save=True)

        expected = json.dumps({
            'headline': kwargs['headline'],
            'startDate': kwargs['start_date'].strftime('%Y,%m,%d'),
            'text': kwargs['text'],
            'asset': kwargs['asset'].to_json_dict(),
            'date': [entry_a.to_json_dict(), entry_b.to_json_dict()],
        })
        self.assertEqual(expected, timeline.to_json())
