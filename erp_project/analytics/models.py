# from django.db import models


# class ReportDefinition(models.Model):
#     name = models.CharField(max_length=255)
#     description = models.TextField(blank=True)
#     filters = models.TextField(blank=True)  # JSON or filter description
#     query = models.TextField()  # SQL or ORM query as text
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.name


# class ReportExecution(models.Model):
#     report = models.ForeignKey(ReportDefinition, related_name='executions', on_delete=models.CASCADE)
#     executed_at = models.DateTimeField(auto_now_add=True)
#     status = models.CharField(max_length=50)  # e.g., Pending, Running, Completed, Failed
#     result = models.TextField(blank=True)  # JSON or CSV string of results 

#     def __str__(self):
#         return f"{self.report.name} executed at {self.executed_at}"


# class Dashboard(models.Model):
#     name = models.CharField(max_length=255)
#     description = models.TextField(blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.name


# class Widget(models.Model):
#     dashboard = models.ForeignKey(Dashboard, related_name='widgets', on_delete=models.CASCADE)
#     title = models.CharField(max_length=255)
#     widget_type = models.CharField(max_length=50)  # e.g., chart, KPI, table
#     config = models.TextField(blank=True)  # JSON config data for widget

#     def __str__(self):
#         return f"{self.title} on {self.dashboard.name}"


# class KPIStore(models.Model):
#     kpi_name = models.CharField(max_length=255)
#     kpi_value = models.FloatField()
#     timestamp = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.kpi_name} at {self.timestamp}"


# class ExportLog(models.Model):
#     report_execution = models.ForeignKey(ReportExecution, related_name='exports', on_delete=models.CASCADE)
#     export_type = models.CharField(max_length=10)  # e.g., CSV, PDF
#     exported_at = models.DateTimeField(auto_now_add=True)
#     exported_by = models.CharField(max_length=255)  # username or identifier

#     def __str__(self):
#         return f"{self.export_type} export at {self.exported_at} for {self.report_execution.report.name}"
from django.db import models
import uuid

class ReportDefinition(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    query_json = models.JSONField(default=dict)  # Use JSON for query/config
    created_by_uuid = models.UUIDField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class ReportExecution(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    report_uuid = models.UUIDField()  # Link by UUID only
    executed_by_uuid = models.UUIDField()
    executed_at = models.DateTimeField(auto_now_add=True)
    parameters_json = models.JSONField(default=dict)
    result_json = models.JSONField(default=dict)
    status = models.CharField(max_length=50, default='pending')
    error_message = models.TextField(blank=True, null=True)
    execution_time_ms = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.report_uuid} executed at {self.executed_at}"

class Dashboard(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    owner_uuid = models.UUIDField()
    is_shared = models.BooleanField(default=False)  # <-- ADD THIS
    shared_with_uuids = models.JSONField(default=list, blank=True)  
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Widget(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    dashboard_uuid = models.UUIDField()  # Link by UUID only
    title = models.CharField(max_length=255)
    widget_type = models.CharField(max_length=50)
    config_json = models.JSONField(default=dict)
    position_x = models.IntegerField(default=0)
    position_y = models.IntegerField(default=0)
    width = models.IntegerField(default=4)
    height = models.IntegerField(default=4)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.widget_type})"

class KPIStore(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    metric_name = models.CharField(max_length=255)
    metric_value = models.DecimalField(max_digits=15, decimal_places=2)
    metric_date = models.DateField()
    source_module = models.CharField(max_length=100)
    metadata_json = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.metric_name}: {self.metric_value} ({self.metric_date})"

class ExportLog(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    report_uuid = models.UUIDField()
    export_type = models.CharField(max_length=10)
    exported_by_uuid = models.UUIDField()
    file_path = models.CharField(max_length=255)
    file_size_bytes = models.BigIntegerField(null=True, blank=True)
    exported_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.export_type} export at {self.exported_at}"
