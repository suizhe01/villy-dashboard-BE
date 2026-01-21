from item.models import Item

def update_item_itemclass(item_code, item_class):
    filter_item = Item.objects.filter(itemcode = item_code)
    filter_item.update(itemclass=item_class)
    # print(filter_item)

    