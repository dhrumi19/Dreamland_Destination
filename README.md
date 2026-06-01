# ✈️ Dreamland Destination — Online Travel Booking System

![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=flat&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-6.0.3-092E20?style=flat&logo=django&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-8.0-4479A1?style=flat&logo=mysql&logoColor=white)
![Razorpay](https://img.shields.io/badge/Razorpay-Integrated-02042B?style=flat&logo=razorpay&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3.2-7952B3?style=flat&logo=bootstrap&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=flat)

A full-stack travel booking web application built with **Python** and **Django 6.0.3**.
Users can explore destinations, book packages, choose transport, pay online
via Razorpay, receive email confirmations, and download PDF invoices —
all from a single platform.

## 🚀 Features

### User Side
- 🔐 User registration and session-based login / logout
- 🏖️ Browse destinations and filter/sort travel packages
- 🪑 Real-time seat availability check before booking
- 💳 Secure online payment via **Razorpay** (UPI, Cards, Net Banking)
- 📧 Automated booking confirmation email via Gmail SMTP
- 📄 Downloadable PDF invoice using **ReportLab**
- 🔍 Track booking status by Booking ID
- ❌ Cancel a booking
- ⭐ Submit star rating and feedback after the trip

### Admin Side
- 📊 Custom dashboard with booking stats and Chart.js visualisations
- 🎨 Modern admin panel with **Jazzmin** (Bootstrap dark theme)
- ✅ Full CRUD for Destinations, Packages, Transport, Bookings, Payments, Feedback

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.12, Django 6.0.3 |
| Database | MySQL 8.0 (mysqlclient 2.2.8) |
| Frontend | Bootstrap 5.3.2, Font Awesome 6.5, Chart.js |
| Payment | Razorpay 2.0.1 |
| PDF | ReportLab 4.4.10 |
| Email | Gmail SMTP (Django send_mail) |
| Admin Theme | Jazzmin 3.0.4 |
| Images | Pillow 12.1.1 |

## ⚙️ Installation

```bash
# 1. Clone the repository
git clone https://github.com/your-username/dreamland-destination.git
cd dreamland-destination

# 2. Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # macOS / Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create MySQL database
mysql -u root -p
CREATE DATABASE dreamland_db;
EXIT;

# 5. Configure settings.py
# Update DATABASES, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD,
# RAZOR_KEY_ID, RAZOR_KEY_SECRET with your credentials

# 6. Run migrations
python manage.py migrate

# 7. Create superuser (for admin panel)
python manage.py createsuperuser

# 8. Start development server
python manage.py runserver

# Visit: http://127.0.0.1:8000
```

## 📁 Project Structure

```
dreamland-destination/
├── dreamland_destination/    # Django project config
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── dreamland_app/            # Main application
│   ├── models.py             # 7 database models
│   ├── views.py              # 15+ view functions
│   ├── urls.py               # 17 URL routes
│   ├── admin.py              # Admin registrations
│   ├── templates/            # 12 HTML templates
│   ├── static/CSS/           # style.css, reg.css
│   └── migrations/           # 9 migration files
├── media/                    # Uploaded images
├── manage.py
└── requirements.txt
```

## 🗄️ Database Models

| Model | Description |
|---|---|
| User | Registered traveller profile |
| Destination | Tourist location with image and price |
| Package | Travel package under a destination |
| Transport | Train / Flight / Bus options |
| Booking | Central booking record (links User, Package, Transport) |
| Payment | Payment transaction record |
| Feedback | Post-trip star rating and comment |

## 🔑 Environment Variables

Add these in **settings.py** (use environment variables in production):

```python
SECRET_KEY          = 'your-django-secret-key'
DB_NAME             = 'dreamland_db'
DB_USER             = 'root'
DB_PASSWORD         = 'your-mysql-password'
EMAIL_HOST_USER     = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'   # Google App Password
RAZOR_KEY_ID        = 'rzp_test_xxxxxxxxxxxx'
RAZOR_KEY_SECRET    = 'your-razorpay-secret'
```



**Dhrumi Shah**
MSCIT Student | Brainy Beam Technologies Internship
