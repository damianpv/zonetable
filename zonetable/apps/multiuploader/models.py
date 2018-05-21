from django.db import models
import random
from django.conf import settings

from zonetable.apps.directory.models import Directory

#try:
#    storage = settings.MULTI_IMAGES_FOLDER+'/'
#except AttributeError:
#    storage = 'multiuploader_images/'

class MultiuploaderImage(models.Model):
    """Model for storing uploaded photos"""

    def url(self,filename):
        #ruta = "multiuploader_images/a.jpg"
        ruta = "multiuploader_images/%s/%s"%(self.directory_id, filename)
        return ruta

    directory = models.ForeignKey(Directory)
    filename = models.CharField(max_length=60, blank=True, null=True)
    image = models.FileField(upload_to=url)
    key_data = models.CharField(max_length=90, blank=True, null=True)
    upload_date = models.DateTimeField(auto_now_add=True)

    @property
    def key_generate(self):
        """returns a string based unique key with length 80 chars"""
        while 1:
            key = str(random.getrandbits(256))
            try:
                MultiuploaderImage.objects.get(key=key)
            except:
                return key

    def __unicode__(self):
        return self.image.name

