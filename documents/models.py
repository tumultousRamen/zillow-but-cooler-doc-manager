from django.db import models
from django.contrib.auth.models import User
import uuid

class Property(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    address = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.address

class Document(models.Model):
    DOCUMENT_TYPES = [
        ('deed', 'Property Deed'),
        ('contract', 'Sales Contract'),
        ('inspection', 'Inspection Report'),
        ('other', 'Other'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    property = models.CharField(max_length=255, blank=True, null=True)
    title = models.CharField(max_length=255)
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPES)
    file = models.FileField(upload_to='property_documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    file_size = models.IntegerField()
    mime_type = models.CharField(max_length=100)

    def __str__(self):
        if self.property:
            return f"{self.title} - {self.property.address}"
        return self.title

    class Meta:
        ordering = ['-uploaded_at']