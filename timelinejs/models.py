import json

from django.db import models


class Asset(models.Model):
    url = models.TextField()
    credit = models.TextField(blank=True, default='')
    caption = models.TextField(blank=True, default='')

    def to_json(self):
        return json.dumps({
            'url': self.url,
            'credit': self.credit,
            'caption': self.caption,
        })


class Timeline(models.Model):
    headline = models.CharField(max_length=255)
    start_date = models.DateField()
    text = models.TextField()
    asset = models.ForeignKey(Asset, related_name='timelines')

    def __unicode__(self):
        return self.headline


class TimelineEntry(models.Model):
    timeline = models.ForeignKey(Timeline, related_name='entries')
    start_date = models.DateField()
    headline = models.CharField(max_length=255)
    text = models.TextField()
    asset = models.ForeignKey(Asset, related_name='timeline_entries')

    def __unicode__(self):
        return "%s: %s" % (self.timeline, self.headline)
