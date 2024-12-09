from django.contrib import admin
from .models import Property, Document
import magic

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('address', 'owner', 'created_at', 'updated_at')
    search_fields = ('address', 'owner__username')

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_property_uuid', 'document_type', 'uploaded_by', 
                   'uploaded_at', 'file_size', 'mime_type')
    list_filter = ('document_type', 'uploaded_at')
    readonly_fields = ('file_size', 'mime_type', 'uploaded_at', 'updated_at', 
                      'uploaded_by')
    exclude = ('file_size', 'mime_type')  # Hide these fields from the form

    def get_property_uuid(self, obj):
        return str(obj.property) if obj.property else None
    get_property_uuid.short_description = 'Property UUID'  # Column header in admin
    get_property_uuid.admin_order_field = 'property'  # Enable sorting

    def save_model(self, request, obj, form, change):
        if not obj.pk:  # If this is a new document
            obj.uploaded_by = request.user

        if 'file' in form.cleaned_data:
            file = form.cleaned_data['file']
            # Set file size
            obj.file_size = file.size
            
            # Set MIME type
            try:
                file_content = file.read(1024)
                obj.mime_type = magic.from_buffer(file_content, mime=True)
                file.seek(0)  # Reset file pointer after reading
            except Exception as e:
                obj.mime_type = file.content_type  # Fallback to HTTP content type
        
        super().save_model(request, obj, form, change)

    def get_readonly_fields(self, request, obj=None):
        if obj:  # If this is an existing document
            return self.readonly_fields
        # For new documents, don't show these as readonly
        return ('uploaded_at', 'updated_at')

    def formfield_for_dbfield(self, db_field, **kwargs):
        # Add help text for property field
        if db_field.name == 'property':
            kwargs['help_text'] = 'Enter a valid UUID. This can be any UUID and does not need to match an existing property.'
        return super().formfield_for_dbfield(db_field, **kwargs)