Image Processing App
Description
The Image Processing App is designed to process image data from CSV files. It uses Django and PostgreSQL to manage and process image data, allowing users to upload CSV files containing image URLs, compress the images, and generate output CSV files with processed image URLs.

Technologies Used
Backend: Django, Django REST Framework
Database: PostgreSQL
Installation
Prerequisites
Python 3.8+
Pip
Setup
Clone the repository:

bash
Copy code
git clone https://github.com/codewithmanuu/image-processing-app.git
Navigate into the project directory:

bash
Copy code
cd image-processing-app
Create a virtual environment:

bash
Copy code
python -m venv venv
Activate the virtual environment:

On Windows:

bash
Copy code
venv\Scripts\activate
On macOS/Linux:

bash
Copy code
source venv/bin/activate
Install dependencies:

bash
Copy code
pip install -r requirements.txt
Apply database migrations:

bash
Copy code
python manage.py makemigrations
python manage.py migrate
Create a superuser for accessing the Django admin panel:

bash
Copy code
python manage.py createsuperuser
Usage
Access the application at http://localhost:8000/api/v1/
Access the Django admin panel at http://localhost:8000/admin/
Use an API client to send a POST request to the /upload/ endpoint to upload a CSV file for processing.
Use an API client to send a POST request to the /status/ endpoint to check the processing status using the request ID.
Development
To stop the development server, use:

bash
Copy code
ctrl + C
To start the development server, use:

bash
Copy code
python manage.py runserver
Contact
For questions or comments, please reach out at mailto:manukrishna.s2001@gmail.com