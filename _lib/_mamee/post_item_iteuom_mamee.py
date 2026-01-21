from company.models import Company
from item.models import Item
from itemuom.models import ItemUOM
from datetime import datetime

def create_mamee_item_itemuom_invoice(itemcode, description, uom, price, rate, unit_uom, unit_price, unit_rate):
    tempcompanyautokey = Company.objects.filter(name='Villy').first()
    filter_itemcode = Item.objects.filter(itemcode=itemcode)
    filter_uom = ItemUOM.objects.filter(itemcode=itemcode, uom=uom)
    
    mainsupplier='Mamee'

    if not filter_itemcode:
        save_new_item = Item(description=description,itemcode=itemcode,companyautokey=tempcompanyautokey,mainsupplier=mainsupplier, dockkey=1, dutyrate=1, costingmethod=0, lastmodified=datetime.now(), lastupdate=0)
        save_new_item.save()
        itemcode_intance = Item.objects.get(itemcode=itemcode)

        filter_unit_uom = ItemUOM.objects.filter(itemcode=itemcode, uom=unit_uom)
        if not filter_uom:
            save_new_uom = ItemUOM(companyautokey=tempcompanyautokey,itemcode=itemcode_intance,uom=uom,rate=rate,price=price,lastupdate=0)
            save_new_uom.save()

        if not filter_unit_uom:
            save_unit_uom = ItemUOM(companyautokey=tempcompanyautokey,itemcode=itemcode_intance,uom=unit_uom,rate=unit_rate,price=unit_price,lastupdate=0)
            save_unit_uom.save()
    else:
        itemcode_intance = Item.objects.get(itemcode=itemcode)
        if not filter_uom:
            save_new_uom = ItemUOM(companyautokey=tempcompanyautokey,itemcode=itemcode_intance,uom=uom,rate=rate,price=price,lastupdate=0)
            save_new_uom.save()

        filter_unit_uom = ItemUOM.objects.filter(itemcode=itemcode, uom=unit_uom)
        if not filter_unit_uom:
            save_unit_uom = ItemUOM(companyautokey=tempcompanyautokey,itemcode=itemcode_intance,uom=unit_uom,rate=unit_rate,price=unit_price,lastupdate=0)
            save_unit_uom.save()

def create_mameee_item_itemuom_cn(item_code,description,uom,price,rate,unit_uom,unit_price,unit_rate):
    tempcompanyautokey = Company.objects.filter(name='Villy').first()
    filter_itemcode = Item.objects.filter(itemcode=item_code)
    filter_uom = ItemUOM.objects.filter(itemcode=item_code, uom=uom)
    
    mainsupplier='Mamee'

    if not filter_itemcode:
        save_new_item = Item(description=description,itemcode=item_code,companyautokey=tempcompanyautokey,mainsupplier=mainsupplier, dockkey=1, dutyrate=1, costingmethod=0, lastmodified=datetime.now(), lastupdate=0)
        save_new_item.save()
        itemcode_intance = Item.objects.get(itemcode=item_code)

        filter_unit_uom = ItemUOM.objects.filter(itemcode=item_code, uom=unit_uom)
        if not filter_uom:
            save_new_uom = ItemUOM(companyautokey=tempcompanyautokey,itemcode=itemcode_intance,uom=uom,rate=rate,price=price,lastupdate=1)
            save_new_uom.save()

        if not filter_unit_uom:
            save_unit_uom = ItemUOM(companyautokey=tempcompanyautokey,itemcode=itemcode_intance,uom=unit_uom,rate=unit_rate,price=unit_price,lastupdate=1)
            save_unit_uom.save()

    else:
        itemcode_intance = Item.objects.get(itemcode=item_code)
        if not filter_uom:
            save_new_uom = ItemUOM(companyautokey=tempcompanyautokey,itemcode=itemcode_intance,uom=uom,rate=rate,price=price,lastupdate=1)
            save_new_uom.save()

        filter_unit_uom = ItemUOM.objects.filter(itemcode=item_code, uom=unit_uom)
        if not filter_unit_uom:
            save_unit_uom = ItemUOM(companyautokey=tempcompanyautokey,itemcode=itemcode_intance,uom=unit_uom,rate=unit_rate,price=unit_price,lastupdate=1)
            save_unit_uom.save()