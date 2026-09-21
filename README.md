

Readme · MD
# 🛍️ MyShop
 
A full-stack Django ecommerce platform — dynamic product catalog, htmx-powered filtering, cart & checkout, real payment gateway integration, a customer account dashboard, and a customized admin panel, all wrapped in a hand-built design system.
 
## 🌐 Live Demo
 
🔗 [myshopdev.pythonanywhere.com](https://myshopdev.pythonanywhere.com)
 
## 📌 About the Project
 
MyShop is a portfolio-grade ecommerce site covering the full flow a real online store needs — browsing and filtering products, managing a cart, checking out through a real (sandboxed) payment gateway, tracking order history from a personal dashboard, and giving admins a clean, visual way to manage inventory, offers, and orders.
 
Beyond storefront basics, the project includes htmx-powered partial page updates for instant filtering with no full reloads, a rich-text product description editor, a Soft UI–styled customer account dashboard, and a Jazzmin-powered admin panel with live image previews, inline photo galleries, and computed status badges.
 
## ✨ Features
 
### Storefront
- 📚 **Product Catalog** — Category → Subcategory → Product structure with sidebar filters (subcategory, price range) and search
- ⚡ **Dynamic Filtering** — htmx-powered partial page swaps for instant filtering/pagination with no full reloads; independent, stackable subcategory and price filters
- 🖼️ **Rich Product Content** — Product descriptions authored via a CKEditor-style rich text editor in admin, rendered safely on the product detail page
- 🎨 **Empty-State UI** — Styled "no products match" state with a one-click filter reset
- 🎯 **Offers & Flash Sales** — Dedicated offer products with a pure-CSS animated flash-sale badge (no image dependency)
- ⭐ **Reviews** — Per-product customer ratings and written reviews
- 📄 **About & Contact Pages** — Animated stats section, feature grid, and a working contact form backed by a `ContactMessage` model
### Cart, Checkout & Payments
- 🛒 **Session-Based Cart** — Add, increment, decrement, and clear items, with live subtotal, tax, and total calculation
- 💳 **eSewa Payment Integration** — Dedicated `payments` app using eSewa's rc-epay v2 test API, HMAC-SHA256 signed requests, signature + amount + ownership verification on callback
- 📦 **Order Tracking** — `Transaction` (PENDING/COMPLETE/FAILED) → `Order` + `OrderItem` created only on confirmed payment, snapshotting product name, price, quantity, and image at time of purchase
### Accounts & Dashboard
- 🔐 **Custom Authentication** — Custom user model (email-based), with a separate `Profile` model for avatar, bio, and date of birth
- 🧑‍💻 **Customer Dashboard** — Soft UI–styled account area: Profile, My Orders (pulled from the payments app's order history), Wishlist, Settings, all in a sidebar-nav layout distinct from the storefront's ink-gold theme
- ✏️ **In-Place Profile Editing** — Modal-based profile editing without leaving the dashboard
### Admin
- 🛠️ **Customized Admin Panel** — django-jazzmin theme with live image thumbnails on list pages, inline product photo galleries with previews, a custom price-range list filter, and a computed "New" status badge per product
- 📋 **Full Model Coverage** — Products, categories, subcategories, offers, reviews, and contact messages all manageable from admin
### Design
- 📱 **Responsive UI** — Bootstrap 5 with a custom ink/gold design-token CSS system (Playfair Display + DM Sans), separate Soft UI theme for the account dashboard
## 🛠️ Tech Stack
 
| Layer | Technology |
|---|---|
| Backend | Python, Django 6.1 |
| Frontend | HTML5, CSS3, Bootstrap 5, htmx |
| Rich Text | django-ckeditor-5 |
| Database | SQLite |
| Media Storage | Cloudinary |
| Payments | eSewa (sandbox, rc-epay v2) |
| Admin UI | django-jazzmin |
| Deployment | PythonAnywhere |
 
## 🗂️ Project Structure
 
| App | Responsibility |
|---|---|
| `core` | Product catalog, category/subcategory models, cart views, homepage, about/contact, reviews, offers |
| `accounts` | Custom user model, authentication, Profile model, customer dashboard (profile, orders, wishlist, settings) |
| `payments` | eSewa payment integration — Transaction/Order/OrderItem models, signing and verification utils |
 
## ⚙️ Getting Started
 
```bash
# 1. Clone the repo
git clone https://github.com/Rajeshpachhai10/E-commerce_Project.git myshop
cd myshop
 
# 2. Create and activate virtual environment
python -m venv shopEnv
shopEnv\Scripts\Activate.ps1   # Windows PowerShell
 
# 3. Install dependencies
pip install -r requirements.txt
 
# 4. Set up environment variables (see below)
 
# 5. Apply migrations
python manage.py migrate
 
# 6. Create a superuser
python manage.py createsuperuser
 
# 7. Run the server
python manage.py runserver
```
 
Visit → http://127.0.0.1:8000
 
### Environment Variables
 
Managed via [python-decouple](https://pypi.org/project/python-decouple/). Create a `.env` file inside the project root:
 
```
SECRET_KEY=your-secret-key
DEBUG=True
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret
ESEWA_SECRET_KEY=your-esewa-secret
ESEWA_PRODUCT_CODE=your-esewa-product-code
ESEWA_FORM_URL=your-esewa-form-url
ESEWA_STATUS_CHECK_URL=your-esewa-status-check-url
```
 
## 🚀 Deployment
 
Deployed on [PythonAnywhere](https://www.pythonanywhere.com) using SQLite for the database, with Cloudinary for image storage and static files served via PythonAnywhere's static file mappings.
  
## 🙋 Author
 
**Rajesh Bahadur Pachhai**
GitHub: [@Rajeshpachhai10](https://github.com/Rajeshpachhai10)
Live Site: [myshopdev.pythonanywhere.com](https://myshopdev.pythonanywhere.com)
 
## 📄 License
 
This project is open source and available under the MIT License.
 










