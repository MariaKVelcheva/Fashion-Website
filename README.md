# EllaPrimE — Fashion Boutique E-Commerce Platform

A full-stack e-commerce web application for a fashion boutique, built with Django. Features a complete shopping experience including product browsing, cart management, secure checkout, user accounts, and order management.

---

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Environment Variables](#environment-variables)
- [Running the Project](#running-the-project)
- [Running Tests](#running-tests)
- [Deployment](#deployment)
- [Screenshots](#screenshots)

---

## Features

### Shopping
- Product catalogue with filtering by category, colour, and size
- Full-text search across product names, descriptions, and categories
- Product variant system — each garment has multiple size/colour combinations with individual stock tracking
- Out-of-stock items automatically pushed to the end of listings with reduced opacity
- New arrivals section (garments added within the last 60 days)
- Lookbook / gallery page with image slideshow

### Cart & Checkout
- Session-based cart for anonymous users, database-backed cart for authenticated users
- Automatic cart merge on login — items added before login are preserved
- Free delivery threshold with live gap indicator
- Pay on delivery and card payment (Stripe Checkout) options
- Stock validation at checkout
- Order confirmation emails to customer and admin via SendGrid + Celery

### User Accounts
- Custom user model with email-based authentication
- Customer profile with delivery details, order history, wishlist, and loyalty points
- Password change and reset via email
- Account deletion
- Loyalty points system — 1 point per 1 € spent

### Wishlist
- Toggle wishlist from any garment card or detail page
- Dedicated wishlist page and profile panel
- AJAX-powered — no page reload required

### Admin
- Full Django admin for managing garments, products, categories, colours, sizes
- Garment image management via inline admin
- Lookbook image management with drag-and-drop ordering
- Order status management with inline order items
- Newsletter subscriber management

### Newsletter
- Email subscription from the home page
- Welcome email via Celery task
- Subscriber management in admin

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Django 5.x |
| Database | PostgreSQL |
| Task Queue | Celery + Redis |
| Email | SendGrid (SMTP) |
| Payments | Stripe Checkout |
| Media Storage | Cloudinary |
| Static Files | WhiteNoise |
| Authentication | Django Auth + django-allauth |
| Frontend | Django Templates + vanilla JS |
| CSS | Custom CSS with CSS variables |

---

## Project Structure

```
fashionWebsite/
├── accounts/          # Custom user model, customer profiles, wishlist
├── clothes/           # Garments, products, categories, colours, sizes
├── common/            # Base templates, contact form, newsletter, utilities
├── orders/            # Cart, orders, checkout, Stripe integration
├── static/            # CSS, JS, images
├── templates/         # HTML templates
│   ├── accounts/
│   ├── clothes/
│   ├── common/
│   ├── emails/
│   ├── orders/
│   └── registration/
├── manage.py
├── requirements.txt
└── README.md
```

---

## Getting Started

### Prerequisites

- Python 3.11+
- PostgreSQL
- Redis (via Docker or local install)
- A Cloudinary account
- A SendGrid account
- A Stripe account

### Installation

**1. Clone the repository:**
```bash
git clone https://github.com/MariaKVelcheva/Fashion-Website.git
cd Fashion-Website
```

**2. Create and activate a virtual environment:**
```bash
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows
```

**3. Install dependencies:**
```bash
pip install -r requirements.txt
```

**4. Create a `.env` file in the project root** (see [Environment Variables](#environment-variables))

**5. Make sure `.env` is in your `.gitignore`:**
```bash
echo ".env" >> .gitignore
```

**6. Run migrations:**
```bash
python manage.py migrate
```

**7. Create a superuser:**
```bash
python manage.py createsuperuser
```

**8. Collect static files:**
```bash
python manage.py collectstatic
```

---

## Environment Variables

Create a `.env` file in the project root with the following:

```env
# Django
SECRET_KEY=your_django_secret_key
DEBUG=True

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/ellaprime

# Email (SendGrid)
EMAIL_HOST_PASSWORD=your_sendgrid_api_key
DEFAULT_FROM_EMAIL=your_verified_sender@yourdomain.com

# Cloudinary
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret

# Stripe
STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...

# Redis
CELERY_BROKER_URL=redis://127.0.0.1:6379/0
```

---

## Running the Project

You need four terminals running simultaneously:

**Terminal 1 — Redis:**
```bash
docker run -p 6379:6379 redis
```

**Terminal 2 — Celery worker:**
```bash
celery -A fashionWebsite worker --loglevel=info --pool=solo
```

**Terminal 3 — Django:**
```bash
python manage.py runserver
```

**Terminal 4 — Stripe CLI (for local webhook testing):**
```bash
stripe listen --forward-to localhost:8000/orders/stripe/webhook/
```

---

## Running Tests

```bash
# Run all tests
python manage.py test

# Run tests for a specific app
python manage.py test accounts
python manage.py test orders
python manage.py test clothes
```

The test suite covers:

- Customer profile completion validation
- Cart creation and session-to-database merge on login
- Add to cart — authenticated and anonymous users, stock validation, auto-selection of single variants
- Checkout — stock decrement, order confirmation, loyalty points, profile and stock guards
- Garment model — availability, new arrivals, slug generation, available colours

---

## Deployment

### Recommended hosts
- **Railway** — easiest setup, supports all services natively
- **DigitalOcean App Platform** — clean UI, good Django support
- **Render** — free tier available, straightforward Django deployment

### Pre-deployment checklist
- [ ] Set `DEBUG=False`
- [ ] Set `ALLOWED_HOSTS` to your domain
- [ ] Configure PostgreSQL on the production server
- [ ] Configure Redis on the production server
- [ ] Set all environment variables on the host
- [ ] Run `python manage.py collectstatic`
- [ ] Update Stripe webhook URL to https://ella-prime.com/orders/stripe/webhook/
- [ ] Verify Cloudinary credentials
- [ ] Point your domain DNS to the host

---

## Screenshots

*Coming soon*

---
## Author

Built by [Maria Velcheva](https://github.com/MariaKVelcheva)  
[ella-prime.com](https://ella-prime.com)
