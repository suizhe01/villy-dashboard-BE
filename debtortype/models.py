from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import pre_save
from django.dispatch import receiver
from _lib import panda
from company.models import Company

class DebtorType(models.Model):
    autokey = models.CharField(primary_key=True, db_column='Autokey',max_length=32, editable=False, unique=True, null=False)
    companyautokey = models.ForeignKey(Company,
                                       models.DO_NOTHING,
                                       db_column='CompanyAutoKey',
                                       related_name='DebtorTypeCompanyAutokey'
                                       )
    debtortype = models.CharField(max_length=20,db_column='DebtorType', null= False)
    description = models.CharField(max_length=40,db_column='Description', null= True)
    desc2 = models.CharField(max_length=40,db_column='Desc2', null= True)
    isactive = models.CharField(max_length=1,db_column='IsActive', null= False)
    lastupdate = models.IntegerField(db_column='LastUpdate', null=False)
    guid = models.CharField(max_length=32,db_column='Guid', null= True, unique=False)

    class Meta:
        # app_label = 'MlItemmaster'
        managed = True
        db_table = "debtortype"
        ordering = ("debtortype",)

    def __str__(self):
        return self.autokey
    
    def get_absolute_url(self):
        return f"/{self.autokey}/"
    
@receiver(pre_save, sender=DebtorType)
def pre_save_company(sender, instance, **kwargs):
    print("pre_save")
    # instance.updated_at = panda.panda_today()
    if instance.autokey == "":
        instance.autokey = panda.panda_uuid()