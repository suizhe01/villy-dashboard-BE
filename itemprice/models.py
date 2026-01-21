from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import pre_save
from django.dispatch import receiver
from _lib import panda
from company.models import Company
from item.models import Item

# Create your models here.
class ItemPrice(models.Model):
    autokey = models.CharField(primary_key=True, db_column='Autokey',max_length=32, editable=False, unique=True)
    companyautokey = models.ForeignKey(Company,
                                       models.DO_NOTHING,
                                       db_column='CompanyAutoKey',
                                       related_name='ItemPriceCompanyAutokey'
                                       )
    itemcode = models.ForeignKey(Item,
                                       models.DO_NOTHING,
                                       db_column='ItemCode',
                                       related_name='ItemPriceItemCode',
                                       null=True
                                       )
    uom = models.CharField(max_length=8,db_column='UOM', null= False)
    pricecategory = models.CharField(max_length=12,db_column='PriceCategory', null= True)
    accno = models.CharField(max_length=12,db_column='AccNo', null= True)
    suppcustitemcode = models.CharField(max_length=30,db_column='SuppCustItemCode', null= True)
    ref = models.CharField(max_length=80,db_column='Ref', null= True)
    usefixedprice = models.CharField(max_length=1,db_column='UseFixedPrice', null= False)
    fixedprice = models.DecimalField(db_column='FixedPrice', max_digits=25, decimal_places=8, null=True)
    fixeddetaildiscount = models.CharField(max_length=20,db_column='FixedDetailDiscount', null= True)
    qty1 = models.DecimalField(db_column='Qty1', max_digits=25, decimal_places=8, null=True)
    price1 = models.DecimalField(db_column='Price1', max_digits=25, decimal_places=8, null=True)
    detaildiscount1 = models.CharField(db_column='DetailDiscount1', max_length=20, null=True)
    qty2 = models.DecimalField(db_column='Qty2', max_digits=25, decimal_places=8, null=True)
    price2 = models.DecimalField(db_column='Price2', max_digits=25, decimal_places=8, null=True)
    detaildiscount2 = models.CharField(db_column='DetailDiscount2', max_length=20, null=True)
    qty3 = models.DecimalField(db_column='Qty3', max_digits=25, decimal_places=8, null=True)
    price3 = models.DecimalField(db_column='Price3', max_digits=25, decimal_places=8, null=True)
    detaildiscount3 = models.CharField(db_column='DetailDiscount3', max_length=20, null=True)
    qty4 = models.DecimalField(db_column='Qty4', max_digits=25, decimal_places=8, null=True)
    price4 = models.DecimalField(db_column='Price4', max_digits=25, decimal_places=8, null=True)
    detaildiscount4 = models.CharField(db_column='DetailDiscount4', max_length=20, null=True)
    foclevel = models.DecimalField(db_column='FOCLevel', max_digits=25, decimal_places=8, null=True)
    focqty = models.DecimalField(db_column='FOCQty', max_digits=25, decimal_places=8, null=True)
    bonuspointqty =models.DecimalField(db_column='BonusPointQty', max_digits=25, decimal_places=8, null=True)
    bonuspoint = models.DecimalField(db_column='BonusPoint', max_digits=19, decimal_places=2, null=True)
    lastupdate = models.IntegerField(db_column='LastUpdate', null=False)
    guid = models.CharField(max_length=32,db_column='Guid', null= False, unique=True)

    class Meta:
        # app_label = 'MlItemmaster'
        managed = True
        db_table = "itemprice"
        ordering = ("pricecategory",)

    def __str__(self):
        return self.autokey
    
    def get_absolute_url(self):
        return f"/{self.autokey}/"
    
@receiver(pre_save, sender=ItemPrice)
def pre_save_company(sender, instance, **kwargs):
    print("pre_save")
    # instance.updated_at = panda.panda_today()
    if instance.autokey == "":
        instance.autokey = panda.panda_uuid()