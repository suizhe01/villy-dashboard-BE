from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import pre_save
from django.dispatch import receiver
from _lib import panda
from cn.models import CN
from item.models import Item
from location.models import Location

# Create your models here.
class CNDTL(models.Model):
    autokey = models.CharField(primary_key=True, db_column='Autokey',max_length=32, editable=False, unique=True)
    headerautokey = models.ForeignKey(CN,
                                       models.DO_NOTHING,
                                       db_column='HeaderAutoKey',
                                       related_name='CNDTLCNAutokey'
                                       )
    itemcode = models.ForeignKey(Item,
                                       models.DO_NOTHING,
                                       db_column='ItemCode',
                                       related_name='CNDTLItemCodeAutokey',
                                       to_field='itemcode',
                                       null=True
                                       )
    location = models.ForeignKey(Location,
                                       models.DO_NOTHING,
                                       db_column='Location',
                                       related_name='CNDTLLocationAutokey'
                                       )
    focdtlkey = models.BigIntegerField(db_column='FOCDtlKey', null=True)
    seq = models.IntegerField(db_column='Seq', null=False)
    indent = models.SmallIntegerField(db_column='Indent',null=True)
    fontstyle = models.CharField(max_length=8,db_column='FontStyle', null= True)
    mainitem = models.CharField(max_length=5,db_column='MainItem', null= False)
    numbering = models.CharField(max_length=6,db_column='Numbering', null= True)
    batchno = models.CharField(max_length=20,db_column='BatchNo', null= True)
    description = models.CharField(max_length=100,db_column='Description', null= True)
    furtherdescription = models.CharField(max_length=255,db_column='FurtherDescription', null= True)
    posttostockdate = models.DateTimeField(db_column='PostToStockDate', null=True)
    projno = models.CharField(max_length=10,db_column='ProjNo', null= True)
    deptno = models.CharField(max_length=10,db_column='DeptNo', null= True)
    uom = models.CharField(max_length=8,db_column='UOM', null= True)
    useruom = models.CharField(max_length=8,db_column='UserUOM', null= True)
    qty = models.DecimalField(db_column='Qty', max_digits=25, decimal_places=8, null=True)
    rate = models.DecimalField(db_column='Rate', max_digits=25, decimal_places=8, null=True)
    smallestqty = models.DecimalField(db_column='SmallestQty', max_digits=25, decimal_places=8, null=True)
    focqty = models.DecimalField(db_column='focqty', max_digits=25, decimal_places=8, null=True)
    smallestunitprice = models.DecimalField(db_column='SmallestUnitPrice', max_digits=25, decimal_places=8, null=True)
    unitprice = models.DecimalField(db_column='UnitPrice', max_digits=25, decimal_places=8, null=True)
    unitcost = models.DecimalField(db_column='UnitCost', max_digits=25, decimal_places=8, null=True)
    focunitcost = models.DecimalField(db_column='FOCUnitCost', max_digits=25, decimal_places=8, null=True)
    discount = models.CharField(max_length=20,db_column='Discount', null= True)
    discountamt = models.DecimalField(db_column='DiscountAmt', max_digits=19, decimal_places=2, null=True)
    taxtype = models.CharField(max_length=14,db_column='TaxType', null= True)
    tax = models.DecimalField(db_column='Tax', max_digits=19, decimal_places=2, null=True)
    subtotal = models.DecimalField(db_column='SubTotal', max_digits=19, decimal_places=2, null=True)
    localsubtotal = models.DecimalField(db_column='LocalSubTotal', max_digits=19, decimal_places=2, null=True)
    bonuspoint = models.DecimalField(db_column='BonusPoint', max_digits=19, decimal_places=2, null=True)
    printout = models.CharField(max_length=1,db_column='PrintOut', null= False)
    dtltype = models.CharField(max_length=1,db_column='DtlType', null= True)
    calcbypercent = models.DecimalField(db_column='CalcByPercent', max_digits=18, decimal_places=6, null=True)
    addtosubtotal = models.CharField(max_length=1,db_column='AddToSubTotal', null= False)
    fromdoctype = models.CharField(max_length=2,db_column='FromDocType', null= True)
    fromdocno = models.CharField(max_length=255,db_column='FromDocNo', null= True)
    fromdocdtlkey = models.BigIntegerField(db_column='FromDocDtlKey', null=True)
    accno = models.CharField(max_length=12,db_column='AccNo', null= True)
    fulltransferoption = models.CharField(max_length=1,db_column='FullTransferOption', null= True)
    fulltransferfromdoclist = models.CharField(max_length=255,db_column='FullTransferFromDocList', null= True)
    serialnolist = models.CharField(max_length=255,db_column='SerialNoList', null= True)
    packagedockey = models.BigIntegerField(db_column='PackageDocKey', null=True)
    packagedtlkey = models.BigIntegerField(db_column='PackageDtlKey', null=True)
    subqty = models.DecimalField(db_column='SubQty', max_digits=25, decimal_places=8, null=True)
    iscalcbonuspoint = models.CharField(max_length=1,db_column='IsCalcBonusPoint', null= True)
    subtotalextax = models.DecimalField(db_column='SubTotalExTax', max_digits=19, decimal_places=2, null=True)
    localtax = models.DecimalField(db_column='LocalTax', max_digits=19, decimal_places=2, null=True)
    yourpono = models.CharField(max_length=25,db_column='YourPONo', null= True)
    yourpodate = models.DateTimeField(db_column='YourPODate', null=True)
    guid = models.CharField(max_length=32,db_column='Guid', null= False, unique=True)
    ruleno = models.BigIntegerField(db_column='RuleNo', null=True)
    goodsreturn = models.CharField(max_length=1,db_column='GoodsReturn', null= True)
    taxableamt = models.DecimalField(db_column='TaxableAmt', max_digits=19, decimal_places=2, null=True)
    taxadjustment = models.DecimalField(db_column='TaxAdjustment', max_digits=19, decimal_places=2, null=True)
    taxexportcountry = models.CharField(max_length=50,db_column='TaxExportCountry', null= True)
    localsubtotalextax = models.DecimalField(db_column='LocalSubTotalExTax', max_digits=19, decimal_places=2, null=True)
    extradiscountamt = models.DecimalField(db_column='ExtraDiscountAmt', max_digits=19, decimal_places=2, null=True)
    taxrate = models.DecimalField(db_column='TaxRate', max_digits=18, decimal_places=6, null=True)
    localtaxadjustment = models.DecimalField(db_column='LocalTaxAdjustment', max_digits=19, decimal_places=2, null=True)
    localtaxableamt = models.DecimalField(db_column='LocalTaxableAmt', max_digits=19, decimal_places=2, null=True)
    taxcurrencytax = models.DecimalField(db_column='TaxCurrencyTax', max_digits=19, decimal_places=2, null=True)
    taxcurrencytaxableamt = models.DecimalField(db_column='TaxCurrencyTaxableAmt', max_digits=19, decimal_places=2, null=True)
    taxpermitno = models.CharField(max_length=20,db_column='TaxPermitNo', null= True)
    salesexemptionno = models.CharField(max_length=60,db_column='SalesExemtionNo', null= True)
    supplypurchase = models.CharField(max_length=1,db_column='SupplyPurchase', null= True)
    tarrifcode = models.CharField(max_length=12,db_column='TarrifCode', null= True)
    desc2 = models.CharField(max_length=100,db_column='Desc2', null= True)

    class Meta:
        # app_label = 'MlItemmaster'
        managed = True
        db_table = "cndtl"
        ordering = ("autokey",)

    def __str__(self):
        return self.autokey
    
    def get_absolute_url(self):
        return f"/{self.autokey}/"
    
@receiver(pre_save, sender=CNDTL)
def pre_save_company(sender, instance, **kwargs):
    print("pre_save")
    # instance.updated_at = panda.panda_today()
    if instance.autokey == "":
        instance.autokey = panda.panda_uuid()

    if not instance.guid:
        instance.guid = panda.panda_uuid()