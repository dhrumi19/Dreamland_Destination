from django.urls import path
from . import views

urlpatterns = [

    # HOME
    path('', views.home, name='home'),

    # DESTINATIONS
    path('destinations/', views.destinations, name='destinations'),

    # PACKAGES
    path('packages/', views.packages, name='packages'),

    # BOOKING
    path('booking/', views.booking, name='booking'),

    # BOOKING SUCCESS
    path('booking-success/', views.booking_success, name='booking_success'),

    # CANCEL BOOKING
    path('cancel-booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),

    # PAYMENT PAGE
    path('payment/', views.payment, name='payment'),

    # RAZORPAY SUCCESS (Saves payment in DB)
    path('success/', views.success, name='success'),
    path('success/<int:booking_id>/', views.success, name='success_with_id'),

    # TRACK BOOKING
    path('track-booking/', views.track_booking, name='track_booking'),
 
    # CUSTOMER
    # path('customer/', views.customer, name='customer'),

    # AUTHENTICATION
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),

    # ADMIN DASHBOARD
    path('dashboard/', views.dashboard, name='dashboard'),

    # INVOICE
    path('invoice/<int:booking_id>/', views.invoice, name='invoice'),

    # FEEDBACK
    path('feedback/<int:booking_id>/', views.feedback, name='feedback'),

    # ASK QUESTION
    path('ask-question/<int:booking_id>/', views.ask_question, name='ask_question'),

]