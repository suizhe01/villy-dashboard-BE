from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import pre_save
from django.dispatch import receiver
from _lib import panda
from commissionitemclass.models import CommissionItemClass
from crewrate.models import CrewRate

class CrewRateDtl(models.Model):
    crewratedtlguid = models.CharField(primary_key=True, db_column='CrewRateDtlGuid',max_length=32, editable=False, unique=True)
    commissionitemclassguid = models.ForeignKey(CommissionItemClass,
                                       models.DO_NOTHING,
                                       db_column='CommissionItemClassGuid',
                                       related_name='CrewRateDtlCommissionItemClassGuid'
                                       )
    crewrateguid = models.ForeignKey(CrewRate,
                                       models.DO_NOTHING,
                                       db_column='CrewRateGuid',
                                       related_name='CrewRateDtlCrewRateGuid'
                                       )
    crewtype = models.CharField(max_length=50,db_column='CrewType', null= True)
    commvalue = models.DecimalField(db_column='CommValue', max_digits=8, decimal_places=7, null=True)

    class Meta:
        # app_label = 'MlItemmaster'
        managed = True
        db_table = "crewratedtl"
        ordering = ("crewratedtlguid",)

    def __str__(self):
        return self.crewratedtlguid
    
    def get_absolute_url(self):
        return f"/{self.crewratedtlguid}/"
    
@receiver(pre_save, sender=CrewRateDtl)
def pre_save_company(sender, instance, **kwargs):
    # print("pre_save")
    # instance.updated_at = panda.panda_today()
    if instance.crewratedtlguid == "":
        instance.crewratedtlguid = panda.panda_uuid()