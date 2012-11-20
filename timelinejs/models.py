import json

from dateutil.parser import parse
from django.db import models


class Asset(models.Model):
    media = models.TextField()
    credit = models.TextField(blank=True, default='')
    caption = models.TextField(blank=True, default='')

    def __unicode__(self):
        return self.caption

    def to_json_dict(self):
        return {
            'media': self.media,
            'credit': self.credit,
            'caption': self.caption,
        }

    def to_json(self):
        return json.dumps(self.to_json_dict())


class Timeline(models.Model):
    headline = models.CharField(max_length=255)
    start_date = models.DateField()
    slug = models.SlugField(default='')
    text = models.TextField()
    asset = models.ForeignKey(Asset, related_name='timelines')

    def __unicode__(self):
        return self.headline

    def to_json(self):
        if type(self.start_date) is str:
            self.start_date = parse(self.start_date)
        return json.dumps({"timeline": {
            'headline': self.headline,
            'type': 'default',
            'startDate': self.start_date.strftime('%Y,%m,%d'),
            'text': self.text,
            'asset': self.asset.to_json_dict(),
            'date': [a.to_json_dict() for a in self.entries.all()],
        }})


class TimelineEntry(models.Model):
    timeline = models.ForeignKey(Timeline, related_name='entries')
    start_date = models.DateField()
    headline = models.CharField(max_length=255)
    text = models.TextField()
    asset = models.ForeignKey(Asset, related_name='timeline_entries')

    def __unicode__(self):
        return "%s: %s" % (self.timeline, self.headline)

    def to_json_dict(self):
        if type(self.start_date) is str:
            self.start_date = parse(self.start_date)
        return {
            'startDate': self.start_date.strftime('%Y,%m,%d'),
            'headline': self.headline,
            'text': self.text,
            'asset': self.asset.to_json_dict(),
        }

    def to_json(self):
        return json.dumps(self.to_json_dict())
