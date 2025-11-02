# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# import json
# from .models import ReportDefinition, ReportExecution, Dashboard, Widget, KPIStore, ExportLog

# # ReportDefinition APIs
# @csrf_exempt
# def report_definition_list(request):
#     if request.method == 'GET':
#         reports = ReportDefinition.objects.all()
#         data = [
#             {
#                 "id": r.id,
#                 "name": r.name,
#                 "description": r.description,
#                 "filters": r.filters,
#                 "query": r.query,
#                 "created_at": r.created_at.isoformat()
#             } for r in reports
#         ]
#         return JsonResponse(data, safe=False)
#     elif request.method == 'POST':
#         body = json.loads(request.body.decode('utf-8'))
#         report = ReportDefinition.objects.create(
#             name=body.get('name'),
#             description=body.get('description', ''),
#             filters=body.get('filters', ''),
#             query=body.get('query', '')
#         )
#         return JsonResponse({
#             "id": report.id,
#             "name": report.name,
#             "description": report.description,
#             "filters": report.filters,
#             "query": report.query,
#             "created_at": report.created_at.isoformat()
#         }, status=201)




# @csrf_exempt
# def report_definition_detail(request, pk):
#     try:
#         report = ReportDefinition.objects.get(pk=pk)
#     except ReportDefinition.DoesNotExist:
#         return JsonResponse({'error': 'Not found'}, status=404)

#     if request.method == 'GET':
#         data = {
#             "id": report.id,
#             "name": report.name,
#             "description": report.description,
#             "filters": report.filters,
#             "query": report.query,
#             "created_at": report.created_at.isoformat()
#         }
#         return JsonResponse(data)

#     elif request.method == 'PUT':
#         try:
#             print(request.body)  # Debug: View in terminal what Postman sends
#             body = json.loads(request.body.decode('utf-8'))
#             report.name = body.get('name', report.name)
#             report.description = body.get('description', report.description)
#             report.filters = body.get('filters', report.filters)
#             report.query = body.get('query', report.query)
#             report.save()
#             return JsonResponse({
#                 "id": report.id,
#                 "name": report.name,
#                 "description": report.description,
#                 "filters": report.filters,
#                 "query": report.query,
#                 "created_at": report.created_at.isoformat()
#             })
#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=400)

#     elif request.method == 'DELETE':
#         report.delete()
#         return JsonResponse({'message': 'Deleted'}, status=204)
#     else:
#         return JsonResponse({'error': 'Method not allowed'}, status=405)


# # ReportExecution APIs
# @csrf_exempt
# def report_execution_list(request):
#     if request.method == 'GET':
#         executions = ReportExecution.objects.all()
#         data = [
#             {
#                 "id": e.id,
#                 "report_id": e.report.id,
#                 "executed_at": e.executed_at.isoformat(),
#                 "status": e.status,
#                 "result": e.result
#             } for e in executions
#         ]
#         return JsonResponse(data, safe=False)
#     elif request.method == 'POST':
#         body = json.loads(request.body.decode('utf-8'))
#         report = ReportDefinition.objects.get(pk=body.get('report_id'))
#         execution = ReportExecution.objects.create(
#             report=report,
#             status=body.get('status', 'Pending'),
#             result=body.get('result', '')
#         )
#         return JsonResponse({
#             "id": execution.id,
#             "report_id": execution.report.id,
#             "executed_at": execution.executed_at.isoformat(),
#             "status": execution.status,
#             "result": execution.result
#         }, status=201)

# @csrf_exempt
# def report_execution_detail(request, pk):
#     try:
#         execution = ReportExecution.objects.get(pk=pk)
#     except ReportExecution.DoesNotExist:
#         return JsonResponse({'error': 'Not found'}, status=404)

#     if request.method == 'GET':
#         data = {
#             "id": execution.id,
#             "report_id": execution.report.id,
#             "executed_at": execution.executed_at.isoformat(),
#             "status": execution.status,
#             "result": execution.result
#         }
#         return JsonResponse(data)
#     elif request.method == 'PUT':
#         body = json.loads(request.body.decode('utf-8'))
#         execution.status = body.get('status', execution.status)
#         execution.result = body.get('result', execution.result)
#         execution.save()
#         return JsonResponse({
#             "id": execution.id,
#             "report_id": execution.report.id,
#             "executed_at": execution.executed_at.isoformat(),
#             "status": execution.status,
#             "result": execution.result
#         })
#     elif request.method == 'DELETE':
#         execution.delete()
#         return JsonResponse({'message': 'Deleted'}, status=204)


# # Dashboard APIs
# @csrf_exempt
# def dashboard_list(request):
#     if request.method == 'GET':
#         dashboards = Dashboard.objects.all()
#         data = [
#             {
#                 "id": d.id,
#                 "name": d.name,
#                 "description": d.description,
#                 "created_at": d.created_at.isoformat()
#             } for d in dashboards
#         ]
#         return JsonResponse(data, safe=False)
#     elif request.method == 'POST':
#         body = json.loads(request.body.decode('utf-8'))
#         dashboard = Dashboard.objects.create(
#             name=body.get('name'),
#             description=body.get('description', '')
#         )
#         return JsonResponse({
#             "id": dashboard.id,
#             "name": dashboard.name,
#             "description": dashboard.description,
#             "created_at": dashboard.created_at.isoformat()
#         }, status=201)

# @csrf_exempt
# def dashboard_detail(request, pk):
#     try:
#         dashboard = Dashboard.objects.get(pk=pk)
#     except Dashboard.DoesNotExist:
#         return JsonResponse({'error': 'Not found'}, status=404)

#     if request.method == 'GET':
#         data = {
#             "id": dashboard.id,
#             "name": dashboard.name,
#             "description": dashboard.description,
#             "created_at": dashboard.created_at.isoformat()
#         }
#         return JsonResponse(data)
#     elif request.method == 'PUT':
#         body = json.loads(request.body.decode('utf-8'))
#         dashboard.name = body.get('name', dashboard.name)
#         dashboard.description = body.get('description', dashboard.description)
#         dashboard.save()
#         return JsonResponse({
#             "id": dashboard.id,
#             "name": dashboard.name,
#             "description": dashboard.description,
#             "created_at": dashboard.created_at.isoformat()
#         })
#     elif request.method == 'DELETE':
#         dashboard.delete()
#         return JsonResponse({'message': 'Deleted'}, status=204)


# # Widget APIs
# @csrf_exempt
# def widget_list(request):
#     if request.method == 'GET':
#         widgets = Widget.objects.all()
#         data = [
#             {
#                 "id": w.id,
#                 "dashboard_id": w.dashboard.id,
#                 "title": w.title,
#                 "widget_type": w.widget_type,
#                 "config": w.config
#             } for w in widgets
#         ]
#         return JsonResponse(data, safe=False)
#     elif request.method == 'POST':
#         body = json.loads(request.body.decode('utf-8'))
#         dashboard = Dashboard.objects.get(pk=body.get('dashboard_id'))
#         widget = Widget.objects.create(
#             dashboard=dashboard,
#             title=body.get('title'),
#             widget_type=body.get('widget_type'),
#             config=body.get('config', '')
#         )
#         return JsonResponse({
#             "id": widget.id,
#             "dashboard_id": widget.dashboard.id,
#             "title": widget.title,
#             "widget_type": widget.widget_type,
#             "config": widget.config
#         }, status=201)

# @csrf_exempt
# def widget_detail(request, pk):
#     try:
#         widget = Widget.objects.get(pk=pk)
#     except Widget.DoesNotExist:
#         return JsonResponse({'error': 'Not found'}, status=404)

#     if request.method == 'GET':
#         data = {
#             "id": widget.id,
#             "dashboard_id": widget.dashboard.id,
#             "title": widget.title,
#             "widget_type": widget.widget_type,
#             "config": widget.config
#         }
#         return JsonResponse(data)
#     elif request.method == 'PUT':
#         body = json.loads(request.body.decode('utf-8'))
#         widget.title = body.get('title', widget.title)
#         widget.widget_type = body.get('widget_type', widget.widget_type)
#         widget.config = body.get('config', widget.config)
#         widget.save()
#         return JsonResponse({
#             "id": widget.id,
#             "dashboard_id": widget.dashboard.id,
#             "title": widget.title,
#             "widget_type": widget.widget_type,
#             "config": widget.config
#         })
#     elif request.method == 'DELETE':
#         widget.delete()
#         return JsonResponse({'message': 'Deleted'}, status=204)


# # KPIStore APIs
# @csrf_exempt
# def kpi_store_list(request):
#     if request.method == 'GET':
#         kpis = KPIStore.objects.all()
#         data = [
#             {
#                 "id": k.id,
#                 "kpi_name": k.kpi_name,
#                 "kpi_value": k.kpi_value,
#                 "timestamp": k.timestamp.isoformat()
#             } for k in kpis
#         ]
#         return JsonResponse(data, safe=False)
#     elif request.method == 'POST':
#         body = json.loads(request.body.decode('utf-8'))
#         kpi = KPIStore.objects.create(
#             kpi_name=body.get('kpi_name'),
#             kpi_value=body.get('kpi_value')
#         )
#         return JsonResponse({
#             "id": kpi.id,
#             "kpi_name": kpi.kpi_name,
#             "kpi_value": kpi.kpi_value,
#             "timestamp": kpi.timestamp.isoformat()
#         }, status=201)

# @csrf_exempt
# def kpi_store_detail(request, pk):
#     try:
#         kpi = KPIStore.objects.get(pk=pk)
#     except KPIStore.DoesNotExist:
#         return JsonResponse({'error': 'Not found'}, status=404)

#     if request.method == 'GET':
#         data = {
#             "id": kpi.id,
#             "kpi_name": kpi.kpi_name,
#             "kpi_value": kpi.kpi_value,
#             "timestamp": kpi.timestamp.isoformat()
#         }
#         return JsonResponse(data)
#     elif request.method == 'PUT':
#         body = json.loads(request.body.decode('utf-8'))
#         kpi.kpi_name = body.get('kpi_name', kpi.kpi_name)
#         kpi.kpi_value = body.get('kpi_value', kpi.kpi_value)
#         kpi.save()
#         return JsonResponse({
#             "id": kpi.id,
#             "kpi_name": kpi.kpi_name,
#             "kpi_value": kpi.kpi_value,
#             "timestamp": kpi.timestamp.isoformat()
#         })
#     elif request.method == 'DELETE':
#         kpi.delete()
#         return JsonResponse({'message': 'Deleted'}, status=204)


# # ExportLog APIs
# @csrf_exempt
# def export_log_list(request):
#     if request.method == 'GET':
#         exports = ExportLog.objects.all()
#         data = [
#             {
#                 "id": e.id,
#                 "report_execution_id": e.report_execution.id,
#                 "export_type": e.export_type,
#                 "exported_at": e.exported_at.isoformat(),
#                 "exported_by": e.exported_by
#             } for e in exports
#         ]
#         return JsonResponse(data, safe=False)
#     elif request.method == 'POST':
#         body = json.loads(request.body.decode('utf-8'))
#         exec_obj = ReportExecution.objects.get(pk=body.get('report_execution_id'))
#         export = ExportLog.objects.create(
#             report_execution=exec_obj,
#             export_type=body.get('export_type'),
#             exported_by=body.get('exported_by')
#         )
#         return JsonResponse({
#             "id": export.id,
#             "report_execution_id": export.report_execution.id,
#             "export_type": export.export_type,
#             "exported_at": export.exported_at.isoformat(),
#             "exported_by": export.exported_by
#         }, status=201)

# @csrf_exempt
# def export_log_detail(request, pk):
#     try:
#         export = ExportLog.objects.get(pk=pk)
#     except ExportLog.DoesNotExist:
#         return JsonResponse({'error': 'Not found'}, status=404)

#     if request.method == 'GET':
#         data = {
#             "id": export.id,
#             "report_execution_id": export.report_execution.id,
#             "export_type": export.export_type,
#             "exported_at": export.exported_at.isoformat(),
#             "exported_by": export.exported_by
#         }
#         return JsonResponse(data)
#     elif request.method == 'PUT':
#         body = json.loads(request.body.decode('utf-8'))
#         export.export_type = body.get('export_type', export.export_type)
#         export.exported_by = body.get('exported_by', export.exported_by)
#         export.save()
#         return JsonResponse({
#             "id": export.id,
#             "report_execution_id": export.report_execution.id,
#             "export_type": export.export_type,
#             "exported_at": export.exported_at.isoformat(),
#             "exported_by": export.exported_by
#         })
#     elif request.method == 'DELETE':
#         export.delete()
#         return JsonResponse({'message': 'Deleted'}, status=204)
# from io import BytesIO
# from reportlab.pdfgen import canvas
# from django.http import HttpResponse

# def exportlog_pdf(request, pk):
#     try:
#         export = ExportLog.objects.get(pk=pk)
#     except ExportLog.DoesNotExist:
#         return HttpResponse('ExportLog not found', status=404)

#     buffer = BytesIO()
#     p = canvas.Canvas(buffer)
#     p.drawString(100, 800, f"Export Log ID: {export.id}")
#     p.drawString(100, 780, f"Report Execution ID: {export.report_execution.id}")
#     p.drawString(100, 760, f"Export Type: {export.export_type}")
#     p.drawString(100, 740, f"Exported At: {export.exported_at}")
#     p.drawString(100, 720, f"Exported By: {export.exported_by}")
#     p.showPage()
#     p.save()

#     buffer.seek(0)
#     return HttpResponse(buffer, content_type='application/pdf')
import time
import csv
import json
import os
from datetime import datetime, timedelta
from io import BytesIO
from reportlab.pdfgen import canvas 
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404

from django.http import HttpResponse, FileResponse
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import (
    ReportDefinition, ReportExecution, Dashboard,
    Widget, KPIStore, ExportLog,
    ScholarshipProgram, Student, ScholarshipApplication, ApplicationDocument, Award
)
from .serializers import (
    ReportDefinitionSerializer, ReportExecutionSerializer,
    DashboardSerializer, WidgetSerializer, KPIStoreSerializer,
    ExportLogSerializer, ExecuteReportSerializer, ExportRequestSerializer,
    ScholarshipProgramSerializer, StudentSerializer, ScholarshipApplicationSerializer, ApplicationDocumentSerializer, AwardSerializer
)

class ScholarshipProgramViewSet(viewsets.ModelViewSet):
    queryset = ScholarshipProgram.objects.all()
    serializer_class = ScholarshipProgramSerializer

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class ScholarshipApplicationViewSet(viewsets.ModelViewSet):
    queryset = ScholarshipApplication.objects.all()
    serializer_class = ScholarshipApplicationSerializer

class ApplicationDocumentViewSet(viewsets.ModelViewSet):
    queryset = ApplicationDocument.objects.all()
    serializer_class = ApplicationDocumentSerializer

class AwardViewSet(viewsets.ModelViewSet):
    queryset = Award.objects.all()
    serializer_class = AwardSerializer

class ReportDefinitionViewSet(viewsets.ModelViewSet):
    queryset = ReportDefinition.objects.all()
    serializer_class = ReportDefinitionSerializer
    lookup_field = 'id'

    @action(detail=True, methods=['post'], url_path='execute')
    def execute(self, request, id=None):
        report = self.get_object()
        serializer = ExecuteReportSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        parameters = serializer.validated_data.get('parameters_json', {})
        executed_by_id = serializer.validated_data.get('executed_by_id')

        execution = ReportExecution.objects.create(
            report=report,
            executed_by_id=executed_by_id,
            parameters_json=parameters,
            status='running'
        )

        try:
            start_time = time.time()
            results = self._execute_report_query(report.query_json, parameters)
            execution_time = int((time.time() - start_time) * 1000)

            execution.result_json = results
            execution.status = 'success'
            execution.execution_time_ms = execution_time
            execution.save()

            return Response({
                'execution_id': execution.id,
                'status': 'success',
                'execution_time_ms': execution_time,
                'result_json': results
            })
        except Exception as e:
            execution.status = 'failed'
            execution.error_message = str(e)
            execution.save()
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def _execute_report_query(self, query_json, parameters):
        source = query_json.get('source', '')
        # Implement report for ScholarshipApplication
        if source == "ScholarshipApplication":
            queryset = ScholarshipApplication.objects.all()
            # Apply filters from parameters
            filters = parameters or {}
            if filters.get('status'):
                queryset = queryset.filter(status=filters['status'])
            # Group by program and count applications
            data = []
            grouped = {}
            for sa in queryset:
                prog_id = sa.program.id
                prog_name = sa.program.name
                if prog_id not in grouped:
                    grouped[prog_id] = {'program_id': prog_id, 'program_name': prog_name, 'total_applications': 0, 'total_amount': 0}
                grouped[prog_id]['total_applications'] += 1
                grouped[prog_id]['total_amount'] += float(sa.approved_amount)
            # Convert to list for JSON response
            for v in grouped.values():
                data.append(v)
            return data
        else:
            # No demo data: just return empty!
            return []

    @action(detail=True, methods=['post'], url_path='export')
    def export(self, request, id=None):
        report = self.get_object()
        serializer = ExportRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        export_type = serializer.validated_data['export_type']
        exported_by_id = serializer.validated_data['exported_by_id']
        parameters = serializer.validated_data.get('parameters_json', {})

        try:
            results = self._execute_report_query(report.query_json, parameters)
            execution = ReportExecution.objects.create(
                report=report,
                executed_by_id=exported_by_id,
                parameters_json=parameters,
                result_json=results,
                status='success'
            )
            file_path, file_size = self._generate_export_file(report, results, export_type)
            export_log = ExportLog.objects.create(
                report_execution=execution,
                export_type=export_type,
                exported_by_id=exported_by_id,
                file_path=file_path,
                file_size_bytes=file_size,
                expires_at=timezone.now() + timedelta(days=7)
            )

            return Response({
                'export_id': export_log.id,
                'file_path': file_path,
                'file_size_bytes': file_size,
                'export_type': export_type,
                'expires_at': export_log.expires_at
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def _generate_export_file(self, report, data, export_type):
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{report.name.replace(' ', '_')}_{timestamp}"
        export_dir = 'exports'
        os.makedirs(export_dir, exist_ok=True)

        if export_type == 'CSV':
            file_path = os.path.join(export_dir, f"{filename}.csv")
            with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
                if data:
                    writer = csv.DictWriter(csvfile, fieldnames=data[0].keys())
                    writer.writeheader()
                    writer.writerows(data)
        elif export_type == 'JSON':
            file_path = os.path.join(export_dir, f"{filename}.json")
            with open(file_path, 'w', encoding='utf-8') as jsonfile:
                json.dump(data, jsonfile, indent=2)
        else:
            file_path = os.path.join(export_dir, f"{filename}.{export_type.lower()}")
            with open(file_path, 'w') as file:
                file.write(json.dumps(data, indent=2))

        file_size = os.path.getsize(file_path)
        return file_path, file_size

class ReportExecutionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ReportExecution.objects.all()
    serializer_class = ReportExecutionSerializer
    lookup_field = 'id'

class DashboardViewSet(viewsets.ModelViewSet):
    queryset = Dashboard.objects.all()
    serializer_class = DashboardSerializer
    lookup_field = 'id'

class WidgetViewSet(viewsets.ModelViewSet):
    queryset = Widget.objects.all()
    serializer_class = WidgetSerializer
    lookup_field = 'id'

class KPIStoreViewSet(viewsets.ModelViewSet):
    queryset = KPIStore.objects.all()
    serializer_class = KPIStoreSerializer
    lookup_field = 'id'

    @action(detail=False, methods=['get'], url_path='summary')
    def summary(self, request):
        latest_kpi = KPIStore.objects.order_by('-metric_date').first()
        if not latest_kpi:
            return Response({'message': 'No KPIs available'}, status=status.HTTP_404_NOT_FOUND)

        kpis = KPIStore.objects.filter(metric_date=latest_kpi.metric_date)
        serializer = self.get_serializer(kpis, many=True)
        return Response({
            'date': latest_kpi.metric_date,
            'kpis': serializer.data
        }, status=status.HTTP_200_OK)

class ExportLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ExportLog.objects.filter(is_deleted=False)
    serializer_class = ExportLogSerializer
    lookup_field = 'id'

    @action(detail=True, methods=['get'], url_path='download')
    def download(self, request, pk=None):
        export_log = self.get_object()
        if export_log.expires_at and export_log.expires_at < timezone.now():
            return Response({'error': 'File has expired'}, status=status.HTTP_410_GONE)
        file_path = export_log.file_path
        if not file_path or not os.path.exists(file_path):
            return Response({'error': 'File not found'}, status=status.HTTP_404_NOT_FOUND)
        try:
            response = FileResponse(open(file_path, 'rb'))
            response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
            return response
        except Exception as e:
            return Response({'error': f'File failed to open: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def exportlog_pdf(request, pk=None):
    export_log = get_object_or_404(ExportLog, id=pk)
    buffer = BytesIO()
    p = canvas.Canvas(buffer)
    p.drawString(100, 800, f"Export Log ID: {export_log.id}")
    p.drawString(100, 780, f"Report ID: {export_log.report_execution.report.id}")
    p.drawString(100, 760, f"Export Type: {export_log.export_type}")
    p.drawString(100, 740, f"Exported At: {export_log.exported_at}")
    p.drawString(100, 720, f"Exported By ID: {export_log.exported_by_id}")
    p.showPage()
    p.save()
    buffer.seek(0)
    return HttpResponse(buffer, content_type='application/pdf')
