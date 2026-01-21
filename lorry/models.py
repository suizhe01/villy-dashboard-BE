from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import pre_save
from django.dispatch import receiver
from _lib import panda
from lorryplate.models import LorryPlate
from django.utils.timezone import timedelta

class Lorry(models.Model):
    lorryguid = models.CharField(primary_key=True, db_column='LorryGuid',max_length=32, editable=False, unique=True)
    lorrynumber = models.ForeignKey(LorryPlate,
                                       models.DO_NOTHING,
                                       db_column='LorryNumber',
                                       related_name='LorryLorryNumber',
                                       to_field='lorrynumber'
                                            )
    docdate = models.DateTimeField(db_column='DocDate', null=False)
    
    class Meta:
        # app_label = 'MlItemmaster'
        managed = True
        db_table = "lorry"
        ordering = ("lorryguid",)

    def __str__(self):
        return self.lorryguid
    
    def get_absolute_url(self):
        return f"/{self.lorryguid}/"
    
@receiver(pre_save, sender=Lorry)
def pre_save_company(sender, instance, **kwargs):
    print("pre_save")
    # instance.updated_at = panda.panda_today()
    if instance.lorryguid == "":
        instance.lorryguid = panda.panda_uuid()

    # Ensure `docdate` is not None before modifying
    if instance.docdate:
        instance.docdate = instance.docdate + timedelta(hours=8)