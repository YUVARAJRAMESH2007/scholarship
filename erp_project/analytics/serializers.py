# analytics/serializers.py
from rest_framework import serializers
from .models import ReportDefinition, ReportExecution, Dashboard, Widget, KPIStore, ExportLog



class ReportDefinitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportDefinition
        fields = [
            'uuid', 'name', 'description', 'query_json', 'created_by_uuid',
            'created_at', 'is_active'
        ]
        read_only_fields = ['uuid', 'created_at']



class ReportExecutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportExecution
        fields = [
            'uuid', 'report_uuid', 'executed_by_uuid', 'executed_at',
            'parameters_json', 'result_json', 'status', 'error_message',
            'execution_time_ms'
        ]
        read_only_fields = ['uuid', 'executed_at', 'execution_time_ms']



class ExecuteReportSerializer(serializers.Serializer):
    parameters_json = serializers.JSONField(default=dict, required=False)
    executed_by_uuid = serializers.UUIDField()



class WidgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Widget
        fields = [
            'uuid', 'dashboard_uuid', 'title', 'widget_type', 'config_json',
            'position_x', 'position_y', 'width', 'height',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['uuid', 'created_at', 'updated_at']



class DashboardSerializer(serializers.ModelSerializer):
    widget_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Dashboard
        fields = [
            'uuid', 'name', 'owner_uuid', 'description', 'is_shared',
            'shared_with_uuids', 'created_at', 'updated_at', 'widget_count'
        ]
        read_only_fields = ['uuid', 'created_at', 'updated_at']
    
    def get_widget_count(self, obj):
        return Widget.objects.filter(dashboard_uuid=obj.uuid).count()



class KPIStoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = KPIStore
        fields = [
            'uuid', 'metric_name', 'metric_value', 'metric_date',
            'source_module', 'metadata_json', 'created_at'
        ]
        read_only_fields = ['uuid', 'created_at']



class ExportLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExportLog
        fields = [
            'uuid', 'report_uuid', 'export_type', 'exported_by_uuid',
            'file_path', 'file_size_bytes', 'exported_at', 'expires_at',
            'is_deleted'
        ]
        read_only_fields = ['uuid', 'exported_at', 'file_size_bytes']



class ExportRequestSerializer(serializers.Serializer):
    export_type = serializers.ChoiceField(choices=['CSV', 'PDF', 'XLSX', 'JSON'])
    exported_by_uuid = serializers.UUIDField()
    parameters_json = serializers.JSONField(default=dict, required=False)
