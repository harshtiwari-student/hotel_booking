from django.contrib import admin
from .models import Room, Booking, Address, Payment

# Register your models here.

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('roomid', 'roomtype','roomtype', 'description','price_per_night','image','is_available', 'userid')
    list_filter = ('roomtype', 'is_available')
    search_fields = ('roomid', 'roomtype')



class BookingAdmin(admin.ModelAdmin):
    list_display = ('bookingid', 'userid', 'roomid', 'checkin_date', 'checkout_date', 'guests', 'totalprice','status')
    list_filter = ('checkin_date', 'checkout_date')
    search_fields = ('userid__username', 'roomid__roomtype')


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('userid', 'mobile','address', 'pincode')
    search_fields = ('userid__username', 'mobile', 'pincode')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('receiptid', 'bookingid', 'userid', 'roomid', 'totalprice')
    # list_filter = ('payment_method',) if 'payment_method' exists in your model
    search_fields = ('receiptid', 'bookingid__bookingid', 'userid__username')

admin.site.register(Booking,BookingAdmin)
