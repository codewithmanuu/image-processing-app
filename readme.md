# Image Processing App

## Description

The Image Processing App is designed to process image data from CSV files. It uses Django and PostgreSQL to manage and process image data, allowing users to upload CSV files containing image URLs, compress the images, and generate output CSV files with processed image URLs.

## LLD (LOW LEVEL DESIGN)
- [lld](https://docs.google.com/document/d/1TcJbiNgyegGSocJZ8DRlX1BnLFspZ1SNNKjEI68Blmw/edit?usp=sharing)

## Technologies Used

- **Backend**: Django, Django REST Framework
- **Database**: PostgreSQL
- **Task Queue**: Celery

## Installation

### Prerequisites

- [Python 3.8+](https://www.python.org/downloads/)
- [Pip](https://pip.pypa.io/en/stable/)
- [Redis](https://redis.io/download) (as the message broker for Celery)

### Setup

1. **Clone the repository:**

   ```bash
   git clone https://github.com/codewithmanuu/image-processing-app.git

2. **Navigate into the project directory:**
   ```bash
   cd image-processing-app

3. **Create a virtual environment:**
   ```bash
   python -m venv venv

4. **Activate the virtual environment:**
   ```bash
   source venv/bin/activate

5. **Install dependencies:**
   ```bash
   pip install -r requirements.txt

6. **Apply database migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate

7. **Create a superuser for accessing the Django admin panel:**
   ```bash
   python manage.py createsuperuser

8. **Start the Redis server (if not already running):**
   ```bash
   redis-server

9. **Start the Celery worker:**
   ```bash
   celery -A imagepro worker --loglevel=info

### usage

- Access the application at(http://localhost:8000/api/v1/)
- Access the Django admin panel at(http://localhost:8000/admin/)
- Use an API client to send a POST request to the /upload/ endpoint to upload a CSV file for processing.
- Use an API client to send a POST request to the /status/ endpoint to check the processing status using the request ID.

### Development

1. **To stop the development server, use:**
   ```bash
   ctrl + C


2. **To start the development server, use:**
   ```bash
   python manage.py runserver


### Contact
- For questions or comments, please reach out <mailto:manukrishna.s2001@gmail.com>






