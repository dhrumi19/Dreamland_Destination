from django.db import models

# -----------------------------
# USER  TABLE
# -----------------------------
class User(models.Model):

    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, unique=True)
    city = models.CharField(max_length=100)
    image = models.ImageField(upload_to='users/', default='default.png')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name



# class UserProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     phone = models.CharField(max_length=15)
#     city = models.CharField(max_length=100)

#     def __str__(self):
#         return self.user.username

# -----------------------------
# DESTINATION TABLE
# -----------------------------
class Destination(models.Model):
    destination_name = models.CharField(max_length=150)
    location = models.CharField(max_length=150)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to='destinations/', blank=True, null=True)

    def __str__(self):
        return self.destination_name


# -----------------------------
# PACKAGE TABLE
# -----------------------------
class Package(models.Model):

    destination = models.ForeignKey(
        Destination,
        on_delete=models.CASCADE,
        related_name="packages"
    )

    package_name = models.CharField(max_length=150)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.CharField(max_length=50)
    description = models.TextField()
    total_seats = models.IntegerField(default=40)

    def __str__(self):
        return self.package_name

# -----------------------------
# CUSTOMER TABLE
# -----------------------------
# class Customer(models.Model):

#     name = models.CharField(max_length=100)
#     email = models.EmailField(unique=True)
#     password = models.CharField(max_length=100)
#     phone = models.CharField(max_length=20, unique=True)
#     city = models.CharField(max_length=100)

#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.name

# -----------------------------
# TRANSPORT TABLE
# -----------------------------

class Transport(models.Model):

    TRANSPORT_TYPE = (
        ('Train','Train'),
        ('Flight','Flight'),
        ('Bus', 'Bus'),
    )

    transport_type = models.CharField(max_length=20,choices=TRANSPORT_TYPE)

    from_city = models.CharField(max_length=100)

    to_city = models.CharField(max_length=100)

    total_seats = models.IntegerField(default=100)

    price = models.IntegerField()

    departure_time = models.TimeField()

    arrival_time = models.TimeField()

    def __str__(self):
        return f"{self.from_city} → {self.to_city} ({self.transport_type})"

# -----------------------------
# BOOKING TABLE
# -----------------------------
class Booking(models.Model):

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="bookings"
    )

    package = models.ForeignKey(
        Package,
        on_delete=models.CASCADE,
        related_name="bookings"
    )

    transport = models.ForeignKey(
        Transport,
        on_delete=models.CASCADE,
        related_name="bookings"
    )
    

    booking_date = models.DateField(auto_now_add=True)
    travel_date = models.DateField()

    total_people = models.IntegerField(default=1)

    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    # Razorpay fields
    razorpay_order_id = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )

    razorpay_payment_id = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )

    payment_status = models.CharField(
        max_length=50,
        default="Pending"
    )

    def __str__(self):
        return f"Booking {self.id} - {self.user.name}"


# -----------------------------
# PAYMENT TABLE
# -----------------------------
class Payment(models.Model):

    PAYMENT_METHOD = [
        ('UPI', 'UPI'),
        ('Credit Card', 'Credit Card'),
        ('Debit Card', 'Debit Card'),
        ('Cash', 'Cash'),
        ('Online', 'Online'),
    ]

    PAYMENT_STATUS = [
        ('Pending', 'Pending'),
        ('Success', 'Success'),
        ('Failed', 'Failed'),
    ]

    booking = models.ForeignKey(
        Booking,
        on_delete=models.CASCADE,
        related_name="payments"
    )

    payment_method = models.CharField(
        max_length=50,
        choices=PAYMENT_METHOD
    )

    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS,
        default="Pending"
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    payment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking {self.booking.id} - {self.payment_status}"
    
# -----------------------------
# FEEDBACK TABLE
# -----------------------------

class Feedback(models.Model):
    booking = models.ForeignKey('Booking', on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback for Booking {self.booking.id}"
