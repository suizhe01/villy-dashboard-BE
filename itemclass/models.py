from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import pre_save
from django.dispatch import receiver
from _lib import panda
from company.models import Company

# Create your models here.
class ItemClass(models.Model):
    itemclassguid = models.CharField(primary_key=True, db_column='ItemClassGuid',max_length=32, editable=False, unique=True)
    companyautokey = models.ForeignKey(Company,
                                       models.DO_NOTHING,
                                       db_column='CompanyAutoKey',
                                       related_name='ItemClassCompanyAutokey'
                                       )
    itemclass = models.CharField(max_length=20,db_column='ItemClass', null= False, unique=True)
    description = models.CharField(max_length=40,db_column='Description', null= True)
    desc2 = models.CharField(max_length=40,db_column='Desc2', null= True)
    note = models.CharField(max_length=255,db_column='Note', null= True)
    lastupdate = models.IntegerField(db_column='LastUpdate', null=False)
    shortcode = models.CharField(max_length=8,db_column='ShortCode', null= True)
    markupratio = models.DecimalField(db_column='MarkupRatio', max_digits=18, decimal_places=6, null=True)
    guid = models.CharField(max_length=32,db_column='Guid', null= False, unique=True)

    class Meta:
        # app_label = 'MlItemmaster'
        managed = True
        db_table = "itemclass"
        ordering = ("itemclass",)

    def __str__(self):
        return self.itemclassguid
    
    def get_absolute_url(self):
        return f"/{self.itemclassguid}/"
    
@receiver(pre_save, sender=ItemClass)
def pre_save_company(sender, instance, **kwargs):
    print("pre_save")
    # instance.updated_at = panda.panda_today()
    if instance.itemclassguid == "":
        instance.itemclassguid = panda.panda_uuid()

    if instance.guid == "":
        instance.guid = panda.panda_uuid()