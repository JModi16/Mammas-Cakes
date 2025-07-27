# Mammas Cakes Project

## Overview
Mammas Cakes is a Django web application that showcases a variety of cakes and treats for different occasions, including birthdays, weddings, and vegan options. The application allows users to browse through different categories of cakes and treats, view images, and get in touch with the bakery.

## Project Structure
The project is organized into several directories and files, each serving a specific purpose:

- **manage.py**: Command-line utility for managing the Django project.
- **mammas_cakes/**: Main project directory containing settings and configuration files.
  - **settings.py**: Configuration for the Django project, including database settings and installed apps.
  - **urls.py**: URL routing for the project.
  - **wsgi.py**: WSGI application for deployment.
  - **asgi.py**: ASGI application for deployment.
- **cakes/**: Django application for managing cake-related views and templates.
  - **models.py**: Data models for the cakes application.
  - **views.py**: View functions for handling requests and returning responses.
  - **urls.py**: URL routing specific to the cakes application.
  - **templates/cakes/**: Directory containing HTML templates for various pages.
- **static/**: Directory for static files such as CSS, JavaScript, and images.
- **media/**: Directory for uploaded media files.
- **requirements.txt**: Lists the dependencies required for the project.

## Features
- Display images of cakes categorized by type: Birthday Cakes, Wedding Cakes, Treats, Vegan Cakes, and All Cakes & Treats.
- User-friendly navigation to browse through different cake categories.
- Contact page for inquiries and feedback.

## Installation
1. Clone the repository:
   ```
   git clone <repository-url>
   ```
2. Navigate to the project directory:
   ```
   cd mammas-cakes
   ```
3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```
4. Run the migrations:
   ```
   python manage.py migrate
   ```
5. Start the development server:
   ```
   python manage.py runserver
   ```

## Usage
- Access the application in your web browser at `http://127.0.0.1:8000/`.
- Browse through the different cake categories and view images.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.