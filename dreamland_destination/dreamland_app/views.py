import razorpay
from django.shortcuts import render, redirect
from django.db.models import Sum, Count, Avg
from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse
from reportlab.pdfgen import canvas
# from .models import UserProfile
from .models import Destination, Package, Booking, Payment, User, Transport, Feedback

razorpay_client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
# ---------------- HOME PAGE ----------------

def home(request):

    destinations = Destination.objects.all()[:4]
    packages = Package.objects.all()[:4]

    context = {
        'destinations': destinations,
        'packages': packages
    }

    return render(request,'index.html',context)


# ---------------- INDEX PAGE ----------------

def index(request):
    return render(request,'index.html')


# ---------------- DESTINATIONS LIST ----------------

def destinations(request):

    destinations = Destination.objects.all()
    packages = Package.objects.all()

    return render(request, "destinations.html", {
        "destinations": destinations,
        "packages": packages
    })


# ---------------- PACKAGES ----------------

def packages(request):

    destination = request.GET.get('destination')
    max_price = request.GET.get('price')
    sort = request.GET.get('sort')

    # 🎯 BASE QUERY
    packages = Package.objects.annotate(avg_rating=Avg('bookings__feedback__rating'))

    # 🔍 FILTER BY DESTINATION
    if destination:
        packages = packages.filter(
            destination__destination_name__icontains=destination
        )

    # 💰 FILTER BY PRICE (SAFE)
    if max_price:
        try:
            max_price = float(max_price)
            packages = packages.filter(price__lte=max_price)
        except ValueError:
            max_price = None


    # 🔃 SORTING
    if sort == "low":
        packages = packages.order_by('price')
    elif sort == "high":
        packages = packages.order_by('-price')
    elif sort == "rating":
        packages = packages.order_by('-avg_rating')

    # 🎯 OPTIMIZED SEAT CALCULATION (NO LOOP QUERY ISSUE)
    bookings_count = Booking.objects.values('package').annotate(count=Count('id'))
    booking_dict = {b['package']: b['count'] for b in bookings_count}

    for p in packages:
        booked = booking_dict.get(p.id, 0)
        p.available_seats = p.total_seats - booked

    return render(request, 'packages.html', {
        'packages': packages,
        'selected_destination': destination,
        'selected_price': max_price,
        'selected_sort': sort
    })

# ---------------- BOOKING ----------------

def booking(request):

    # 🔒 Check Login
    if 'user_id' not in request.session:
        return redirect('login')

    user_id = request.session.get('user_id')

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return redirect('login')

    # 📦 Load Data
    packages = Package.objects.all()
    transports = Transport.objects.all()

    # 🎯 Pre-select package
    package_id = request.GET.get('package')
    selected_package = None

    if package_id:
        selected_package = Package.objects.filter(id=package_id).first()

    # =========================
    # 🧾 FORM SUBMIT
    # =========================
    if request.method == "POST":

        try:
            package_id = request.POST.get('package')
            transport_id = request.POST.get('transport')
            travel_date = request.POST.get('travel_date')
            people = int(request.POST.get('people'))

            # ✅ Validation
            if not package_id or not transport_id:
                return HttpResponse("Please fill all fields")

            if people <= 0:
                return HttpResponse("Invalid number of people")

            # Fetch objects
            package = Package.objects.get(id=package_id)
            transport = Transport.objects.get(id=transport_id)

            # 🪑 Package Seats Check
            booked_seats = Booking.objects.filter(package=package).count()
            available_seats = package.total_seats - booked_seats

            if people > available_seats:
                return HttpResponse(f"Only {available_seats} seats available")

            # 🪑 Transport Seats Check
            transport_booked = Booking.objects.filter(transport=transport).count()
            transport_available = transport.total_seats - transport_booked

            if people > transport_available:
                return HttpResponse(f"Only {transport_available} seats available in transport")

            # 💰 Price Calculation
            total_price = (package.price + transport.price) * people

            # 📝 Create Booking
            booking = Booking.objects.create(
                user=user,
                package=package,
                transport=transport,
                travel_date=travel_date,
                total_people=people,
                total_price=total_price,
                status="Pending"
            )

            # 💳 Razorpay Order
            amount = int(total_price * 100)

            razorpay_order = razorpay_client.order.create({
                "amount": amount,
                "currency": "INR",
                "payment_capture": "1"
            })

            booking.razorpay_order_id = razorpay_order['id']
            booking.save()

            return render(request, "payment.html", {
                "payment": razorpay_order,
                "booking": booking,
                "razorpay_key": settings.RAZOR_KEY_ID
            })

        except Package.DoesNotExist:
            return HttpResponse("Invalid Package Selected")

        except Transport.DoesNotExist:
            return HttpResponse("Invalid Transport Selected")

        except Exception as e:
            return HttpResponse(f"Error: {str(e)}")

    # =========================
    # 📄 LOAD PAGE
    # =========================
    return render(request, "booking.html", {
        "packages": packages,
        "transports": transports,
        "selected_package": selected_package
    })

# ---------------- BOOKING SUCCESS ----------------

def booking_success(request):

    booking_id = request.GET.get('booking_id')
    booking = None

    if booking_id:

        try:
            booking = Booking.objects.get(id=booking_id)

            if not Payment.objects.filter(booking=booking).exists():

                Payment.objects.create(
                    booking=booking,
                    payment_method="Online",
                    payment_status="Success",
                    amount=booking.total_price
                )

                booking.status = "Confirmed"
                booking.payment_status = "Success"
                booking.save()

                # SEND EMAIL
                send_mail(
                    "Booking Confirmation - Dreamland Travel",
                    f"""
Hello {booking.user.name},

Your booking is confirmed 🎉

📍 Destination: {booking.package.destination.destination_name}
📦 Package: {booking.package.package_name}
📅 Travel Date: {booking.travel_date}
👥 People: {booking.total_people}
💰 Amount Paid: ₹{booking.total_price}

Booking ID: {booking.id}

Thank you for choosing Dreamland Destination✈️!
""",
                    settings.EMAIL_HOST_USER,
                    [booking.user.email],
                    fail_silently=False,
                )

        except Booking.DoesNotExist:
            booking = None

    return render(request, 'success.html', {'booking': booking})


# ---------------- PAYMENT PAGE ----------------

def payment(request):

    user_id = request.session.get('user_id')

    bookings = Booking.objects.filter(user_id=user_id)

    if request.method == "POST":

        booking_id = request.POST.get('booking')
        method = request.POST.get('method')

        booking = Booking.objects.get(id=booking_id)

        Payment.objects.create(
            booking=booking,
            payment_method=method,
            payment_status="Success",
            amount=booking.total_price
        )

        return redirect('track_booking')

    return render(request, 'payment.html', {'bookings': bookings})


# ---------------- PAYMENT SUCCESS ----------------

def success(request, booking_id=None):

    if booking_id is None:
        booking_id = request.GET.get("booking_id")
    booking = None

    if booking_id:

        try:
            booking = Booking.objects.get(id=booking_id)

            if not Payment.objects.filter(booking=booking).exists():

                Payment.objects.create(
                    booking=booking,
                    payment_method="Online",
                    payment_status="Success",
                    amount=booking.total_price
                )

                booking.status = "Confirmed"
                booking.save()

        except Booking.DoesNotExist:
            pass

    return render(request, "success.html", {"booking": booking})

# ---------------- SIGNUP ----------------

def signup(request):

    if request.method == "POST":

        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone = request.POST.get('phone')
        city = request.POST.get('city')

        # 🔴 Robust Validation
        if not name or not email or not password or not phone or not city:
            return render(request, "signup.html", {
                "error": "All fields are required"
            })
            
        if len(phone) > 20:
            return render(request, "signup.html", {
                "error": "Phone number is too long (maximum 20 characters)."
            })
            
        if len(name) > 100 or len(email) > 100 or len(password) > 100 or len(city) > 100:
            return render(request, "signup.html", {
                "error": "One of the provided fields exceeds the maximum allowed length."
            })
        
        # 🔍 Check email already exists
        if User.objects.filter(email=email).exists():
            return render(request, "signup.html", {
                "error": "Email already registered"
            })

        # 🔍 Check phone already exists
        if User.objects.filter(phone=phone).exists():
            return render(request, "signup.html", {
                "error": "Phone already registered"
            })

        # ✅ Create User (your custom model)
        User.objects.create(
            name=name,
            email=email,
            password=password,   
            phone=phone,
            city=city
        )

        return redirect('login')

    return render(request, 'signup.html')

# ---------------- LOGIN ----------------

def login(request):

    if request.method == "POST":

        email = request.POST.get("email")
        password = request.POST.get("password")

        user = User.objects.filter(email=email, password=password)

        if user.exists():

            user = user.first()

            request.session['user_id'] = user.id
            request.session['user_name'] = user.name

            return redirect('home')

        else:

            return render(request, "login.html", {
                "error": "Invalid Email or Password"
            })

    return render(request, "login.html")


# ---------------- LOGOUT ----------------

def logout(request):

    if 'user_id' in request.session:
        del request.session['user_id']

    return redirect('home')


# ---------------- TRACK BOOKING ----------------

def track_booking(request):

    booking = None

    if request.method == "POST":

        booking_id = request.POST['booking_id']

        try:
            booking = Booking.objects.get(id=booking_id)
        except Booking.DoesNotExist:
            booking = None

    return render(request, 'track_booking.html', {'booking': booking})


# ---------------- ADMIN DASHBOARD ----------------

def dashboard(request):

    total_bookings = Booking.objects.count()
    total_payments = Payment.objects.count()
    total_users = User.objects.count()

    total_revenue = Payment.objects.filter(
        payment_status="Success"
    ).aggregate(total=Sum('amount'))['total'] or 0

    bookings = Booking.objects.select_related(
        'user', 'package'
    ).order_by('-id')[:5]

    return render(request, "dashboard.html", {
        "total_bookings": total_bookings,
        "total_payments": total_payments,
        "total_users": total_users,
        "total_revenue": total_revenue,
        "bookings": bookings
    })

# ---------------- INVOICE ----------------

def invoice(request, booking_id):

    booking = Booking.objects.get(id=booking_id)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_{booking.id}.pdf"'

    p = canvas.Canvas(response)

    p.setFont("Helvetica", 16)
    p.drawString(200, 800, "Dreamland Destination")

    p.setFont("Helvetica", 12)
    p.drawString(50, 750, f"Invoice ID: {booking.id}")
    p.drawString(50, 730, f"Customer: {booking.user.name}")
    p.drawString(50, 710, f"Email: {booking.user.email}")

    p.drawString(50, 670, f"Package: {booking.package.package_name}")
    p.drawString(50, 650, f"Travel Date: {booking.travel_date}")
    p.drawString(50, 630, f"People: {booking.total_people}")

    p.drawString(50, 590, f"Total Price: ₹{booking.total_price}")

    p.drawString(50, 540, "Thank you for booking with Dreamland!")

    p.showPage()
    p.save()

    return response

# ---------------- CANCEL BOOKING ----------------

def cancel_booking(request, booking_id):

    booking = Booking.objects.get(id=booking_id)

    booking.status = "Cancelled"
    booking.save()

    return redirect("track_booking")

# ----------------- FEEDBACK ----------------

def feedback(request, booking_id):
    booking = Booking.objects.get(id=booking_id)

    if request.method == "POST":
         rating = request.POST.get("rating")
         comment = request.POST.get("comment")

         Feedback.objects.create(
             booking=booking,
             rating=rating,
             comment=comment
         )
         return redirect(f"/success/?booking_id={booking.id}")
    return render(request, "feedback.html", {"booking": booking})

# ----------------- ASK QUESTION ----------------

def ask_question(request, booking_id):
    booking = Booking.objects.get(id=booking_id)

    if request.method == "POST":
        # Usually questions would be saved or emailed, 
        # but the request is specifically to redirect to success.
        return redirect(f"/success/?booking_id={booking.id}")

    return render(request, "ask_question.html", {"booking": booking})
