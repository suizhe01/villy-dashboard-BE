"""Turn a per-quantity line sold loose (UNIT, bottle, ...) into cartons.

Commission rates for these classes are set per carton, but a line's qty is in
whatever UOM it was invoiced in, so 1,000 loose 1KG bottles used to earn as much
as 1,000 cartons of 12. A loose line is converted with its item's own UOM rates:

    cartons = qty x rate of the sold UOM / rate of the item's CTN UOM

Rates come from the dashboard's itemuom first. It only holds the UOMs an invoice
has used, so a rate missing there is looked up in Autocount, book 1, then 2,
then 3, the first one found winning. An item with no CTN anywhere (the 17KG tin
and jerry can, a single pack each) is left as invoiced, as is a line whose rates
cannot be read because Autocount is unreachable.
"""
import logging

from acitemuom.models import AcItemUOM
from itemuom.models import ItemUOM

logger = logging.getLogger(__name__)

LOOSE_TO_CARTON_CLASSES = ('SAJIOIL(Q)', 'ECOSAFA(Q)')
CARTON_UOM = 'CTN'
AUTOCOUNT_BOOKS = ('windows_server', 'windows_server_book2', 'windows_server_book3')


class CartonRates:
    """UOM rates for one calculation run, each looked up once."""

    def __init__(self):
        self._rates = {}
        self._unreachable = set()

    def rate(self, item_code, uom):
        key = (item_code, uom)
        if key not in self._rates:
            self._rates[key] = self._local_rate(item_code, uom) or self._autocount_rate(item_code, uom)
        return self._rates[key]

    def cartons(self, item_code, uom, qty):
        """qty in cartons, or None when the line has to stay as invoiced."""
        carton_rate = self.rate(item_code, CARTON_UOM)
        uom_rate = self.rate(item_code, uom)
        if not carton_rate or not uom_rate:
            return None
        return qty * uom_rate / carton_rate

    @staticmethod
    def _local_rate(item_code, uom):
        return (ItemUOM.objects.filter(itemcode=item_code, uom=uom, rate__gt=0)
                .values_list('rate', flat=True).first())

    def _autocount_rate(self, item_code, uom):
        for book in AUTOCOUNT_BOOKS:
            if book in self._unreachable:
                continue
            try:
                rate = (AcItemUOM.objects.using(book).filter(itemcode=item_code, uom=uom, rate__gt=0)
                        .values_list('rate', flat=True).first())
            except Exception:
                # Not asked again this run, so one unreachable book does not
                # stall every line behind its connection timeout.
                logger.exception('Autocount %s unreachable; loose lines it would convert stay as invoiced', book)
                self._unreachable.add(book)
                continue
            if rate:
                return rate
        return None
