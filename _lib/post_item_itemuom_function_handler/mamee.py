from company.models import Company
from item.models import Item
from itemuom.models import ItemUOM
from datetime import datetime

def create_mamee_item_itemuom_purchase(itemcode, description, uom, price, rate, unit_uom, unit_price, unit_rate, bundle_uom, bundle_price, bundle_rate):
    tempcompanyautokey = Company.objects.filter(name='Villy').first()
    filter_itemcode = Item.objects.filter(itemcode=itemcode)
    mainsupplier='Mamee'
    filter_unit_uom = ItemUOM.objects.filter(itemcode=itemcode, uom=unit_uom)
    filter_bundle_uom = ItemUOM.objects.filter(itemcode=itemcode, uom=bundle_uom)
    filter_carton_uom = ItemUOM.objects.filter(itemcode=itemcode, uom=uom)
    last_update= 0

    if not filter_itemcode:
        save_new_item = Item(description=description,itemcode=itemcode,companyautokey=tempcompanyautokey,mainsupplier=mainsupplier, dockkey=1, dutyrate=1, costingmethod=0, lastmodified=datetime.now(), lastupdate=last_update)
        save_new_item.save()
        
        itemcode_intance = Item.objects.get(itemcode=itemcode)
        if not filter_unit_uom:
            save_unit_uom = ItemUOM(companyautokey=tempcompanyautokey,itemcode=itemcode_intance,uom=unit_uom,rate=unit_rate,price=unit_price,lastupdate=last_update)
            save_unit_uom.save()
        if not filter_bundle_uom:
            save_bundle_uom = ItemUOM(companyautokey=tempcompanyautokey,itemcode=itemcode_intance,uom=bundle_uom,rate=bundle_rate,price=bundle_price,lastupdate=last_update)
            save_bundle_uom.save()
        if not filter_carton_uom:
            save_carton_uom = ItemUOM(companyautokey=tempcompanyautokey,itemcode=itemcode_intance,uom=uom,rate=rate,price=price,lastupdate=last_update)
            save_carton_uom.save()

    else:
        itemcode_intance = Item.objects.get(itemcode=itemcode)
        if not filter_unit_uom:
            save_unit_uom = ItemUOM(companyautokey=tempcompanyautokey,itemcode=itemcode_intance,uom=unit_uom,rate=unit_rate,price=unit_price,lastupdate=last_update)
            save_unit_uom.save()
        if not filter_bundle_uom:
            save_bundle_uom = ItemUOM(companyautokey=tempcompanyautokey,itemcode=itemcode_intance,uom=bundle_uom,rate=bundle_rate,price=bundle_price,lastupdate=last_update)
            save_bundle_uom.save()
        if not filter_carton_uom:
            save_carton_uom = ItemUOM(companyautokey=tempcompanyautokey,itemcode=itemcode_intance,uom=uom,rate=rate,price=price,lastupdate=last_update)
            save_carton_uom.save()

    
# def create_mamee_item_itemuom_invoice(itemcode, description, uom, price, rate, unit_uom, unit_price, unit_rate):
#     tempcompanyautokey = Company.objects.filter(name='Villy').first()
#     filter_itemcode = Item.objects.filter(itemcode=itemcode)
#     filter_uom = ItemUOM.objects.filter(itemcode=itemcode, uom=uom)
#     filter_unit_uom = ItemUOM.objects.filter(itemcode=itemcode, uom=unit_uom)
#     mainsupplier='Mamee'

#     if not filter_itemcode:
#         save_new_item = Item(description=description,itemcode=itemcode,companyautokey=tempcompanyautokey,mainsupplier=mainsupplier, dockkey=1, dutyrate=1, costingmethod=0, lastmodified=datetime.now(), lastupdate=0)
#         save_new_item.save()
#         itemcode_intance = Item.objects.get(itemcode=itemcode)

#         if not filter_uom:
#             save_new_uom = ItemUOM(companyautokey=tempcompanyautokey,itemcode=itemcode_intance,uom=uom,rate=rate,price=price,lastupdate=1)
#             save_new_uom.save()

#         if not filter_unit_uom:
#             save_unit_uom = ItemUOM(companyautokey=tempcompanyautokey,itemcode=itemcode_intance,uom=unit_uom,rate=unit_rate,price=unit_price,lastupdate=1)
#             save_unit_uom.save()
#     else:
#         itemcode_intance = Item.objects.get(itemcode=itemcode)
#         if not filter_uom:
#             save_new_uom = ItemUOM(companyautokey=tempcompanyautokey,itemcode=itemcode_intance,uom=uom,rate=rate,price=price,lastupdate=1)
#             save_new_uom.save()

#         if not filter_unit_uom:
#             save_unit_uom = ItemUOM(companyautokey=tempcompanyautokey,itemcode=itemcode_intance,uom=unit_uom,rate=unit_rate,price=unit_price,lastupdate=1)
#             save_unit_uom.save()


# def create_mameee_item_itemuom_cn(item_code,description,uom,price,rate,unit_uom,unit_price,unit_rate):
#     tempcompanyautokey = Company.objects.filter(name='Villy').first()
#     filter_itemcode = Item.objects.filter(itemcode=item_code)
#     filter_uom = ItemUOM.objects.filter(itemcode=item_code, uom=uom)
#     filter_unit_uom = ItemUOM.objects.filter(itemcode=item_code, uom=unit_uom)
#     mainsupplier='Mamee'

#     if not filter_itemcode:
#         save_new_item = Item(description=description,itemcode=item_code,companyautokey=tempcompanyautokey,mainsupplier=mainsupplier, dockkey=1, dutyrate=1, costingmethod=0, lastmodified=datetime.now(), lastupdate=0)
#         save_new_item.save()
#         itemcode_intance = Item.objects.get(itemcode=item_code)

#         if not filter_uom:
#             save_new_uom = ItemUOM(companyautokey=tempcompanyautokey,itemcode=itemcode_intance,uom=uom,rate=rate,price=price,lastupdate=1)
#             save_new_uom.save()

#         if not filter_unit_uom:
#             save_unit_uom = ItemUOM(companyautokey=tempcompanyautokey,itemcode=itemcode_intance,uom=unit_uom,rate=unit_rate,price=unit_price,lastupdate=1)
#             save_unit_uom.save()

#     else:
#         itemcode_intance = Item.objects.get(itemcode=item_code)
#         if not filter_uom:
#             save_new_uom = ItemUOM(companyautokey=tempcompanyautokey,itemcode=itemcode_intance,uom=uom,rate=rate,price=price,lastupdate=1)
#             save_new_uom.save()

#         if not filter_unit_uom:
#             save_unit_uom = ItemUOM(companyautokey=tempcompanyautokey,itemcode=itemcode_intance,uom=unit_uom,rate=unit_rate,price=unit_price,lastupdate=1)
#             save_unit_uom.save()
