from django.urls import include, re_path

from quinzo.control.views.dashboards.main import main_dashboard

urlpatterns = [
    re_path(r'^$', main_dashboard, name='index'),
]