**E-commerce Website using Django**

## Introduction
Welcome to our E-commerce website built with Django! This repository contains the source code for our online store where users can browse and purchase products, manage their profiles, and perform various account-related actions. Additionally, the website provides API endpoints for seamless integration with external applications.

## Features
- **User Authentication**: Users can create accounts, login, logout, and update their profiles securely. Simple JWT (JSON Web Tokens) is used for authentication, ensuring secure access to user accounts.
- **OTP Verification**: Users undergo OTP (One-Time Password) verification during account creation and certain sensitive operations for enhanced security.
- **Email Services**: The website integrates email services to send OTP verification codes, password change reminders, and order summary emails.
- **Product Management**: Browse products, view detailed descriptions, and add items to the cart for purchase.
- **Shopping Cart**: Users can add products to their cart, update quantities, and proceed to checkout.
- **Order Management**: Place orders, view order history, and track shipment status.
- **API Endpoints**: Includes endpoints for user profile creation, login, change password, add address, and more, facilitating seamless integration with other applications.
- **Responsive Design**: The website is optimized for various devices, providing a consistent user experience across desktop and mobile platforms.

## Setup
To run the project locally, follow these steps:
1. Clone the repository to your local machine.
2. Install the required dependencies listed in `requirements.txt`.
3. Configure the database settings in `settings.py`.
4. Run database migrations using `python manage.py migrate`.
5. Start the development server with `python manage.py runserver`.

## API Documentation
The API provides endpoints for the following operations:
- **User Profile Creation**: `POST /api/register/`
- **User Authentication**: `POST /api/login/`
- **User RefreshToken**: `POST /api/refresh/`
- **Change Password**: `POST /api/password_change/`
- **Add/Create/Update Address**: `GET/POST/PUT /api/address/`
- **View/Update Profile**: `GET/PATCH /api/profile/`

## Technologies Used
- Django: Python web framework for building the backend.
- Django Rest Framework: Toolkit for building Web APIs.
- Simple JWT: Secure token-based authentication for API endpoints.
- HTML/CSS: Frontend styling and layout.
- JavaScript: Client-side scripting for dynamic behavior.
- SQLite: Databases for storing user and product information.
- Email Services: Integration with email services for sending OTP codes, password change reminders, and order summary emails.

## Contributors
- [Ritik Mehra](https://github.com/Yyuichiii)

## Acknowledgments
We would like to thank the Django and Django Rest Framework communities for their excellent documentation and support.
