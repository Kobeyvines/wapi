import qrcode
from io import BytesIO
from celery import shared_task
from django.core.files import File
from reportlab.pdfgen import canvas
from .models import Booking, Ticket

@shared_task
def generate_event_tickets(booking_id):
    booking = Booking.objects.get(id=booking_id)
    
    # One booking can have multiple tickets (quantity)
    for i in range(booking.quantity):
        ticket_number = f"WAPI-{str(booking.id)[:4]}-{i+1:03d}"
        ticket = Ticket.objects.create(booking=booking, ticket_number=ticket_number)

        # 1. Generate QR Code (In-memory for performance)
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(f"TICKET_ID:{ticket.id}")
        qr.make(fit=True)
        
        qr_io = BytesIO()
        img = qr.make_image(fill_color="black", back_color="white")
        img.save(qr_io, format='PNG')
        
        ticket.qr_code.save(f"{ticket_number}_qr.png", File(qr_io), save=False)

        # 2. Generate PDF Ticket
        pdf_io = BytesIO()
        p = canvas.Canvas(pdf_io)
        p.setFont("Helvetica-Bold", 16)
        p.drawString(100, 750, f"OFFICIAL TICKET: {booking.ticket_tier.event.name}")
        p.setFont("Helvetica", 12)
        p.drawString(100, 730, f"Attendee: {booking.user.username}")
        p.drawString(100, 715, f"Tier: {booking.ticket_tier.get_name_display()}")
        p.drawString(100, 700, f"Ticket No: {ticket_number}")
        p.showPage()
        p.save()

        ticket.pdf_ticket.save(f"{ticket_number}.pdf", File(pdf_io), save=True)