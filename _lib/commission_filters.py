"""Line filters shared by the commission pipeline and the printed report.

create_crewdtl (calculate_commission.py) and commission_list_report must apply
the same filters, otherwise the PDF shows different numbers than the dashboard.
Both alias transactiondtl as `a`, so these fragments assume that alias.
"""

# RB(Q) commission is quoted per carton, so loose-unit lines earn nothing. They
# are dropped from the totals and hidden from the report rather than converted,
# so the underlying transactiondtl rows stay untouched.
NON_COMMISSIONABLE_UOM_SQL = """
        AND NOT (a.itemclass = 'RB(Q)' AND a.uom IN ('UNT','UNIT'))
"""
