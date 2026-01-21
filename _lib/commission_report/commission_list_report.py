from weasyprint import HTML
from django.template.loader import render_to_string
from django.http import HttpResponse
from collections import defaultdict
from decimal import Decimal
from django.db import connections
from weasyprint import HTML, CSS

def list_report(lorry_number, document_date, employee_details, invoice_list_no, generator_name=None):
    # print(document_date, invoice_list_no)
    employee_details = employee_details or []  # Handle None case
    driver_names = [crew["crewname"] for crew in employee_details if crew["crewtype"] == "Driver"]
    assistant_names = [crew["crewname"] for crew in employee_details if crew["crewtype"] == "Assistant"]

    driver_name_str = ", ".join(driver_names)
    assistant_name_str = ", ".join(assistant_names)

    # SQL Execution
    docno_list = tuple(invoice_list_no)

    query = """
    SELECT 
        a.uom,
        c.CompanyName as "Outlet Name", 
        b.DebtorCode, 
        b.DocNo, 
        a.commtype,
        CASE 
            WHEN a.commtype = '$' THEN a.itemclass 
            ELSE 'N/A' 
        END as itemclass,
        SUM(qty) AS qty, 
        SUM(subtotal) AS subtotal
    FROM autocount_dashboard.transactiondtl a
    INNER JOIN autocount_dashboard.transaction b ON a.transactionguid = b.transactionguid
    INNER JOIN autocount_dashboard.debtor c ON b.DebtorCode = c.AccNo
    INNER JOIN autocount_dashboard.lorry d ON b.lorryguid = d.lorryguid
    WHERE b.docno IN %s AND d.docdate LIKE %s
    GROUP BY 
        c.CompanyName, b.DebtorCode, b.DocNo, a.commtype, a.uom,
        CASE WHEN a.commtype = '$' THEN a.itemclass ELSE 'N/A' END;
    """
    if 'T' in document_date:
        document_date = document_date.replace('T', ' ')
        document_date = document_date.split('.')[0]
    date_pattern = f"{document_date}%"

    with connections['default'].cursor() as cursor:
        cursor.execute(query, [docno_list,date_pattern])
        rows = cursor.fetchall()

    # Group + transform
    grouped = defaultdict(lambda: {
        "outlet name": "",
        "debtor code": "",
        "document number": "",
        "amount": Decimal("0.00"),
        "ctn_parts": []
    })

    for row in rows:
        uom, outlet_name, debtor_code, docno, commtype, itemclass, qty, subtotal = row
        if subtotal:
            group = grouped[docno]
            group["outlet name"] = outlet_name
            group["debtor code"] = debtor_code
            group["document number"] = docno

            if commtype == "%":
                group["amount"] += subtotal
            if commtype == "$" and itemclass != "N/A":
                group["ctn_parts"].append(f"{int(qty)} {itemclass}")
                # if uom == 'UNT':
                #     if qty >= 6:
                #         qty = int(qty)/6
                #         group["ctn_parts"].append(f"{int(qty)} {itemclass}")
                # else:
                #     group["ctn_parts"].append(f"{int(qty)} {itemclass}")

    final_rows = []
    for doc in grouped.values():
        final_rows.append([
            doc["outlet name"],
            doc["debtor code"],
            doc["document number"],
            float(doc["amount"]),
            ", ".join(doc["ctn_parts"])
        ])

    final_rows.sort(key=lambda row: row[0].lower())

    document_date = document_date.split('T')[0]
    # Render HTML
    html = render_to_string("report_template.html", {
        "lorry_number": lorry_number,
        "document_date": document_date,
        "driver_name": driver_name_str,
        "assistant_name": assistant_name_str,
        "report_rows": final_rows,
        "generator_name": generator_name
    })

    pdf = HTML(string=html).write_pdf(
        stylesheets=[
            CSS(string='''
                @page {
                    size: A4;
                    margin: 1cm;
                }
                table {
                    page-break-inside: auto;
                }
                tr {
                    page-break-inside: avoid;
                    page-break-after: auto;
                }
                thead {
                    display: table-header-group;
                }
                tfoot {
                    display: table-footer-group;
                }
            ''')
        ]
    )

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="commission_report.pdf"'  # open in browser
    return response
