from rest_framework import status
from django.http import JsonResponse
from transaction.models import Transaction
from transactiondtl.models import TransactionDtl

def delete_transaction(lorry_guid,doc_no):
    print(lorry_guid, doc_no)

    try:
        get_transaction = Transaction.objects.filter(lorryguid=lorry_guid, docno=doc_no).first()
        
        if not get_transaction:
            print(f"No transaction found with lorry_guid={lorry_guid}, doc_no={doc_no}")
            return []
        
        transaction_guid = get_transaction.transactionguid
        print(f"Found transaction with GUID: {transaction_guid}")
        
        # Get transaction details
        filter_transactiondtl = TransactionDtl.objects.filter(transactionguid=transaction_guid)
        detail_count = filter_transactiondtl.count()
        print(f"Found {detail_count} transaction details to delete")
        
        # Delete transaction details
        if detail_count > 0:
            try:
                delete_result = filter_transactiondtl.delete()
                print(f"Transaction details deletion result: {delete_result}")
            except Exception as e:
                print(f"Error deleting transaction details: {str(e)}")
                return []
        
        # Delete main transaction
        try:
            # Refresh the transaction from database to ensure we have the latest state
            get_transaction.refresh_from_db()
            delete_result = get_transaction.delete()
            print(f"Main transaction deletion result: {delete_result}")
        except Exception as e:
            print(f"Error deleting main transaction: {str(e)}")
            return []
        
        # Check if transaction was actually deleted
        transaction_exists = Transaction.objects.filter(transactionguid=transaction_guid).exists()
        print(f"After deletion, transaction still exists: {transaction_exists}")
        
        # Return remaining document numbers
        filter_docno = Transaction.objects.filter(lorryguid=lorry_guid).order_by('docno').values_list('docno', flat=True)
        all_docno = list(filter_docno)
        return all_docno
        
    except Exception as e:
        print(f"Unexpected error in delete_transaction: {str(e)}")
        return []