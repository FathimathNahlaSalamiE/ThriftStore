# 🛍️ ThriftStore — Full-Stack Django E-Commerce Platform

A multi-role e-commerce web application for buying and selling second-hand goods. Built with Django, integrated with Stripe for payments, and deployed on Render with Cloudinary for media storage.

---

## 🔗 Live Demo

(https://thriftstore-55yl.onrender.com/)

---

## 📸 Screenshots

<img width="1912" height="962" alt="Screenshot 2026-06-20 014111" src="https://github.com/user-attachments/assets/22a595e9-88dc-4de2-b752-401e3db6f169" />
<img width="1912" height="960" alt="Screenshot 2026-06-20 014148" src="https://github.com/user-attachments/assets/4488b575-ef5f-423d-9cd9-2a3d49e45684" />
<img width="1912" height="966" alt="Screenshot 2026-06-20 014811" src="https://github.com/user-attachments/assets/06692282-4602-4ff2-aca2-4fa5bd757519" />
<img width="1917" height="961" alt="Screenshot 2026-06-20 014319" src="https://github.com/user-attachments/assets/ea022583-da6d-4e36-bbca-cb68c5a43c7a" />
<img width="1917" height="960" alt="Screenshot 2026-06-20 014339" src="https://github.com/user-attachments/assets/4b9d610b-6ee3-4ef8-9024-5d7fac4a6136" />

---

## ✨ Features

### Buyer
- Browse products by category with images
- View individual product details
- Add to cart with quantity control (increase / decrease / remove)
- Checkout flow with delivery address collection
- Stripe-powered payment (AED currency)
- View order history and re-order past items

### Seller
- Register as a seller at signup
- Add, edit, and delete own product listings
- Upload product images
- Seller dashboard showing all listed products

### Auth & Roles
- Custom user model with three roles: `Admin`, `Seller`, `Buyer`
- Role-based redirect after login
- Login-required protection on all buyer and seller views
- Profile image upload on signup

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3 · Django 6 |
| Database | SQLite (dev) · PostgreSQL (production) |
| Payments | Stripe Checkout (card payments) |
| Media storage | Cloudinary |
| Static files | WhiteNoise |
| Frontend | HTML · CSS · Bootstrap · Django templates |
| Deployment | Render (web service + gunicorn) |

---

## 🗂️ Project Structure

```
ThriftStore/
├── ThriftStore/          # Django project settings & root URLs
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── ThriftStoreApp/       # Main application
│   ├── models.py         # CustomUser, Product, Cart, Order, Address
│   ├── views.py          # All view logic
│   ├── urls.py           # URL routing
│   ├── forms.py          # Signup, Login, AddProduct forms
│   ├── templates/
│   │   ├── buyer/        # Home, cart, checkout, orders, product views
│   │   ├── seller/       # Seller dashboard, add/edit product
│   │   ├── login.html
│   │   └── signup.html
│   ├── static/css/
│   └── migrations/
├── media/                # Uploaded images (dev)
├── staticfiles/          # Collected static (production)
├── requirements.txt
├── build.sh              # Render build script
└── render.yaml           # Render deployment config
```

---

## 📦 Data Models

```
CustomUser      → extends AbstractUser; adds role (admin/seller/buyer) + profile image
CategoryDb      → product categories with images
ProductDb       → product listings linked to seller (CustomUser) and category
CartDb          → per-user cart items with quantity and computed total
AddressDb       → delivery address saved at checkout
OrderDb         → completed order with payment ID and status
OrderItem       → line items belonging to an order
```

---

## ⚙️ Local Setup

### Prerequisites
- Python 3.10+
- pip

### Steps

```bash
# 1. Clone the repository
git clone https://github.com/your-username/ThriftStore.git
cd ThriftStore

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set environment variables
# Create a .env file in the root directory:
SECRET_KEY=your-secret-key
DEBUG=True
STRIPE_PUBLIC_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...

# 5. Run migrations
python manage.py migrate

# 6. Create a superuser (for admin panel access)
python manage.py createsuperuser

# 7. Start the development server
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` — you'll land on the login page.

---

## 💳 Stripe Integration

This project uses [Stripe Checkout](https://stripe.com/docs/payments/checkout) for payment processing.

- Currency: **AED**
- Mode: `payment` (one-time)
- Test card: `4242 4242 4242 4242` · any future expiry · any CVC

To test locally, use your Stripe test keys from the [Stripe Dashboard](https://dashboard.stripe.com/test/apikeys).

---

## 🚀 Deployment (Render)

The project includes a `render.yaml` and `build.sh` for one-click deployment on [Render](https://render.com).

### Environment variables to set on Render:
| Key | Value |
|---|---|
| `SECRET_KEY` | Generate a strong random key |
| `DEBUG` | `False` |
| `DATABASE_URL` | Auto-set by Render PostgreSQL addon |
| `STRIPE_PUBLIC_KEY` | Your Stripe publishable key |
| `STRIPE_SECRET_KEY` | Your Stripe secret key |
| `CLOUDINARY_URL` | Your Cloudinary URL |

The `build.sh` script runs:
```bash
pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate
```

---

## 🔐 Security Note

> ⚠️ The Stripe API keys visible in this repository are **test keys only** and should be rotated before any production use. Never commit live secret keys to version control. Use environment variables or a secrets manager in production.

---

## 🧭 URL Reference

| URL | View | Access |
|---|---|---|
| `/` | Login | Public |
| `/signup/` | Signup | Public |
| `/home_page/` | Product browse | Buyer |
| `/display_products/<category>/` | Category filter | Buyer |
| `/view_product/<id>/` | Product detail | Buyer |
| `/cart_page/` | Shopping cart | Buyer |
| `/checkout/` | Checkout summary | Buyer |
| `/address_page/` | Delivery address | Buyer |
| `/payment/` | Stripe redirect | Buyer |
| `/my_orders/` | Order history | Buyer |
| `/seller_products/` | Seller dashboard | Seller |
| `/add_product/` | Add listing | Seller |
| `/edit_product/<id>` | Edit listing | Seller |

---

## 🙋 About the Developer

Built by **Fathimath Nahla Salami** — a full-stack developer with a BTech in Computer Science and hands-on experience in Django, React, and REST APIs.

- 🔗 [LinkedIn](https://www.linkedin.com/in/fathimathnahlasalamie)
- 🔗 [GitHub](https://github.com/FathimathNahlaSalamiE)
- 📧 nahlasalami321@gmail.com

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
