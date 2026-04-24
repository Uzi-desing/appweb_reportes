from django.db import models
from django.utils import timezone
from PIL import Image
from io import BytesIO
from .storage_backend import AzureMediaStorage
from django.core.files.base import ContentFile
import uuid

# Create your models here.
