from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import pre_save
from django.dispatch import receiver
from _lib import panda
from branch.models import Branch
from pi.models import PI
from item.models import Item
from location.models import Location

# Create your models here.
class PIDTL(models.Model):
    autokey = models.CharField(primary_key=True, db_column='AutoKey',max_length=32, editable=False, unique=True)
    headerautokey = models.ForeignKey(PI,
                                       models.DO_NOTHING,
                                       db_column='HeaderAutoKey',
                                       related_name='PIDTLPIAutokey'
                                       )
    itemcode = models.ForeignKey(Item,
                                       models.DO_NOTHING,
                                       db_column='ItemCode',
                                       related_name='PIDTLItemCodeAutokey',
                                       to_field='itemcode'
                                       )
    location = models.ForeignKey(Location,
                                       models.DO_NOTHING,
                                       db_column='Location',
                                       related_name='PIDTLLocationAutokey',
                                       to_field='location'
                                       )
    focdtlkey = models.BigIntegerField(db_column='FOCDtlKey', null=True)
    seq = models.IntegerField(db_column='Seq', null=False)
    indent = models.SmallIntegerField(db_column='Indent',null=True)
    fontstyle = models.CharField(max_length=8,db_column='FontStyle', null= True)
    mainitem = models.CharField(max_length=5,db_column='Mainitem', null= False)
    numbering = models.CharField(max_length=6,db_column='Numbering', null= True)
    batchno = models.CharField(max_length=20,db_column='BatchNo', null= True)
    description = models.CharField(max_length=100,db_column='Description', null= True)
    furtherdescription = models.CharField(max_length=255,db_column='FurtherDescription', null= True)
    projno = models.CharField(max_length=10,db_column='ProjNo', null= True)
    deptno = models.CharField(max_length=10,db_column='DeptNo', null= True)
    ourpono = models.CharField(max_length=20,db_column='OurPONo', null= True)
    ourpodate = models.DateTimeField(db_column='OurPODate', null=True)
    posttostockdate = models.DateTimeField(db_column='PostToStockDate', null=True)
    uom = models.CharField(max_length=8,db_column='UOM', null= True)
    useruom = models.CharField(max_length=8,db_column='UserUOM', null= True)
    qty = models.DecimalField(db_column='Qty', max_digits=25, decimal_places=8, null=True)
    rate = models.DecimalField(db_column='Rate', max_digits=25, decimal_places=8, null=True)
    smallestqty = models.DecimalField(db_column='SmallestQty', max_digits=25, decimal_places=8, null=True)
    transferedqty = models.DecimalField(db_column='TransferedQty', max_digits=25, decimal_places=8, null=False)
    focqty = models.DecimalField(db_column='FOCQty', max_digits=25, decimal_places=8, null=True)
    foctransferedqty = models.DecimalField(db_column='FOCTransferedQty', max_digits=25, decimal_places=8, null=True)
    smallestunitprice = models.DecimalField(db_column='SmallestUnitPrice', max_digits=25, decimal_places=8, null=True)
    unitprice = models.DecimalField(db_column='UnitPrice', max_digits=25, decimal_places=8, null=True)
    discount = models.CharField(max_length=20,db_column='Discount', null= True)
    discountamt = models.DecimalField(db_column='DiscountAmt', max_digits=19, decimal_places=2, null=True)
    taxtype = models.CharField(max_length=14,db_column='TaxType', null= True)
    tax = models.DecimalField(db_column='Tax', max_digits=19, decimal_places=2, null=True)
    subtotal = models.DecimalField(db_column='SubTotal', max_digits=19, decimal_places=2, null=True)
    localsubtotal = models.DecimalField(db_column='LocalSubTotal', max_digits=19, decimal_places=2, null=True)
    transferable = models.CharField(max_length=1,db_column='Transferable', null= False)
    printout = models.CharField(max_length=1,db_column='PrintOut', null= False)
    dtltype = models.CharField(max_length=1,db_column='DTLType', null= True)
    calcbypercent = models.DecimalField(db_column='CalcByPercent', max_digits=18, decimal_places=6, null=True)
    addtosubtotal = models.CharField(max_length=1,db_column='AddToSubTotal', null= False)
    fromdoctype = models.CharField(max_length=2,db_column='FromDocType', null= True)
    fromdocno = models.CharField(max_length=255,db_column='FromDocNo', null= True)
    fromdocdtlkey = models.BigIntegerField(db_column='FromDocDtlKey', null=True)
    fulltransferoption = models.CharField(max_length=1,db_column='FullTransferOption', null= True)
    foreigncharges = models.DecimalField(db_column='ForeignCharges', max_digits=25, decimal_places=8, null=True)
    localcharges = models.DecimalField(db_column='LocalCharges', max_digits=25, decimal_places=8, null=True)
    duty = models.DecimalField(db_column='Duty', max_digits=25, decimal_places=8, null=True)
    accno = models.CharField(max_length=12,db_column='AccNo', null= True)
    fulltransferfromdoclist = models.CharField(max_length=255,db_column='FullTransferFromDocList', null= True)
    serialnolist = models.CharField(max_length=255,db_column='SerialNoList', null= True)
    edtimateddeliverydate = models.CharField(max_length=20,db_column='EstimatedDeliveryDate', null= True)
    packagedockey = models.BigIntegerField(db_column='PackageDocKey', null=True)
    parentdtlkey = models.BigIntegerField(db_column='ParentDtlKey', null=True)
    subqty = models.DecimalField(db_column='SubQty', max_digits=25, decimal_places=8, null=True)
    subtotalextax = models.DecimalField(db_column='SubTotalExTax', max_digits=19, decimal_places=2, null=True)
    localtax = models.DecimalField(db_column='LocalTax', max_digits=19, decimal_places=2, null=True)
    guid = models.CharField(max_length=32,db_column='Guid', null= False, unique=True)
    deliverydate = models.DateTimeField(db_column='DeliveryDate', null=True)
    cnamt = models.DecimalField(db_column='CNAmt', max_digits=19, decimal_places=2, null=True)
    taxpermitno = models.CharField(max_length=20,db_column='TaxPermitNo', null= True)
    taxableamt = models.DecimalField(db_column='TaxableAmt', max_digits=19, decimal_places=2, null=True)
    taxadjustment = models.DecimalField(db_column='TaxAdjustment', max_digits=19, decimal_places=2, null=True)
    localsubtotalextax = models.DecimalField(db_column='LocalSubTotalExTax', max_digits=19, decimal_places=2, null=True)
    extradiscountamt = models.DecimalField(db_column='ExtraDiscountAmt', max_digits=19, decimal_places=2, null=True)
    taxrate = models.DecimalField(db_column='TaxRate', max_digits=18, decimal_places=6, null=True)
    localtaxadjustment = models.DecimalField(db_column='LocalTaxAdjustment', max_digits=19, decimal_places=2, null=True)
    localtaxableamt = models.DecimalField(db_column='LocalTaxableAmt', max_digits=19, decimal_places=2, null=True)
    taxcurrencytax = models.DecimalField(db_column='TaxCurrencyTax', max_digits=19, decimal_places=2, null=True)
    taxcurrencytaxableamt = models.DecimalField(db_column='TaxCurrencyTaxableAmt', max_digits=19, decimal_places=2, null=True)
    salesexamtionno = models.CharField(max_length=60,db_column='SalesExamtionNo', null= True)
    tariffcode = models.CharField(max_length=12,db_column='TariffCode', null= True)
    desc2 = models.CharField(max_length=100,db_column='Desc2', null= True)

    class Meta:
        # app_label = 'MlItemmaster'
        managed = True
        db_table = "pidtl"
        ordering = ("autokey",)

    def __str__(self):
        return self.autokey
    
    def get_absolute_url(self):
        return f"/{self.autokey}/"
    
@receiver(pre_save, sender=PIDTL)
def pre_save_company(sender, instance, **kwargs):
    print("pre_save")
    # instance.updated_at = panda.panda_today()
    if not instance.autokey:
        instance.autokey = panda.panda_uuid()

    if not instance.guid:
        instance.guid = panda.panda_uuid()