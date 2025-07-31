import os

# Environment variables for Django project
# This file should be added to .gitignore to keep sensitive data secure


# Django Secret Key - Generate a new one for production
os.environ.setdefault('SECRET_KEY', "12Moore!")

# Database Configuration
os.environ.setdefault('DATABASE_URL', "postgresql://neondb_owner:npg_uMcI0l7GokAL@ep-late-feather-a2avc9t0.eu-central-1.aws.neon.tech/debt_dried_grill_721186")

# Debug Mode - Set to False in production
os.environ.setdefault('DEBUG', 'True')

# Allowed Hosts - Add your domain names for production
os.environ.setdefault('ALLOWED_HOSTS', 'localhost,127.0.0.1')

# Email Configuration (optional - for contact forms)
os.environ.setdefault('EMAIL_HOST', 'smtp.gmail.com')
os.environ.setdefault('EMAIL_PORT', '587')
os.environ.setdefault('EMAIL_HOST_USER', 'your-email@gmail.com')
os.environ.setdefault('EMAIL_HOST_PASSWORD', 'your-app-password')
os.environ.setdefault('EMAIL_USE_TLS', 'True')

# Static and Media Files
os.environ.setdefault('STATIC_URL', '/static/')
os.environ.setdefault('MEDIA_URL', '/media/')

# Cloudinary Configuration (if using for image hosting)
# os.environ.setdefault('CLOUDINARY_URL', 'cloudinary://your-cloudinary-url')