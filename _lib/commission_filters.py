"""Line filters shared by the commission pipeline and the printed report.

create_crewdtl (calculate_commission.py) and commission_list_report must apply
the same filters, otherwise the PDF shows different numbers than the dashboard.
Both alias transactiondtl as `a`, so these fragments assume that alias.
"""

# Red Bull commission is quoted per carton, so RB(Q) earns on CTN alone - UNT,
# UNIT, OTR, PKT, CAN and BDL all pay nothing. Written as "not CTN" rather than
# a list of the loose UOMs so a new one does not silently start earning.
#
# RB PALLET(Q) needs its own list because pallet customers are invoiced in OTR,
# which there is a real multi-unit pack (rate 6 or 12), not a loose single. Some
# of those customers buy in OTR only, so folding the pallet class into the CTN
# rule would drop their invoices entirely rather than trim them.
#
# The pallet class still has to be named: update_transactiondtl_ispallet_itemclass
# converts RB(Q) to it whenever the debtor and item are both pallet, so a loose
# line sold to a pallet customer would otherwise slip past this.
#
# Free-of-charge cartons earn nothing either. A quantity-based itemclass pays
# commvalue x qty and never reads the amount, so without this a giveaway carton
# would pay the crew exactly as much as a sold one. Only an exact zero is
# dropped - a negative line is a return, which is not the same thing.
#
# Lines are dropped from the totals and hidden from the report rather than
# converted, so the underlying transactiondtl rows stay untouched.
NON_COMMISSIONABLE_RB_SQL = """
        AND NOT (
            (a.itemclass = 'RB(Q)' AND a.uom <> 'CTN')
            OR (a.itemclass = 'RB PALLET(Q)' AND a.uom NOT IN ('CTN','OTR'))
            OR (a.itemclass IN ('RB(Q)','RB PALLET(Q)') AND a.subtotal = 0)
        )
"""
