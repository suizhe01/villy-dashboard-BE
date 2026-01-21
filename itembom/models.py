from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import pre_save
from django.dispatch import receiver
from _lib import panda
from company.models import Company
from item.models import Item

# Create your models here.
class ItemBOM(models.Model):
    autokey = models.CharField(primary_key=True, db_column='AutoKey',max_length=32, editable=False, unique=True)
    companyautokey = models.ForeignKey(Company,
                                       models.DO_NOTHING,
                                       db_column='CompanyAutoKey',
                                       related_name='ItemBOMCompanyAutokey'
                                       )
    itemcode = models.ForeignKey(Item,
                                       models.DO_NOTHING,
                                       db_column='ItemCode',
                                       related_name='ItemBOMItemCode',
                                       null=False
                                       )
    subitemcode = models.CharField(max_length=30,db_column='SubItemCode', null= False)
    qty = models.DecimalField(db_column='Qty', max_digits=25, decimal_places=8, null=False)
    overheadcost = models.DecimalField(db_column='OverHeadCost', max_digits=25, decimal_places=8, null=False)
    seq = models.IntegerField(db_column='Seq', null=False)
    costfraction = models.DecimalField(db_column='CostFraction', max_digits=19, decimal_places=2, null=True)

    class Meta:
        # app_label = 'MlItemmaster'
        managed = True
        db_table = "itembom"
        ordering = ("itemcode",)

    def __str__(self):
        return self.autokey
    
    def get_absolute_url(self):
        return f"/{self.autokey}/"
    
@receiver(pre_save, sender=ItemBOM)
def pre_save_company(sender, instance, **kwargs):
    print("pre_save")
    # instance.updated_at = panda.panda_today()
    if instance.autokey == "":
        instance.autokey = panda.panda_uuid()