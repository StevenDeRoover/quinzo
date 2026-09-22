from django.urls import include, re_path
from django.views.generic import TemplateView

from quinzo.urls import common_patterns

quinzomain_patterns_main = [
    re_path(r'', include(([
        re_path(r'^$', TemplateView.as_view(template_name='quinzomain/index.html'), name="index")
    ], 'main')))
]

urlpatterns = common_patterns +  quinzomain_patterns_main

# handler404 = 'pretix.base.views.errors.page_not_found'
# handler500 = 'pretix.base.views.errors.server_error'