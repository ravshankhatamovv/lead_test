import base64
import uuid
from django.core.files.base import ContentFile
from rest_framework import serializers


class Base64FileField(serializers.FileField):
    """
    A custom DRF field to handle Base64-encoded files (images, PDFs, etc.).
    """
    
    ALLOWED_TYPES = ['jpg', 'jpeg', 'png', 'gif', 'pdf', 'doc', 'xlsx']
    
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:'):
            try:
                # Extract metadata and actual base64 data
                format, imgstr = data.split(';base64,')  
                ext = format.split('/')[-1].lower()  # Extract file extension
                
                if ext not in self.ALLOWED_TYPES:
                    raise serializers.ValidationError(f"Unsupported file format: {ext}")

                # Generate a unique filename
                file_name = f"{uuid.uuid4()}.{ext}"

                # Return decoded file as a Django ContentFile
                return ContentFile(base64.b64decode(imgstr), name=file_name)

            except (ValueError, IndexError, base64.binascii.Error):
                raise serializers.ValidationError("Invalid Base64-encoded file data")

        raise serializers.ValidationError("This field expects a valid Base64-encoded file string")