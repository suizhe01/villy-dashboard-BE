from django.db import connection
import pandas as pd
from openpyxl import Workbook
from datetime import datetime
from openpyxl.utils import get_column_letter
from openpyxl.styles import Border, Side
from openpyxl.styles import Font
from openpyxl.styles import Alignment

def export_report_by_date(start_date, end_date):
    fixed_headers = [
    'SUNDRY($)', 'DOB($)', 'LIPTON($)', 'MAMEE($)', 'MAMYPOKO($)', 'DKSH($)',
    'RB(Q)', 'YLTC(Q)', 'LE(Q)', 'CHEERS(Q)', 'RB PALLET(Q)',
    'SAJIOIL(Q)', 'SAJIOILPALLET(Q)', 'SAJISWEET(Q)', 'SAJISWEETPALLET(Q)',
    'SUNQUICK(Q)', 'ECOSAFA(Q)', 'KARA($)', 'KARA PALLET($)'
    ]

    # Query to count numbers of people in each lorry
    query_crewdtl_by_date = """
        SELECT DATE(d.DocDate) AS DocDate, d.LorryNumber, b.CrewId, c.crewname, a.ItemClass, 
        ROUND(SUM(CASE WHEN a.CommType = %s THEN totalqty ELSE 0 END), 2) AS totalqty, 
        ROUND(SUM(CASE WHEN a.CommType = %s THEN totalamount ELSE 0 END), 2) AS totalamount
        FROM autocount_dashboard.crewdtl a
        INNER JOIN autocount_dashboard.crew b
        ON a.CrewGuid = b.CrewGuid
        INNER JOIN autocount_dashboard.crewrate AS c
        ON b.CrewId = c.crewid
        INNER JOIN autocount_dashboard.lorry d
        ON b.LorryGuid=d.LorryGuid
        WHERE d.DocDate BETWEEN %s AND %s
        GROUP BY b.CrewGuid,b.crewid, a.ItemClass
        order by b.crewid, d.DocDate;
    """

    # Execute the queries
    with connection.cursor() as cursor:
        cursor.execute(query_crewdtl_by_date, ['$', '%', start_date, end_date])
        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()

    # Run once before looping over sheets
    crew_commission_map = {}  # { '0038': { 'CHEERS(Q)': 0.05, ... }, ... }

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT b.crewid, d.itemclass, commvalue 
            FROM autocount_dashboard.crewratedtl a
            INNER JOIN autocount_dashboard.crewrate b ON a.CrewRateGuid = b.crewrateguid
            INNER JOIN autocount_dashboard.commissionitemclass c ON a.CommissionItemClassGuid = c.CommissionItemClassGuid
            INNER JOIN autocount_dashboard.itemclass d ON d.ItemClassGuid = c.ItemClassGuid
            ORDER BY b.crewid;
        """)
        commission_rows = cursor.fetchall()

    for crewid, itemclass, commvalue in commission_rows:
        crew_commission_map.setdefault(crewid, {})[itemclass] = commvalue

    df = pd.DataFrame(rows, columns=columns)
    df['DocDate'] = pd.to_datetime(df['DocDate'])

    wb = Workbook()
    wb.remove(wb.active)

    # Group by CrewId to create one sheet per crew
    for crew_id, group_df in df.groupby("CrewId"):
        crewname = group_df["crewname"].iloc[0]
        
        
        sanitized_crewname = crewname.replace('/', '_').replace('\\', '_').replace('?', '_').replace('*', '_').replace('[', '_').replace(']', '_').replace(':', '_')
        crewname = sanitized_crewname[:31]

        ws = wb.create_sheet(title=str(crewname))

        title_row = 1
        ws.merge_cells(start_row=title_row, start_column=1, end_row=title_row, end_column=2 + len(fixed_headers))
        title_cell = ws.cell(row=title_row, column=1, value=crewname)
        title_cell.font = Font(bold=True, size=14)
        title_cell.alignment = Alignment(horizontal='center')
        ws.append(["DocDate", "LorryNumber"] + fixed_headers)  # Header row

        for (doc_date, lorry_number), date_group in group_df.groupby(["DocDate", "LorryNumber"]):
            row_data = {key: 0 for key in fixed_headers}

            for _, row in date_group.iterrows():
                item = row["ItemClass"]
                if item in fixed_headers:
                    value = row["totalqty"] if "(Q)" in item else row["totalamount"]
                    row_data[item] += value

            row_values = [row_data[header] if row_data[header] != 0 else "" for header in fixed_headers]
            ws.append([doc_date.date(), lorry_number] + row_values)
        
        total_row = ws.max_row + 1
        ws.merge_cells(start_row=total_row, start_column=1, end_row=total_row, end_column=2)
        ws.cell(row=total_row, column=1, value="Total").font = Font(bold=True)

        for col_idx in range(3, 3 + len(fixed_headers)):
            col_letter = get_column_letter(col_idx)
            formula = f"=SUM({col_letter}3:{col_letter}{total_row - 1})"  # because data starts from row 3 now
            ws.cell(row=total_row, column=col_idx, value=formula)
        for col in range(1, ws.max_column + 1):
            ws.cell(row=total_row, column=col).font = Font(bold=True)

        commission_rates = crew_commission_map.get(crew_id, {})  # from pre-fetched SQL results

        rate_row = ws.max_row + 1
        ws.merge_cells(start_row=rate_row, start_column=1, end_row=rate_row, end_column=2)
        ws.cell(row=rate_row, column=1, value="%").font = Font(bold=True)

        for col_idx, item in enumerate(fixed_headers, start=3):
            rate = commission_rates.get(item)
            ws.cell(row=rate_row, column=col_idx, value=rate if rate is not None else "")

        comm_row = ws.max_row + 1
        ws.merge_cells(start_row=comm_row, start_column=1, end_row=comm_row, end_column=2)
        ws.cell(row=comm_row, column=1, value="Total Commission").font = Font(bold=True)

        for col_idx, item in enumerate(fixed_headers, start=3):
            col_letter = get_column_letter(col_idx)
            total_cell = f"{col_letter}{total_row}"   # Total row
            rate_cell = f"{col_letter}{rate_row}"     # Commission rate row
            formula = f"={total_cell}*{rate_cell}"
            cell = ws.cell(row=comm_row, column=col_idx, value=formula)
            cell.number_format = '"RM"#,##0.00' 

        # === Grand Total Payout row (sum of all Total Commission cells) ===
        payout_row = ws.max_row + 1  # Leave one row spacing for clarity

        # Merge label (TOTAL PAYOUT) across columns A and B
        ws.merge_cells(start_row=payout_row, start_column=1, end_row=payout_row, end_column=2)
        ws.cell(row=payout_row, column=1, value="TOTAL PAYOUT").font = Font(bold=True)

        # Merge payout amount cell across columns C to S (columns 3 to 19)
        ws.merge_cells(start_row=payout_row, start_column=3, end_row=payout_row, end_column=2 + len(fixed_headers))

        # Calculate sum of Total Commission row (comm_row)
        start_col = get_column_letter(3)
        end_col = get_column_letter(2 + len(fixed_headers))
        sum_range = f"{start_col}{comm_row}:{end_col}{comm_row}"

        # Write the formula into the merged cell
        payout_cell = ws.cell(row=payout_row, column=3, value=f"=SUM({sum_range})")
        payout_cell.font = Font(bold=True, size=16)
        payout_cell.number_format = '"RM"#,##0.00'
        payout_cell.alignment = Alignment(horizontal='center')

        # autofit column
        for column_cells in ws.columns:
            max_length = 0
            for cell in column_cells:
                try:
                    value = str(cell.value)
                    max_length = max(max_length, len(value))
                except:
                    pass
            col_letter = get_column_letter(column_cells[0].column)
            ws.column_dimensions[col_letter].width = max_length + 2
        
        thin_border = Border(
        left=Side(style='thin'),
        right=Side(style='thin'),
        top=Side(style='thin'),
        bottom=Side(style='thin')
        )
        
        for row in ws.iter_rows(min_row=1, max_row=ws.max_row, min_col=1, max_col=ws.max_column):
            for cell in row:
                cell.border = thin_border

        

    
    end_date = end_date.strftime("%Y-%m-%d")

    filename = f"commission_report_{start_date}_to_{end_date}.xlsx"
    wb.save(filename)
    print(f"Excel report generated: {filename}")
    return filename
    
    # display_comm_by_crewid = []

    # for comm in filter_calculated_comm_by_crewid:
    #     doc_date, lorry_number, crew_id,crew_name,calculated_comm, total_qty, total_amount, crew_guid, lorry_guid = comm
    #     crew_dtl = {'docdate': doc_date,'lorrynumber': lorry_number ,'crewid': crew_id, 'crewname': crew_name, 'calculatedcomm': calculated_comm, 'crewguid':crew_guid, 'lorry_guid':lorry_guid, 'totalqty': total_qty, 'totalamount': total_amount}
    #     display_comm_by_crewid.append(crew_dtl)
        

    # return display_comm_by_crewid