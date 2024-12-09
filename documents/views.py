import magic
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Document, Property
from .serializers import DocumentSerializer, PropertySerializer

from django.views.generic import RedirectView
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def health_check(request):
    return HttpResponse("API is running", content_type="text/plain")

def api_root(request):
    return JsonResponse({
        'status': 'ok',
        'message': 'Real Estate Documents API is running',
        'endpoints': {
            'documents': '/api/documents/',
            'properties': '/api/properties/',
            'admin': '/admin/'
        }
    })

class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

    def perform_create(self, serializer):
        file_obj = self.request.FILES['file']
        mime_type = magic.from_buffer(file_obj.read(1024), mime=True)
        file_obj.seek(0)

        serializer.save(
            file_size=file_obj.size,
            mime_type=mime_type
        )

    @action(detail=True, methods=['get'])
    def preview(self, request, pk=None):
        document = self.get_object()
        return Response({
            'preview_url': document.file.url
        })

    def destroy(self, request, *args, **kwargs):
        document = self.get_object()
        document.file.delete(save=False)
        return super().destroy(request, *args, **kwargs)

class PropertyViewSet(viewsets.ModelViewSet):
    serializer_class = PropertySerializer
    queryset = Property.objects.all()  # Show all properties

    def perform_create(self, serializer):
        # Save without an owner
        serializer.save(owner=None)