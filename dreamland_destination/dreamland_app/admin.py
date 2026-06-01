from django.contrib import admin
from .models import *


class UserAdmin(admin.ModelAdmin):
    list_display = ('id','name','email','phone','city','created_at')


class DestinationAdmin(admin.ModelAdmin):
    list_display = ('id','destination_name','location','price')


class PackageAdmin(admin.ModelAdmin):
    list_display = ('id','package_name','destination','price','duration')


class BookingAdmin(admin.ModelAdmin):
    list_display = ('id','user','package','travel_date','total_people','total_price','status')


class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id','booking','payment_method','payment_status','amount','payment_date')


class TransportAdmin(admin.ModelAdmin):
    list_display = (
        'transport_type',
        'from_city',
        'to_city',
        'price',
        'total_seats',
        'departure_time',
        'arrival_time'
    )
    search_fields = ('from_city', 'to_city')
    list_filter = ('transport_type',)

class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('id', 'booking', 'rating', 'comment', 'created_at')
    search_fields = ('booking__id', 'comment')
    list_filter = ('rating',)


admin.site.register(User,UserAdmin)
admin.site.register(Destination,DestinationAdmin)
admin.site.register(Package,PackageAdmin)
admin.site.register(Booking,BookingAdmin)
admin.site.register(Payment,PaymentAdmin)
admin.site.register(Transport, TransportAdmin)
admin.site.register(Feedback, FeedbackAdmin)