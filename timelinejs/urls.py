from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns('',
    url(r'^(?P<pk>\d+).json$', views.TimelineJsonView.as_view(),
            name='timelinejs_json'),
)
