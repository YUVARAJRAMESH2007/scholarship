#
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
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .serializers import RegisterSerializer

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            
            # Fetch the linked student profile ID that was just created
            student_profile_id = None
            if hasattr(user, 'student_profile'):
                student_profile_id = user.student_profile.id

            return Response({
                "message": "Registration completed successfully",
                "token": token.key,
                "role": "student",
                "username": user.username,                         # NEW: Send username back
                "student_profile_id": student_profile_id           # NEW: Send student ID back
            }, status=status.HTTP_201_CREATED)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({"error": "Username and password fields are required"}, status=status.HTTP_400_BAD_REQUEST)

        # Authenticate details against Django auth subsystem
        user = authenticate(username=username, password=password)

        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            
            # Identify access role permissions tier
            role = "student"
            if user.is_superuser or user.is_staff:
                role = "admin"

            # Gather internal profile database ID reference context for a student account
            student_profile_id = None
            if hasattr(user, 'student_profile'):
                student_profile_id = user.student_profile.id

            return Response({
                "token": token.key,
                "role": role,
                "username": user.username,
                "student_profile_id": student_profile_id
            }, status=status.HTTP_200_OK)
        
        return Response({"error": "Invalid authentication credentials"}, status=status.HTTP_401_UNAUTHORIZED)
# Find your existing StudentViewSet and replace it with this:
class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    # Override the delete method to remove the core User account as well
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        # If the student has a linked login account, delete the account (which cascades and deletes the student profile)
        if instance.user:
            instance.user.delete()
        else:
            # If no login account exists, just delete the profile
            instance.delete()
        return Response({"message": "User deleted successfully"}, status=status.HTTP_204_NO_CONTENT)