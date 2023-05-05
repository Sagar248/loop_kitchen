from django.urls import path

from core.views import TriggerReport, GetReport

urlpatterns = [
    path('trigger_report/', TriggerReport.as_view(), name="trigger_report_view"),
    path('get_report/', GetReport.as_view(), name="get_report_view")
]