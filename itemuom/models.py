from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import pre_save
from django.dispatch import receiver
from _lib import panda
from company.models import Company
from item.models import Item

# Create your models here.
class ItemUOM(models.Model):
    autokey = models.CharField(primary_key=True, db_column='Autokey',max_length=32, editable=False, unique=True)
    companyautokey = models.ForeignKey(Company,
                                       models.DO_NOTHING,
                                       db_column='CompanyAutoKey',
                                       related_name='ItemUOMCompanyAutokey'
                                       )
    itemcode = models.ForeignKey(Item,
                                models.DO_NOTHING,
                                db_column='ItemCode',
                                related_name='ItemUOMItemCode',
                                null=False,
                                to_field='itemcode'
                                )
    # New Column udf
    udfcalmethod = models.CharField(max_length=8,db_column='UdfCalMethod', null= True)
    udfcalrate = models.DecimalField(db_column='UdfCalRate', max_digits=2, decimal_places=2, null=True)
    udfispallet = models.SmallIntegerField(db_column='UdfPallet',default=0, null=True, blank=True)
    uom = models.CharField(max_length=8,db_column='UOM', null= False)
    rate = models.DecimalField(db_column='Rate', max_digits=25, decimal_places=8)
    shelf = models.CharField(max_length=20,db_column='Shelf', null= True)
    price = models.DecimalField(db_column='Price', max_digits=25, decimal_places=8, null=True)
    cost = models.DecimalField(db_column='Cost', max_digits=25, decimal_places=8, null=True)
    realcost = models.DecimalField(db_column='RealCost', max_digits=25, decimal_places=8, null=True)
    mostrecentlycost = models.DecimalField(db_column='MostRecentlyCost', max_digits=25, decimal_places=8, null=True)
    minsaleprice = models.DecimalField(db_column='MinSalePrice', max_digits=25, decimal_places=8, null=True)
    maxsaleprice = models.DecimalField(db_column='MaxSalePrice', max_digits=25, decimal_places=8, null=True)
    minpurchaseprice = models.DecimalField(db_column='MinPurchasePrice', max_digits=25, decimal_places=8, null=True)
    maxpurchaseprice = models.DecimalField(db_column='MaxPurchasePrice', max_digits=25, decimal_places=8, null=True)
    minqty = models.DecimalField(db_column='MinQty', max_digits=25, decimal_places=8, null=True)
    maxqty = models.DecimalField(db_column='MaxQty', max_digits=25, decimal_places=8, null=True)
    normallevel = models.DecimalField(db_column='NormalLevel', max_digits=25, decimal_places=8, null=True)
    reolelvel = models.DecimalField(db_column='ReOLevel', max_digits=25, decimal_places=8, null=True)
    reoqty = models.DecimalField(db_column='ReOQty', max_digits=25, decimal_places=8, null=True)
    foclevel = models.DecimalField(db_column='FOCLevel', max_digits=25, decimal_places=8, null=True)
    focqty = models.DecimalField(db_column='FOCQty', max_digits=25, decimal_places=8, null=True)
    bonuspointqty = models.DecimalField(db_column='BonusPointQty', max_digits=25, decimal_places=8, null=True)
    bonuspoint = models.DecimalField(db_column='Bonuspoint', max_digits=19, decimal_places=2, null=True)
    weight = models.DecimalField(db_column='Weight', max_digits=25, decimal_places=8, null=True)
    weightuom = models.CharField(max_length=8,db_column='WeightUOM', null= True)
    volume = models.DecimalField(db_column='Volume', max_digits=25, decimal_places=8, null=True)
    voumeuom = models.CharField(max_length=8,db_column='VolumeUOM', null= True)
    barcode = models.CharField(max_length=30,db_column='Barcode', null= True)
    lastupdate = models.IntegerField(db_column='LastUpdate', null= False)
    redeembonuspoint = models.DecimalField(db_column='RedeemBonuesPoint', max_digits=19, decimal_places=2, null=True)
    csgnqty = models.DecimalField(db_column='CSGNQty', max_digits=25, decimal_places=8, null=True)
    price2 = models.DecimalField(db_column='Price2', max_digits=25, decimal_places=8, null=True)
    guid = models.CharField(max_length=32,db_column='Guid', null= False, unique=False)
    price3 = models.DecimalField(db_column='Price3', max_digits=25, decimal_places=8, null=True)
    price4 = models.DecimalField(db_column='Price4', max_digits=25, decimal_places=8, null=True)
    price5 = models.DecimalField(db_column='Price5', max_digits=25, decimal_places=8, null=True)
    price6 = models.DecimalField(db_column='Price6', max_digits=25, decimal_places=8, null=True)
    markupratio = models.DecimalField(db_column='MarkupRatio', max_digits=18, decimal_places=6, null=True)
    markdownratio2 = models.DecimalField(db_column='MarkdownRatio2', max_digits=18, decimal_places=6, null=True)
    markdownratio3 = models.DecimalField(db_column='MarkdownRatio3', max_digits=18, decimal_places=6, null=True)
    markdownratio4 = models.DecimalField(db_column='MarkdownRatio4', max_digits=18, decimal_places=6, null=True)
    markdownratio5 = models.DecimalField(db_column='MarkdownRatio5', max_digits=18, decimal_places=6, null=True)
    markdownratio6 = models.DecimalField(db_column='MarkdownRatio6', max_digits=18, decimal_places=6, null=True)
    markdownratiominprice = models.DecimalField(db_column='MarkdownRatioMinPrice', max_digits=18, decimal_places=6, null=True)
    markdownratiomaxprice = models.DecimalField(db_column='MarkdownRatioMaxPrice', max_digits=18, decimal_places=6, null=True)
    
    class Meta:
        # app_label = 'MlItemmaster'
        managed = True
        db_table = "itemuom"
        ordering = ("uom",)

    def __str__(self):
        return self.autokey
    
    def get_absolute_url(self):
        return f"/{self.autokey}/"
    
@receiver(pre_save, sender=ItemUOM)
def pre_save_company(sender, instance, **kwargs):
    print("pre_save")
    # instance.updated_at = panda.panda_today()
    if instance.autokey == "":
        instance.autokey = panda.panda_uuid()