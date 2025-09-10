from django.urls import path
from .views import Report, ReportSQL

urlpatterns = [
    path('report/', Report.as_view()),
    path('report-sql/', ReportSQL.as_view()),
]
