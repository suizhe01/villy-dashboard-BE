from company.models import Company
from item.models import Item
from itemuom.models import ItemUOM
from datetime import datetime

def create_dob_dksh_item_itemuom(itemcode, description, uom, price, rate, unit_uom, unit_price, unit_rate):
    tempcompanyautokey = Company.objects.filter(name='Villy').first()
    filter_itemcode = Item.objects.filter(itemcode=itemcode)
    filter_uom = ItemUOM.objects.filter(itemcode=itemcode, uom=uom)

    mainsupplier = 'DOB_DKSH'
    itembrand = 'DKSH'
    itemclass = 'DKSH($)'

    if not filter_itemcode:
        save_new_item = Item(description=description, itemcode=itemcode, companyautokey=tempcompanyautokey, mainsupplier=mainsupplier, itembrand=itembrand, itemclass=itemclass, dockkey=1, dutyrate=1, costingmethod=0, lastmodified=datetime.now(), lastupdate=0)
        save_new_item.save()

    itemcode_instance = Item.objects.get(itemcode=itemcode)

    # Backfill items that were created before this import set the itemclass. An
    # itemclass that is already set is left alone, so an ERP reclassification is
    # never overwritten by this import.
    if not itemcode_instance.itemclass:
        itemcode_instance.itemclass = itemclass
        itemcode_instance.save()

    if not filter_uom:
        save_new_uom = ItemUOM(companyautokey=tempcompanyautokey, itemcode=itemcode_instance, uom=uom, rate=rate, price=price, lastupdate=0)
        save_new_uom.save()

    filter_unit_uom = ItemUOM.objects.filter(itemcode=itemcode, uom=unit_uom)
    if not filter_unit_uom:
        save_unit_uom = ItemUOM(companyautokey=tempcompanyautokey, itemcode=itemcode_instance, uom=unit_uom, rate=unit_rate, price=unit_price, lastupdate=0)
        save_unit_uom.save()
