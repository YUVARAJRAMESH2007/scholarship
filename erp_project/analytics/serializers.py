from rest_framework import serializers
from .models import *


class ScholarshipProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScholarshipProgram
        fields = '__all__'


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'


class ScholarshipApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScholarshipApplication
        fields = '__all__'


class ApplicationDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationDocument
        fields = '__all__'


class AwardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Award
        fields = '__all__'


class ReportDefinitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportDefinition
        fields = '__all__'


class ReportExecutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportExecution
        fields = '__all__'


class ExecuteReportSerializer(serializers.Serializer):
    parameters_json = serializers.JSONField(default=dict, required=False)
    executed_by_id = serializers.IntegerField()


class DashboardSerializer(serializers.ModelSerializer):
    widget_count = serializers.SerializerMethodField()

    class Meta:
        model = Dashboard
        fields = '__all__'

    def get_widget_count(self, obj):
        return Widget.objects.filter(dashboard=obj).count()


class WidgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Widget
        fields = '__all__'


class KPIStoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = KPIStore
        fields = '__all__'


class ExportLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExportLog
        fields = '__all__'


class ExportRequestSerializer(serializers.Serializer):
    export_type = serializers.ChoiceField(choices=['CSV', 'PDF', 'XLSX', 'JSON'])
    exported_by_id = serializers.IntegerField()
    parameters_json = serializers.JSONField(default=dict, required=False)
