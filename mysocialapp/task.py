from celery import shared_task
from .models import *
from PIL import Image as img
import io
from django.core.files.uploadedfile import SimpleUploadedFile


@shared_task
def make_thumbnail(record_pk):
    record = AppUser.objects.get(pk=record_pk)
    
    image = img.open(record.image)
    
    thumbnail = image.resize((50,50))
    thumbnail.save("test.jpg")
    
    byteArr = io.BytesIO()
    thumbnail.save(byteArr, format='jpeg')

    file = SimpleUploadedFile("thumb_"+str(record.image),byteArr.getvalue())
    record.thumbnail = file
    record.save()