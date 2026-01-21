from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import pre_save
from django.dispatch import receiver
from _lib import panda
from crew.models import Crew
from itemclass.models import ItemClass

class Crewdtl(models.Model):
    crewdtlguid = models.CharField(primary_key=True, db_column='CrewDtlGuid',max_length=32, editable=False, unique=True)
    crewguid = models.ForeignKey(Crew,
                                       models.DO_NOTHING,
                                       db_column='CrewGuid',
                                       related_name='CrewDtlCrewGuid'
                                       )
    itemclass = models.ForeignKey(ItemClass,
                                       models.DO_NOTHING,
                                       db_column='ItemClass',
                                       related_name='CrewdtlItemClass',
                                       to_field='itemclass'
                                            )
    commtype = models.CharField(max_length=100,db_column='CommType', null= True)
    commvalue = models.DecimalField(db_column='CommValue', max_digits=8, decimal_places=7, null=True)
    documentsum = models.DecimalField(db_column='DocumentSum', max_digits=25, decimal_places=4, null=True)
    calculatedcomm = models.DecimalField(db_column='CalculatedComm', max_digits=25, decimal_places=8, null=True)
    totalqty = models.DecimalField(db_column='TotalQty', max_digits=25, decimal_places=8, null=True)
    totalamount =models.DecimalField(db_column='TotalAmount', max_digits=20, decimal_places=4, null=True)
    calculationtype = models.CharField(max_length=100,db_column='CalculationType', null= True)
    share = models.SmallIntegerField(db_column='Share', null=True)
    uom = models.CharField(max_length=10,db_column='Uom', null= True)
    udfcalmethod = models.CharField(max_length=8,db_column='UdfCalMethod', null= True)
    udfcalrate = models.DecimalField(db_column='UdfCalRate', max_digits=2, decimal_places=2, null=True)

    class Meta:
        # app_label = 'MlItemmaster'
        managed = True
        db_table = "crewdtl"
        ordering = ("crewdtlguid",)

    def __str__(self):
        return self.crewdtlguid
    
    def get_absolute_url(self):
        return f"/{self.crewdtlguid}/"
    
@receiver(pre_save, sender=Crewdtl)
def pre_save_company(sender, instance, **kwargs):
    print("pre_save")
    # instance.updated_at = panda.panda_today()
    if instance.crewdtlguid == "":
        instance.crewdtlguid = panda.panda_uuid()
