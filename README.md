# Django Supplements Website

This project is an E-commerce web application developed in **Django**, dedicated to the sale of supplements.

## General Structure

- **Project Name:** `suplimente_django`
- **Applications:**
    - `magazin`: The main application containing the store logic.
    - `Mesaje`: A directory used for storing messages received via the contact form (in JSON format).
    - `suplimente`: The project configuration directory.

## Technical Configuration
- **Database:** Configured to use **PostgreSQL** (`proiectsuplimente`).
  *Note: A `db.sqlite3` file exists in the root directory but is likely unused or legacy.*
- **Dependency Management:** Standard Django files (`manage.py`, `wsgi.py`, `asgi.py`).

## Core Functionalities (`magazin` App)

### 1. Data Models (`models.py`)
The database structure is well-defined for an e-commerce platform:
- **`Produs` (Product)**: The central element. Includes price, stock, status (active/inactive), and relationships to Category, Manufacturer, Ingredients, and Offers.
- **`Categorie` (Category)**: Product categories featuring visual properties such as `color` (hex) and `icon` (FontAwesome).
- **`Producator` (Manufacturer)**: Manufacturer details (country, founding year, turnover).
- **`Ingredient`**: A list of possible ingredients, classified by type (active, flavor, vitamin, other).
- **`Oferta` (Offer)**: Manages percentage discounts over specific time periods.
- **`ProfilUtilizator` (User Profile)**: An extension of the standard Django User, adding fields for phone number and full address.

### 2. User Flows (`views.py` & `urls.py`)
- **Public Navigation:** Home, About, and Info pages.
- **Product Catalog:**
    - Product listing with **advanced filtering** (by name, min/max price, category, active status).
    - Sorting (ascending/descending by price).
    - Customizable pagination.
    - Product detail pages and filtering by specific category.
- **User Account:**
    - Registration (automatically creates the associated User Profile).
    - Login and Logout.
    - Profile Page (accessible only to authenticated users).
- **Virtual Cart:** Routes for the cart exist, but currently display a "Work in Progress" page.

### 3. Special Features
- **Complex Contact Form:**
    - Validates user age.
    - Processes message text (corrects spacing, capitalizes sentences based on punctuation).
    - **Urgency Calculation:** Automatically determines if a message is urgent based on the message type and the user's selected waiting time.
    - Saves messages as **JSON** files in the `Mesaje` folder, including timestamps.
- **Custom Logging System:**
    - The `Accesare` class retains request history (IP, URL, date) in memory (RAM).
    - The `/log/` page allows viewing and filtering these logs, as well as displaying executed SQL queries (useful for debugging).
- **Context Processors:**
    - `categorii_meniu`: Makes product categories available in all templates (for the navigation menu).
    - `status_relatii_clienti`: Checks a schedule from a JSON file (`program_relatii.json`) to display whether Customer Service is currently "Open" or "Closed" based on the access time.

### Conclusion
This project is an advanced functional prototype for an online store. It implements core data structures and main user flows, featuring interesting elements regarding data processing (contact form) and system monitoring (logging). The "Shopping Cart" and "Checkout" areas are currently under development.
