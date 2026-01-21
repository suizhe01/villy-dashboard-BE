from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import pre_save
from django.dispatch import receiver
from _lib import panda

# Create your models here.
class CrewRate(models.Model):
    crewrateguid = models.CharField(primary_key=True, db_column='CrewRateGuid',max_length=32, editable=False, unique=True)
    crewid = models.CharField(max_length=50,db_column='CrewId', unique=True)
    crewname = models.CharField(max_length=88,db_column='CrewName', null= True)
    isactive = models.CharField(db_column ='IsActive',max_length=1, null=False)

    class Meta:
        # app_label = 'MlItemmaster'
        managed = True
        db_table = "crewrate"
        ordering = ("crewrateguid",)

    def __str__(self):
        return self.crewrateguid
    
    def get_absolute_url(self):
        return f"/{self.crewrateguid}/"
    
@receiver(pre_save, sender=CrewRate)
def pre_save_company(sender, instance, **kwargs):
    print("pre_save")
    # instance.updated_at = panda.panda_today()
    if instance.crewrateguid == "":
        instance.crewrateguid = panda.panda_uuid()