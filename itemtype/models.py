from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import pre_save
from django.dispatch import receiver
from _lib import panda
from company.models import Company

class ItemType(models.Model):
    autokey = models.CharField(primary_key=True, db_column='Autokey',max_length=32, editable=False, unique=True, null=False)
    companyautokey = models.ForeignKey(Company,
                                       models.DO_NOTHING,
                                       db_column='CompanyAutoKey',
                                       related_name='ItemTypeCompanyAutokey'
                                       )
    itemtype = models.CharField(max_length=12,db_column='ItemType', null= False)
    description = models.CharField(max_length=40,db_column='Description', null= True)
    desc2 = models.CharField(max_length=40,db_column='Desc2', null= True)
    note = models.CharField(max_length=255,db_column='Note', null= True)
    lastupdate = models.IntegerField(db_column='LastUpdate', null=False)
    shortcode = models.CharField(max_length=8,db_column='ShortCode', null= True)
    markupratio = models.DecimalField(db_column='MarkupRatio' ,max_digits=18, decimal_places=6, null=True)
    guid = models.CharField(max_length=32,db_column='Guid', null= False, unique=True)

    class Meta:
        # app_label = 'MlItemmaster'
        managed = True
        db_table = "itemtype"
        ordering = ("itemtype",)

    def __str__(self):
        return self.autokey
    
    def get_absolute_url(self):
        return f"/{self.autokey}/"
    
@receiver(pre_save, sender=ItemType)
def pre_save_company(sender, instance, **kwargs):
    print("pre_save")
    # instance.updated_at = panda.panda_today()
    if instance.autokey == "":
        instance.autokey = panda.panda_uuid()