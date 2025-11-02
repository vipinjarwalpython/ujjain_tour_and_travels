╔═══════════════════════════════════════════════════════════════════════════╗
║          DJANGO DRF TOUR & TRAVELS - CONTACT API SETUP GUIDE             ║
╚═══════════════════════════════════════════════════════════════════════════╝

📦 STEP 1: CREATE VIRTUAL ENVIRONMENT
=====================================
# Create venv
python -m venv venv

# Activate venv
Windows:    venv\Scripts\activate
Linux/Mac:  source venv/bin/activate

# Verify activation (you should see (venv) in terminal)


📥 STEP 2: CREATE DJANGO PROJECT
=================================
# Install Django
pip install Django

# Create project
django-admin startproject tour_travels
cd tour_travels

# Create app
python manage.py startapp contact


📚 STEP 3: INSTALL DEPENDENCIES
================================
pip install djangorestframework python-decouple

# Save dependencies
pip freeze > requirements.txt


⚙️ STEP 4: CONFIGURE SETTINGS
==============================
# Update tour_travels/settings.py with the configuration provided above
# Add 'rest_framework' and 'contact' to INSTALLED_APPS
# Configure CACHES, EMAIL, and other settings


📁 STEP 5: CREATE DIRECTORY STRUCTURE
======================================
mkdir -p contact/templates/emails


📄 STEP 6: CREATE TEMPLATE FILES
=================================
# Create two HTML files in contact/templates/emails/:
1. contact_confirmation.html (copy from above)
2. admin_notification.html (copy from above)


🗄️ STEP 7: SETUP DATABASE CACHE
==================================
# Create cache table
python manage.py createcachetable

# This creates 'tour_travels_cache_table' in SQLite


🔑 STEP 8: CREATE .env FILE
============================
# Create .env file in project root:
SECRET_KEY=django-insecure-your-secret-key-here-change-in-production
DEBUG=True
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-16-digit-app-password
ADMIN_EMAIL=admin@tourtravels.com

# For Gmail App Password:
1. Go to Google Account Settings
2. Security → 2-Step Verification (enable if not enabled)
3. App Passwords → Generate new password
4. Use the 16-digit password in EMAIL_HOST_PASSWORD


🗃️ STEP 9: RUN MIGRATIONS
===========================
python manage.py makemigrations
python manage.py migrate
python manage.py createcachetable



👤 STEP 10: CREATE SUPERUSER
==============================
python manage.py createsuperuser
# Enter username, email, and password


🚀 STEP 11: RUN SERVER
=======================
python manage.py runserver

# Server will start at: http://127.0.0.1:8000/


╔═══════════════════════════════════════════════════════════════════════════╗
║                            API ENDPOINTS                                  ║
╚═══════════════════════════════════════════════════════════════════════════╝

🌐 BASE URL: http://127.0.0.1:8000/api/contact/inquiries/

1️⃣ LIST ALL INQUIRIES (GET)
============================
GET /api/contact/inquiries/

Response:
{
  "count": 10,
  "next": null,
  "previous": null,
  "results": [...]
}


2️⃣ CREATE NEW INQUIRY (POST)
==============================
POST /api/contact/inquiries/
Content-Type: application/json

Body:
{
  "full_name": "Rahul Sharma",
  "email": "rahul@example.com",
  "phone": "+919876543210",
  "inquiry_type": "package",
  "subject": "Kashmir Tour Package Inquiry",
  "message": "I am looking for a 7-day Kashmir package for 2 adults and 1 child in December. Please provide details on pricing and itinerary."
}

Response:
{
  "status": "success",
  "message": "Your inquiry has been submitted successfully! You will receive a confirmation email shortly.",
  "data": {
    "id": 1,
    "full_name": "Rahul Sharma",
    "email": "rahul@example.com",
    ...
  }
}

✉️ Emails sent automatically:
- User confirmation email
- Admin notification email


3️⃣ GET SINGLE INQUIRY (GET)
=============================
GET /api/contact/inquiries/1/

Response:
{
  "id": 1,
  "full_name": "Rahul Sharma",
  "email": "rahul@example.com",
  "phone": "+919876543210",
  "inquiry_type": "package",
  "inquiry_type_display": "Package Information",
  "subject": "Kashmir Tour Package Inquiry",
  "message": "I am looking for...",
  "status": "pending",
  "status_display": "Pending",
  "created_at": "2025-11-02T10:30:00Z",
  "updated_at": "2025-11-02T10:30:00Z",
  "is_active": true,
  "inquiry_age_days": 0
}


4️⃣ UPDATE INQUIRY (PUT)
=========================
PUT /api/contact/inquiries/1/
Content-Type: application/json

Body:
{
  "full_name": "Rahul Sharma",
  "email": "rahul@example.com",
  "phone": "+919876543210",
  "inquiry_type": "package",
  "subject": "Kashmir Tour Package - Updated",
  "message": "Updated message...",
  "status": "in_progress"
}


5️⃣ PARTIAL UPDATE (PATCH)
===========================
PATCH /api/contact/inquiries/1/
Content-Type: application/json

Body:
{
  "status": "resolved",
  "admin_notes": "Customer contacted and package details sent"
}


6️⃣ DELETE INQUIRY (DELETE)
============================
DELETE /api/contact/inquiries/1/

Response:
{
  "status": "success",
  "message": "Inquiry deleted successfully"
}

Note: This is a SOFT DELETE (sets is_active=False)


7️⃣ UPDATE STATUS (POST) - Custom Action
==========================================
POST /api/contact/inquiries/1/update-status/
Content-Type: application/json

Body:
{
  "status": "in_progress",
  "admin_notes": "Contacted customer via phone"
}

Response:
{
  "status": "success",
  "message": "Status updated to In Progress",
  "data": {...}
}


8️⃣ GET STATISTICS (GET)
=========================
GET /api/contact/inquiries/statistics/

Response:
{
  "total": 25,
  "pending": 10,
  "in_progress": 8,
  "resolved": 5,
  "closed": 2,
  "by_type": {
    "general": {
      "count": 5,
      "display_name": "General Inquiry"
    },
    "booking": {
      "count": 8,
      "display_name": "Booking Related"
    },
    "package": {
      "count": 10,
      "display_name": "Package Information"
    },
    "complaint": {
      "count": 1,
      "display_name": "Complaint"
    },
    "feedback": {
      "count": 1,
      "display_name": "Feedback"
    }
  },
  "recent_inquiries": 12
}


9️⃣ GET RECENT INQUIRIES (GET)
===============================
GET /api/contact/inquiries/recent/

Response:
{
  "status": "success",
  "count": 10,
  "data": [...]
}


╔═══════════════════════════════════════════════════════════════════════════╗
║                         TESTING WITH CURL                                 ║
╚═══════════════════════════════════════════════════════════════════════════╝

# Create new inquiry
curl -X POST http://127.0.0.1:8000/api/contact/inquiries/ \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "Priya Patel",
    "email": "priya@example.com",
    "phone": "9876543210",
    "inquiry_type": "booking",
    "subject": "Goa Beach Resort Booking",
    "message": "Want to book beach resort for 3 nights"
  }'

# Get all inquiries
curl http://127.0.0.1:8000/api/contact/inquiries/

# Get single inquiry
curl http://127.0.0.1:8000/api/contact/inquiries/1/

# Update status
curl -X POST http://127.0.0.1:8000/api/contact/inquiries/1/update-status/ \
  -H "Content-Type: application/json" \
  -d '{
    "status": "resolved",
    "admin_notes": "Booking confirmed"
  }'

# Get statistics
curl http://127.0.0.1:8000/api/contact/inquiries/statistics/

# Delete inquiry
curl -X DELETE http://127.0.0.1:8000/api/contact/inquiries/1/


╔═══════════════════════════════════════════════════════════════════════════╗
║                         TESTING WITH PYTHON                               ║
╚═══════════════════════════════════════════════════════════════════════════╝

import requests
import json

BASE_URL = "http://127.0.0.1:8000/api/contact/inquiries/"

# Create inquiry
data = {
    "full_name": "Amit Kumar",
    "email": "amit@example.com",
    "phone": "9123456789",
    "inquiry_type": "package",
    "subject": "Kerala Backwaters Tour",
    "message": "Looking for 5-day Kerala tour package for family"
}

response = requests.post(BASE_URL, json=data)
print(response.json())

# Get all inquiries
response = requests.get(BASE_URL)
print(response.json())

# Get statistics
response = requests.get(f"{BASE_URL}statistics/")
print(response.json())


╔═══════════════════════════════════════════════════════════════════════════╗
║                    FEATURES IMPLEMENTED                                   ║
╚═══════════════════════════════════════════════════════════════════════════╝

✅ Full CRUD Operations using ViewSet
   - Create, Read, Update, Delete with REST standards
   - Proper HTTP methods and status codes

✅ Django Built-in Database Cache
   - No Redis dependency required
   - Cache stored in SQLite table
   - 5-minute cache for list and detail views
   - 10-minute cache for statistics
   - Auto cache invalidation on updates

✅ Multi-threading for Email Sending
   - Custom EmailThread class
   - Non-blocking email operations
   - Emails sent in background threads
   - Fast API responses

✅ Dual Email Notifications
   - Beautiful HTML email to customer
   - Professional alert email to admin
   - Responsive email templates
   - Modern gradient designs

✅ Professional Email Templates
   - Customer confirmation with inquiry details
   - Admin notification with action buttons
   - Mobile-friendly responsive design
   - Professional branding

✅ Data Validation
   - Email validation and normalization
   - Phone number validation
   - Name and message length validation
   - Subject validation

✅ Advanced Features
   - Inquiry categorization (5 types)
   - Status management (4 states)
   - Soft delete (is_active flag)
   - Admin notes for internal use
   - Inquiry age calculation
   - Statistics endpoint
   - Recent inquiries endpoint

✅ Admin Panel Integration
   - Custom admin interface
   - Colored badges for status and type
   - Bulk actions (mark as resolved, etc.)
   - Search and filter capabilities
   - Inquiry age display
   - Professional UI

✅ Database Optimizations
   - Indexed fields for performance
   - Efficient queries
   - Pagination support

✅ Logging System
   - Comprehensive logging
   - File and console handlers
   - Email status tracking
   - Cache hit/miss logging

✅ Virtual Environment
   - Isolated Python environment
   - Clean dependency management
   - Production-ready setup


╔═══════════════════════════════════════════════════════════════════════════╗
║                       CACHE MANAGEMENT                                    ║
╚═══════════════════════════════════════════════════════════════════════════╝

# Clear all cache
python manage.py shell
>>> from django.core.cache import cache
>>> cache.clear()
>>> print("Cache cleared!")

# View cache table
python manage.py dbshell
sqlite> SELECT * FROM tour_travels_cache_table;

# Check cache statistics
python manage.py shell
>>> from django.core.cache import cache
>>> print(f"Cache info: {cache._cache.get_backend_timeout()}")


╔═══════════════════════════════════════════════════════════════════════════╗
║                      EMAIL CONFIGURATION GUIDE                            ║
╚═══════════════════════════════════════════════════════════════════════════╝

📧 FOR GMAIL:
=============
1. Enable 2-Factor Authentication
   - Go to Google Account → Security
   - Enable 2-Step Verification

2. Generate App Password
   - Go to: https://myaccount.google.com/apppasswords
   - Select "Mail" and "Other"
   - Copy the 16-digit password

3. Update .env file
   EMAIL_HOST_USER=your-email@gmail.com
   EMAIL_HOST_PASSWORD=your-16-digit-app-password

📧 FOR OTHER EMAIL PROVIDERS:
==============================
Outlook/Hotmail:
  EMAIL_HOST=smtp-mail.outlook.com
  EMAIL_PORT=587

Yahoo:
  EMAIL_HOST=smtp.mail.yahoo.com
  EMAIL_PORT=587

Custom SMTP:
  EMAIL_HOST=your-smtp-server.com
  EMAIL_PORT=587 or 465


╔═══════════════════════════════════════════════════════════════════════════╗
║                          TROUBLESHOOTING                                  ║
╚═══════════════════════════════════════════════════════════════════════════╝

❌ Problem: Emails not sending
================================
Solution 1: Check .env file
  - Verify EMAIL_HOST_USER and EMAIL_HOST_PASSWORD
  - Ensure no spaces in credentials

Solution 2: Check Gmail settings
  - Enable "Less secure app access" or use App Password
  - Check spam folder

Solution 3: Check logs
  - Look in debug.log file
  - Check console for error messages

Solution 4: Test email manually
  python manage.py shell
  >>> from django.core.mail import send_mail
  >>> send_mail('Test', 'Message', 'from@example.com', ['to@example.com'])


❌ Problem: Cache not working
==============================
Solution 1: Create cache table
  python manage.py createcachetable

Solution 2: Check settings
  - Verify CACHES configuration in settings.py

Solution 3: Clear and rebuild cache
  python manage.py shell
  >>> from django.core.cache import cache
  >>> cache.clear()


❌ Problem: Virtual environment issues
========================================
Solution 1: Recreate venv
  deactivate
  rm -rf venv  (or delete venv folder)
  python -m venv venv
  venv\Scripts\activate (Windows) or source venv/bin/activate (Linux/Mac)
  pip install -r requirements.txt

Solution 2: Check Python version
  python --version
  (Should be Python 3.8 or higher)


❌ Problem: Import errors
===========================
Solution: Reinstall dependencies
  pip install --upgrade -r requirements.txt


╔═══════════════════════════════════════════════════════════════════════════╗
║                     PRODUCTION CONSIDERATIONS                             ║
╚═══════════════════════════════════════════════════════════════════════════╝

🔒 Security:
============
- Set DEBUG=False in production
- Use strong SECRET_KEY
- Configure ALLOWED_HOSTS properly
- Use HTTPS only
- Implement rate limiting (already included)
- Add authentication/permissions for admin endpoints

📊 Database:
============
- Use PostgreSQL instead of SQLite
- Set up database backups
- Implement database connection pooling

⚡ Performance:
===============
- Consider using Celery for email tasks (better than threading)
- Use Redis cache instead of database cache
- Enable database query optimization
- Implement CDN for static files

🔍 Monitoring:
==============
- Set up error tracking (Sentry)
- Implement application monitoring
- Set up log aggregation
- Create health check endpoints

🚀 Deployment:
==============
- Use Gunicorn/uWSGI for WSGI server
- Configure Nginx as reverse proxy
- Set up SSL certificates
- Use environment-specific settings
- Implement CI/CD pipeline


╔═══════════════════════════════════════════════════════════════════════════╗
║                      PROJECT STRUCTURE SUMMARY                            ║
╚═══════════════════════════════════════════════════════════════════════════╝

tour_travels/
├── venv/                          # Virtual environment
├── tour_travels/
│   ├── __init__.py
│   ├── settings.py               # Main settings
│   ├── urls.py                   # Root URL config
│   └── wsgi.py
├── contact/
│   ├── __init__.py
│   ├── models.py                 # ContactInquiry model
│   ├── serializers.py            # DRF serializers
│   ├── views.py                  # ViewSet with CRUD
│   ├── urls.py                   # App URLs
│   ├── admin.py                  # Admin configuration
│   ├── utils.py                  # Email utilities
│   └── templates/
│       └── emails/
│           ├── contact_confirmation.html
│           └── admin_notification.html
├── manage.py
├── requirements.txt              # Dependencies
├── .env                          # Environment variables
├── db.sqlite3                    # Database
└── debug.log                     # Log file


╔═══════════════════════════════════════════════════════════════════════════╗
║                          QUICK START COMMANDS                             ║
╚═══════════════════════════════════════════════════════════════════════════╝

# Setup
python -m venv venv
venv\Scripts\activate  # Windows
pip install Django djangorestframework python-decouple
django-admin startproject tour_travels
cd tour_travels
python manage.py startapp contact

# Configure (add files and settings as shown above)

# Initialize
python manage.py createcachetable
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser

# Run
python manage.py runserver

# Access
API: http://127.0.0.1:8000/api/contact/inquiries/
Admin: http://127.0.0.1:8000/admin/


╔═══════════════════════════════════════════════════════════════════════════╗
║                              SUCCESS!                                     ║
║                                                                           ║
║  Your Tour & Travels Contact API is ready to use!                        ║
║  Visit http://127.0.0.1:8000/api/contact/inquiries/                      ║
║                                                                           ║
║  Features: ✅ ViewSet CRUD ✅ Cache ✅ Multi-threading ✅ Email          ║
╚═══════════════════════════════════════════════════════════════════════════╝
"""
    