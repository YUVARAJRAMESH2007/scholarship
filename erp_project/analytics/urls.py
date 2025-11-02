# from django.urls import path
# from . import views
# from .views import exportlog_pdf

# urlpatterns = [
#     # ReportDefinition
#     path('reports/', views.report_definition_list, name='report-list'),
#     path('reports/<int:pk>/', views.report_definition_detail, name='report-detail'),

#     # ReportExecution
#     path('executions/', views.report_execution_list, name='execution-list'),
#     path('executions/<int:pk>/', views.report_execution_detail, name='execution-detail'),

#     # Dashboard
#     path('dashboards/', views.dashboard_list, name='dashboard-list'),
#     path('dashboards/<int:pk>/', views.dashboard_detail, name='dashboard-detail'),

#     # Widget
#     path('widgets/', views.widget_list, name='widget-list'),
#     path('widgets/<int:pk>/', views.widget_detail, name='widget-detail'),

#     # KPIStore
#     path('kpis/', views.kpi_store_list, name='kpi-list'),
#     path('kpis/<int:pk>/', views.kpi_store_detail, name='kpi-detail'),

#     # ExportLog
#     path('exports/', views.export_log_list, name='export-list'),
#     path('exports/<int:pk>/', views.export_log_detail, name='export-detail'),

#     # PDF Preview
#     path('exportlog/<int:pk>/pdf/', exportlog_pdf, name='exportlog-pdf'),

# ]
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ScholarshipProgramViewSet, StudentViewSet, ScholarshipApplicationViewSet,
    ApplicationDocumentViewSet, AwardViewSet,
    ReportDefinitionViewSet, ReportExecutionViewSet,
    DashboardViewSet, WidgetViewSet, KPIStoreViewSet, ExportLogViewSet,
    exportlog_pdf
)

router = DefaultRouter()
router.register(r'programs', ScholarshipProgramViewSet, basename='program')
router.register(r'students', StudentViewSet, basename='student')
router.register(r'applications', ScholarshipApplicationViewSet, basename='application')
router.register(r'documents', ApplicationDocumentViewSet, basename='document')
router.register(r'awards', AwardViewSet, basename='award')
router.register(r'reports', ReportDefinitionViewSet, basename='report')
router.register(r'executions', ReportExecutionViewSet, basename='execution')
router.register(r'dashboards', DashboardViewSet, basename='dashboard')
router.register(r'widgets', WidgetViewSet, basename='widget')
router.register(r'kpis', KPIStoreViewSet, basename='kpi')
router.register(r'exports', ExportLogViewSet, basename='export')


urlpatterns = [
    path('', include(router.urls)),
    path('exports/<int:pk>/pdf/', exportlog_pdf, name='exportlog-pdf')
]


