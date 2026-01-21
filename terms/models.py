from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import pre_save
from django.dispatch import receiver
from _lib import panda
from company.models import Company

# Create your models here.
class Terms(models.Model):
    autokey = models.CharField(primary_key=True, db_column='Autokey',max_length=32, editable=False, null=False)
    companyautokey = models.ForeignKey(Company,
                                       models.DO_NOTHING,
                                       db_column='CompanyAutokey',
                                       related_name='TermsCompanyAutoKey',
                                       null=False
                                       )
    displayterm = models.CharField(db_column='DisplayTerm',max_length=50,null=False, unique=True)
    terms = models.CharField(db_column='Terms',max_length=30,null=True)
    lastupdate = models.IntegerField(db_column='LastUpdate',null=False)
    termtype = models.CharField(db_column='Termtype',max_length=40,null=True)
    termdays = models.IntegerField(db_column='TermDays',null=True)
    discountdays = models.IntegerField(db_column='DiscountDays', null=True)
    discountpercent = models.DecimalField(db_column='DiscountPercent', null=True, max_digits=18, decimal_places=6)

    class Meta:
        # app_label = 'MlItemmaster'
        managed = True
        db_table = "terms"
        ordering = ("autokey",)

    def __str__(self):
        return self.autokey
    
    def get_absolute_url(self):
        return f"/{self.autokey}/"
    
@receiver(pre_save, sender=Terms)
def pre_save_company(sender, instance, **kwargs):
    print("pre_save")
    # instance.updated_at = panda.panda_today()
    if instance.autokey == "":
        instance.autokey = panda.panda_uuid()