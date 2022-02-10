from django.urls import path
from . import views

from django.views.decorators.csrf import csrf_exempt
from django.contrib import admin

urlpatterns = [
    path('', views.index, name="Complaints"),
    path('add-complaint', views.add_complaint, name="add-complaints"),
    path('edit-complaint/<int:id>', views.complaint_edit, name="complaint-edit"),
    path('complaint-delete/<int:id>', views.delete_complaint, name="complaint-delete"),
    path('search-complaints', csrf_exempt(views.search_complaints),name="search_complaints"),
    path('dashboardsearch-complaints', csrf_exempt(views.dashboard_search_complaints),name="dashboard_search_complaints"),
    path('dashboard_complaint_category_summary', views.dashboard_complaint_category_summary,name="dashboard_complaint_category_summary"),
    path('complaint_category_summary', views.complaint_category_summary,name="complaint_category_summary"),
    path('stats', views.stats_view,name="stats"),
    path('dashbord', views.dashboard_view,name="dashbord"),
    path('listdashbord', views.listdashboard_view,name="listdashbord"),
    path('admin/', admin.site.urls),
]
