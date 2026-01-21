from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import pre_save
from django.dispatch import receiver
from _lib import panda
from django.utils import timezone

class LorryPlate(models.Model):
    lorryplateguid = models.CharField(primary_key=True, db_column='LorryPlateGuid',max_length=32, editable=False, unique=True)
    lorrynumber = models.CharField(max_length=30,db_column='LorryNumber', null= False, blank=False, unique=True)
    createdat = models.DateTimeField(db_column='CreatedAt', null=False)

    class Meta:
        # app_label = 'MlItemmaster'
        managed = True
        db_table = "lorryplate"
        ordering = ("lorryplateguid",)

    def __str__(self):
        return self.lorryplateguid
    
    def get_absolute_url(self):
        return f"/{self.lorryplateguid}/"

from datetime import datetime
@receiver(pre_save, sender=LorryPlate)
def pre_save_lorry_plate(sender, instance, **kwargs):
    print("pre_save")
    # instance.updated_at = panda.panda_today()
    if instance.lorryplateguid == "":
        instance.lorryplateguid = panda.panda_uuid()

    
    if not instance.createdat:
        # print(timezone.now())
        instance.createdat = datetime.now() 