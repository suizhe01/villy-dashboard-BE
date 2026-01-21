from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import pre_save
from django.dispatch import receiver
from _lib import panda
from adj.models import ADJ
from item.models import Item
from location.models import Location

# Create your models here.
class ADJDTL(models.Model):
    autokey = models.CharField(primary_key=True, db_column='Autokey',max_length=32, editable=False, unique=True)
    adjautokey = models.ForeignKey(ADJ,
                                       models.DO_NOTHING,
                                       db_column='ADJAutokey',
                                       related_name='ADJDTLCNAutokey'
                                       )
    itemcode = models.ForeignKey(Item,
                                       models.DO_NOTHING,
                                       db_column='ItemCode',
                                       related_name='ADJDTLItemCodeAutokey',
                                       null=True
                                       )
    location = models.ForeignKey(Location,
                                       models.DO_NOTHING,
                                       db_column='Location',
                                       related_name='ADJDTLLocationAutokey',
                                       null=True
                                       )
    seq = models.IntegerField(db_column='Seq', null=False)
    numbering = models.CharField(max_length=6,db_column='Numbering', null= True)
    batchno = models.CharField(max_length=20,db_column='BatchNo', null= True)
    description = models.CharField(max_length=100,db_column='Description', null= True)
    furtherdescription = models.CharField(max_length=255,db_column='FurtherDescription', null= True)
    projno = models.CharField(max_length=10,db_column='ProjNo', null= True)
    deptno = models.CharField(max_length=10,db_column='DeptNo', null= True)
    qty = models.DecimalField(db_column='Qty', max_digits=25, decimal_places=8, null=True)
    uom = models.CharField(max_length=8,db_column='UOM', null= True)
    unitcost = models.DecimalField(db_column='UnitCost', max_digits=25, decimal_places=8, null=True)
    subtotal = models.DecimalField(db_column='SubTotal', max_digits=19, decimal_places=2, null=True)
    printout = models.CharField(max_length=1,db_column='PrintOut', null= False)
    serialnolist = models.CharField(max_length=255,db_column='SerialNoList', null= True)
    guid = models.CharField(max_length=32,db_column='Guid', null= False, unique=True)
    desc2 = models.CharField(max_length=100,db_column='Desc2', null= True)

    class Meta:
        # app_label = 'MlItemmaster'
        managed = True
        db_table = "adjdtl"
        ordering = ("autokey",)

    def __str__(self):
        return self.autokey
    
    def get_absolute_url(self):
        return f"/{self.autokey}/"
    
@receiver(pre_save, sender=ADJDTL)
def pre_save_company(sender, instance, **kwargs):
    print("pre_save")
    # instance.updated_at = panda.panda_today()
    if instance.autokey == "":
        instance.autokey = panda.panda_uuid()