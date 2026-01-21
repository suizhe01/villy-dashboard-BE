from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import pre_save
from django.dispatch import receiver
from _lib import panda
from itemclass.models import ItemClass

# Create your models here.
class CommissionItemClass(models.Model):
    commissionitemclassguid = models.CharField(primary_key=True, db_column='CommissionItemClassGuid',max_length=32, editable=False, unique=True)
    itemclassguid = models.ForeignKey(ItemClass,
                                       models.DO_NOTHING,
                                       db_column='ItemClassGuid',
                                       related_name='CommissionItemClassItemClassGuid'
                                       )
    commtype = models.CharField(max_length=20, db_column='CommType', null=False)

    class Meta:
        managed = True
        db_table = 'commissionitemclass'
        ordering = ('commissionitemclassguid',)
    
    def __str__(self):
        return self.commissionitemclassguid
    
    def get_absolute_url(self):
        return f"/{self.commissionitemclassguid}/"
    
@receiver(pre_save, sender=CommissionItemClass)
def pre_save_company(sender, instance, **kwargs):
    print("pre_save")
    # instance.updated_at = panda.panda_today()
    if instance.commissionitemclassguid == "":
        instance.commissionitemclassguid = panda.panda_uuid()
    