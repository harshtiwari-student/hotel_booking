from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Room(models.Model):
    roomid = models.IntegerField(primary_key=True)
    userid = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)  # for admin who added the room
    ROOM_TYPES = (
        ("Single", "Single"),
        ("Double", "Double"),
        ("Suite", "Suite"),
    )
    roomtype = models.CharField(max_length=50, choices=ROOM_TYPES)
    description = models.TextField()
    price_per_night = models.FloatField()
    image = models.ImageField(upload_to="photos")
    is_available = models.BooleanField(default=True)



class Booking(models.Model):
    bookingid = models.IntegerField(primary_key=True)
    userid = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    roomid = models.ForeignKey(Room, on_delete=models.CASCADE, null=True)
    checkin_date = models.DateField()
    checkout_date = models.DateField()
    guests = models.PositiveIntegerField(default=1)
    payment_method = models.CharField(max_length=30, default='cod')
    razorpay_order_id = models.CharField(max_length=100, blank=True, null=True)  # ✅ Keep this  # 
    totalprice = models.FloatField()
    STATUS_CHOICES = [
        ('booked', 'Booked'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='booked')


class Address(models.Model):
    userid = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    mobile = models.PositiveIntegerField()
    address = models.TextField()
    pincode = models.PositiveIntegerField()


class Payment(models.Model):
    receiptid = models.PositiveIntegerField(primary_key=True)
    bookingid = models.ForeignKey(Booking, on_delete=models.SET_NULL, null=True)
    userid = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    roomid = models.ForeignKey(Room, on_delete=models.CASCADE, null=True)
    totalprice = models.FloatField()