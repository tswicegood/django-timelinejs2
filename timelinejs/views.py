from django.http import HttpResponse
from django.views.generic.detail import BaseDetailView

from . import models


class TimelineJsonView(BaseDetailView):
    model = models.Timeline

    def render_to_response(self, context):
        return HttpResponse(self.object.to_json(), status=200,
                content_type="application/json")
