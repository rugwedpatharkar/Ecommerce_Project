# GadgetGalaxy E-commerce

## Overview

GadgetGalaxy is an e-commerce platform that specializes in selling electronic gadgets and devices. The platform allows users to browse through various categories, view product details, add items to their cart, and place orders. Users can also manage their profiles, update personal information, and track their order history.

## Table of Contents

- [GadgetGalaxy E-commerce](#gadgetgalaxy-e-commerce)
  - [Overview](#overview)
  - [Table of Contents](#table-of-contents)
  - [1. Installation and Setup ](#1-installation-and-setup-)
  - [2. User Authentication ](#2-user-authentication-)
    - [2.1 User Registration](#21-user-registration)
    - [2.2 User Login](#22-user-login)
    - [2.3 User Logout](#23-user-logout)
    - [2.4 Password Reset](#24-password-reset)
  - [3. Product Management ](#3-product-management-)
    - [3.1 Product Listing](#31-product-listing)
    - [3.2 Product Details](#32-product-details)
    - [3.3 Product Reviews](#33-product-reviews)
  - [4. Shopping Cart ](#4-shopping-cart-)
    - [4.1 Cart Management](#41-cart-management)
  - [5. Liked Items ](#5-liked-items-)
  - [6. Payment Options ](#6-payment-options-)
    - [6.1 Cards and UPI](#61-cards-and-upi)
  - [7. Order Placement and Tracking ](#7-order-placement-and-tracking-)
    - [7.1 Order Placement](#71-order-placement)
    - [7.2 Order History](#72-order-history)
    - [7.3 Invoice Download](#73-invoice-download)
  - [8. Views and Templates ](#8-views-and-templates-)
  - [9. Email Notifications ](#9-email-notifications-)
  - [Conclusion ](#conclusion-)

## 1. Installation and Setup <a name="installation-and-setup"></a>

The GadgetGalaxy project is built using Django, a high-level Python web framework. To set up the project locally, follow these steps:

- Clone the repository from GitHub link.
- Install required dependencies using `pip install -r requirements.txt`.
- Run migrations to set up the database: `python manage.py migrate`.
- Create a superuser account: `python manage.py createsuperuser`.
- Start the development server: `python manage.py runserver`.
- Access the admin panel at <http://localhost:8000/admin/> to add products, categories, and manage users.

## 2. User Authentication <a name="user-authentication"></a>

### 2.1 User Registration

Users can register on the platform by providing their first name, last name, email, and password. An email confirmation is sent to verify the user's email address.

### 2.2 User Login

Registered users can log in using their email and password. Email verification is required for successful login.

### 2.3 User Logout

Users can log out of their accounts.

### 2.4 Password Reset

Users can initiate a password reset by providing their registered email. A one-time password (OTP) is sent to the user's email for verification. Users can set a new password after successful OTP verification.

## 3. Product Management <a name="product-management"></a>

### 3.1 Product Listing

Products are categorized, and users can browse products by category. Best-selling products are highlighted on the homepage.

### 3.2 Product Details

Detailed product information is available on the product detail page. Users can view related products based on the current product's category.

### 3.3 Product Reviews

Users can leave reviews for products, including optional images.

## 4. Shopping Cart <a name="shopping-cart"></a>

### 4.1 Cart Management

Users can add products to their shopping cart. Quantity can be adjusted, and items can be removed from the cart. Total cart amount is displayed, considering the quantity and prices of items.

## 5. Liked Items <a name="liked-items"></a>

Users can add products to their liked items list. Liked items can be viewed, and users can remove items from the list.

## 6. Payment Options <a name="payment-options"></a>

### 6.1 Cards and UPI

Users can add and manage their payment options, including credit/debit cards and UPI IDs.

## 7. Order Placement and Tracking <a name="order-placement-and-tracking"></a>

### 7.1 Order Placement

Users can place orders, selecting payment options and shipping addresses. Stock is updated upon order placement.

### 7.2 Order History

Users can view their order history, including order details and status.

### 7.3 Invoice Download

Users can download invoices for delivered orders in PDF format.

## 8. Views and Templates <a name="views-and-templates"></a>

Django's views and templates are used to render HTML pages and handle user interactions. Views include home page, product listing, product detail, user profile, order history, and more.

## 9. Email Notifications <a name="email-notifications"></a>

Users receive email notifications for account verification, password reset, and order confirmation.

## Conclusion <a name="conclusion"></a>

GadgetGalaxy provides a seamless e-commerce experience, allowing users to explore, purchase, and manage electronic gadgets effortlessly. The platform is designed with a user-friendly interface, robust authentication, and efficient order processing. The project's modular structure makes it easy to extend and enhance for future features and improvements.
