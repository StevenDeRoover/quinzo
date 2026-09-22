from django.conf import settings
from django.urls import include, re_path

import quinzo.control.urls

base_patterns = []

control_patterns = [
    re_path(r'^control/', include((quinzo.control.urls, 'control'))),
]

debug_patterns = []
if settings.DEBUG:
    try:
        import debug_toolbar

        debug_patterns.append(re_path(r'^__debug__/', include(debug_toolbar.urls)))
    except ImportError:
        pass


common_patterns = base_patterns + control_patterns + debug_patterns

