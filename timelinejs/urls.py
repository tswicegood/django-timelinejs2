try:
    from django.conf.urls import patterns, url
except ImportError:
    # Support Django 1.3
    from django.conf.urls.defaults import patterns, url

from . import views

urlpatterns = patterns('',
    url(r'^(?P<pk>\d+).json$', views.TimelineJsonView.as_view(),
            name='timelinejs_json'),
)
