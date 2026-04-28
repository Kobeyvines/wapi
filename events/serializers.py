from rest_framework import serializers
from .models import Event, Category, TicketTier, Booking

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        # DRF needs this to be explicit!
        fields = ['id', 'name', 'slug']

class TicketTierSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketTier
        fields = ['id', 'name', 'price', 'capacity', 'quantity_sold']

class EventSerializer(serializers.ModelSerializer):
    # These nested serializers help show full data in the API
    categories = CategorySerializer(many=True, read_only=True)
    tiers = TicketTierSerializer(many=True, read_only=True)
    organizer_name = serializers.CharField(source='organizer.username', read_only=True)

    class Meta:
        model = Event
        fields = [
            'id', 'name', 'slug', 'description', 'venue', 
            'date', 'poster', 'categories', 'tiers', 
            'organizer_name', 'is_approved'
        ]
        
class BookingSerializer(serializers.ModelSerializer):
    event_name = serializers.ReadOnlyField(source='ticket_tier.event_name')
    tier_name = serializers.ReadOnlyField(source='ticket_tier.get_name_display')
    
    class Meta:
        model = Booking
        fields = ['id', 'ticket_tier', 'quantity', 'total_price', 'status', 'event_name', 'tier_name']
        read_only_fields = ['total_price', 'status']