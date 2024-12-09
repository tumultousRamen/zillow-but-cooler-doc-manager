from rest_framework import serializers
from .models import Document, Property
import uuid

class PropertySerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    
    class Meta:
        model = Property
        fields = ['id', 'address', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class DocumentSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    download_url = serializers.SerializerMethodField()
    property = serializers.CharField(required=False, allow_null=True, max_length=255)

    class Meta:
        model = Document
        fields = ['id', 'property', 'title', 'document_type', 'file', 
                 'uploaded_at', 'updated_at', 'file_size', 'mime_type', 
                 'download_url']
        read_only_fields = ['file_size', 'mime_type', 'download_url']

    def validate_property(self, value):
        if value:
            return value
            # try:
            #     return uuid.UUID(str(value))
            # except ValueError:
            #     raise serializers.ValidationError("Invalid UUID format")
        return None

    def get_download_url(self, obj):
        request = self.context.get('request')
        if obj.file and hasattr(obj.file, 'url'):
            return request.build_absolute_uri(obj.file.url)
        return None
    
    def to_representation(self, instance):
        """Keep the original representation format"""
        data = super().to_representation(instance)
        # Convert property UUID to string format if it exists
        if data['property']:
            data['property'] = str(data['property'])
        return data