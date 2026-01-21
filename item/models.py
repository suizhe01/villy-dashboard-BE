from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import pre_save
from django.dispatch import receiver
from _lib import panda
from company.models import Company
from datetime import datetime

# Create your models here.
class Item(models.Model):
    autokey = models.CharField(primary_key=True, db_column='Autokey',max_length=32, editable=False, unique=True)
    companyautokey = models.ForeignKey(Company,
                                       models.DO_NOTHING,
                                       db_column='CompanyAutoKey',
                                       related_name='ItemCompanyAutokey'
                                       )
    mainsupplier = models.CharField(max_length=30,db_column='MainSupplier', null= False)
    itemcode = models.CharField(max_length=30,db_column='ItemCode', null= False, unique=True, db_index=True)
    itemgroup = models.CharField(max_length=30,db_column='ItemGroup', null= True)
    itemtype = models.CharField(max_length=30,db_column='ItemType', null= True)
    itembrand = models.CharField(max_length=30,db_column='ItemBrand', null= True)
    itemcategory = models.CharField(max_length=30,db_column='ItemCategory', null= True)
    itemclass = models.CharField(max_length=30,db_column='ItemClass', null= True)
    taxtype = models.CharField(max_length=30,db_column='TaxType', null= True)
    dockkey = models.IntegerField(db_column='DockKey', null=False)
    description = models.CharField(max_length=100,db_column='Description', null= True)
    desc2 = models.CharField(max_length=100,db_column='Desc2', null= True)
    furtherdescription = models.CharField(max_length=255,db_column='FurtherDescription', null= True)
    assemblycost = models.DecimalField(db_column='AssemblyCost', max_digits=25, decimal_places=8, null=True)
    leadtime = models.CharField(max_length=40,db_column='LeadTime', null= True)
    stockcontrol = models.CharField(max_length=5,db_column='StockControl', null= False)
    hasserialno = models.CharField(max_length=5,db_column='HasSerialNo', null= False)
    hasbatchno = models.CharField(max_length=5,db_column='HasBatchNo', null= False)
    dutyrate = models.DecimalField(max_digits=18, decimal_places=6, db_column='DutyRate', null=False)
    note = models.CharField(max_length=255,db_column='Note', null= True)
    image = models.BinaryField(db_column='Image', null=True)
    costingmethod = models.SmallIntegerField(db_column='CostingMethod', null=False)
    salesuom = models.CharField(max_length=8,db_column='SalesUOM', null= False)
    purchaseuom = models.CharField(max_length=8,db_column='PurchaseUOM', null= False)
    reportuom = models.CharField(max_length=8,db_column='ReportUOM', null= False)
    lastmodified = models.DateTimeField(null=False, db_column='LastModified')
    lastmodifieduserid = models.CharField(max_length=10,db_column='LastModifiedUserID', null= False)
    createdtimestamp = models.DateTimeField(auto_now=True, editable=False, db_column='CreatedTimeStamp', null=False, )
    createduserid = models.CharField(max_length=10,db_column='CreatedUserID', null= False)
    isactive = models.CharField(max_length=5,db_column='IsActive', null= False)
    lastupdate = models.IntegerField(db_column='LastUpdate', null=False)
    snformatname = models.CharField(max_length=5,db_column='SNFormatName', null= True)
    iscalcbonuspoint = models.CharField(max_length=5,db_column='IsCalcBonusPoint', null= True)
    markupratio = models.DecimalField(db_column='MarkupRatio', max_digits=18, decimal_places=6, null=True)
    haspromoter = models.CharField(max_length=5,db_column='HasPromoter', null= False)
    globalcode = models.CharField(max_length=30,db_column='GlobalCode', null= True)
    leadtimeday = models.IntegerField(db_column='LeadTimeDay', null=True)
    externallink = models.CharField(max_length=255,db_column='ExternalLink', null= True)
    discontinued = models.CharField(max_length=5,db_column='Discontinued', null= False)
    autouomconversion = models.CharField(max_length=5,db_column='AutoUOMConversion', null= True)
    baseuom = models.CharField(max_length=8,db_column='BaseUOM', null= False)
    backordercontrol = models.CharField(max_length=5,db_column='BackOrderCOntrol', null= False)
    purchasetaxtype = models.CharField(max_length=14,db_column='PurchaseTaxType', null= True)
    tariffcode = models.CharField(max_length=12,db_column='TariffCode', null= True)
    guid = models.CharField(max_length=32,db_column='Guid', null= False, unique=False)
    issalesitem = models.CharField(max_length=5,db_column='IsSalesItem', null= True)
    ispurchaseitem = models.CharField(max_length=5,db_column='IsPurchaseItem', null= True)
    ispositem = models.CharField(max_length=5,db_column='IspOSItem', null= True)
    israwmeterialitem = models.CharField(max_length=5,db_column='IsRawMaterialItem', null= True)
    isfinishgoodsitem = models.CharField(max_length=5,db_column='IsFinishGoodsItem', null= True)
    imagefilename = models.CharField(max_length=120,db_column='ImageFileName', null= True)

    class Meta:
        # app_label = 'MlItemmaster'
        managed = True
        db_table = "item"
        ordering = ("itemcode",)

    def __str__(self):
        return self.autokey
    
    def get_absolute_url(self):
        return f"/{self.autokey}/"
    
@receiver(pre_save, sender=Item)
def pre_save_company(sender, instance, **kwargs):
    print("pre_save")
    # instance.updated_at = panda.panda_today()
    if instance.autokey == "":
        instance.autokey = panda.panda_uuid()
