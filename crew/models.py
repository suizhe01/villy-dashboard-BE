from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import pre_save
from django.dispatch import receiver
from _lib import panda
from lorry.models import Lorry

class Crew(models.Model):
    crewguid = models.CharField(primary_key=True, db_column='CrewGuid',max_length=32, editable=False, unique=True)
    lorryguid = models.ForeignKey(Lorry,
                                       models.DO_NOTHING,
                                       db_column='LorryGuid',
                                       related_name='CrewLorryGuid'
                                       )
    crewid = models.CharField(max_length=50,db_column='CrewId', null=False)
    # crewname = models.CharField(max_length=88,db_column='CrewName', null= True)
    crewtype = models.CharField(max_length=55,db_column='CrewType', null= True)

    class Meta:
        # app_label = 'MlItemmaster'
        managed = True
        db_table = "crew"
        ordering = ("crewguid",)

    def __str__(self):
        return self.crewguid
    
    def get_absolute_url(self):
        return f"/{self.crewguid}/"
    
@receiver(pre_save, sender=Crew)
def pre_save_company(sender, instance, **kwargs):
    print("pre_save")
    # instance.updated_at = panda.panda_today()
    if instance.crewguid == "":
        instance.crewguid = panda.panda_uuid()