from django.db import transaction
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Event, Category, TicketTier, Booking
from .serializers import EventSerializer, CategorySerializer, BookingSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .mpesa_utils import MpesaHandler 
from django.shortcuts import get_object_or_404

# Create your views here.
class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.filter(is_approved=True)
    serializer_class = EventSerializer
    
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    
    def create(self, request, *args, **kwargs):
        tier_id = request.data.get('ticket_tier')
        quantity = int(request.data.get('quantity', 1))
        
        # start the atomic transactions
        try:
            with transaction.atomic():
                # select_for_update() lock the row in the DB
                tier = TicketTier.objects.select_for_update().get(id=tier_id)
                
                # 1. Check Availability
                if tier.quantity_sold + quantity > tier.capacity:
                    return Response(
                        {"error": "Sold out or insufficient tickets remaining!"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                    
                # 2. Calculate Price
                total_price = tier.price * quantity
                
                # 3.Create the Booking
                booking = Booking.objects.create(
                    user=request.user,
                    ticket_tier=tier,
                    quantity=quantity,
                    total_price=total_price,
                    status='PENDING'
                )
                
                # 4. Update the Tier Stock
                tier.quantity_sold += quantity
                tier.save()
                
                serializer = self.get_serializer(booking)
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        except TicketTier.DoesNotExist:
            return Response({"error": "Ticket tier not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def initiate_payment(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    handler = MpesaHandler()
    
    # You'll need a public URL for the callback (use ngrok for local dev)
    callback_url = "https://plaza-clothing-brook.ngrok-free.dev/api/payments/callback/"
    
    response = handler.trigger_stk_push(
        phone_number=request.data.get('phone_number'),
        amount=booking.total_price,
        callback_url=callback_url,
        reference=str(booking.id)[:8]
    )

    if response.get('ResponseCode') == '0':
        booking.checkout_request_id = response.get('CheckoutRequestID')
        booking.phone_number = request.data.get('phone_number')
        booking.save()
        return Response({"message": "STK Push sent!"}, status=status.HTTP_200_OK)
    
    return Response({"error": "Failed to trigger M-Pesa"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def mpesa_callback(request):
    data = request.data.get('Body').get('stkCallback')
    result_code = data.get('ResultCode')
    checkout_request_id = data.get('CheckoutRequestID')

    if result_code == 0:
        booking = Booking.objects.get(checkout_request_id=checkout_request_id)
        booking.status = 'PAID'
        # Extract the receipt number from CallbackMetadata
        metadata = data.get('CallbackMetadata').get('Item')
        for item in metadata:
            if item.get('Name') == 'MpesaReceiptNumber':
                booking.mpesa_receipt_number = item.get('Value')
        booking.save()
        
    return Response({"ResultCode": 0, "ResultDesc": "Accepted"})