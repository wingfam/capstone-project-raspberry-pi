from app import create_app, db
from app.models import Resident, Locker, BookingOrder, BookingCode, BookingHistory

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {
        'db': db, 
        'Resident': Resident, 
        'Locker': Locker, 
        'BookingOrder': BookingOrder, 
        'BookingCode': BookingCode, 
        'BookingHistory': BookingHistory
    }
