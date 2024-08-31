import csv
import io
import uuid

import boto3
import pandas as pd
import requests
from django.conf import settings
from django.core.files.base import ContentFile
from PIL import Image

from .models import RequestObject

s3_client = s3_client = boto3.client(
    "s3",
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
)


def create_request_id():
    slug = uuid.uuid4()
    if RequestObject.objects.filter(request_id=slug).exists():
        return create_request_id()
    else:
        return slug


def compress_image(url, quality=50):
    response = requests.get(url)
    image_data = response.content
    image = Image.open(io.BytesIO(image_data))
    image.thumbnail((300, 300))
    output = io.BytesIO()
    image.save(output, format="JPEG", quality=quality)
    output.seek(0)

    return output


def upload_to_s3(output, request_id, idx):
    file_path = f"{request_id}/img_{idx}.jpeg"
    s3_client.upload_fileobj(output, settings.AWS_STORAGE_BUCKET_NAME, file_path)
    output_url = f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.{settings.AWS_S3_REGION_NAME}.amazonaws.com/{file_path}"
    return output_url


def generate_output_csv(reqobj, output_csv, output_urls):
    output_csv["Output urls"] = output_urls
    csv_data = output_csv.to_csv(index=False)
    csv_file = ContentFile(csv_data, name=f"{str(reqobj.request_id)}.csv")
    reqobj.output_file.save(csv_file.name, csv_file, save=False)
    reqobj.save()
    return True


def validate_csv(file):
    errors = []
    required_columns = ["S. No.", "Product Name", "Input Image Urls"]

    file.seek(0)

    reader = csv.DictReader(file.read().decode("utf-8-sig").splitlines())
    headers = reader.fieldnames

    if not all(column in headers for column in required_columns):
        errors.append(
            "Missing required columns: Serial Number, Product Name, Input Image Urls"
        )
        return errors

    for i, row in enumerate(reader, start=1):
        serial_number = row["S. No."]
        if not serial_number.isdigit():
            errors.append(
                f"Row {i}: Invalid Serial Number '{serial_number}'. It should be a number."
            )

        product_name = row["Product Name"]
        if not product_name.strip():
            errors.append(f"Row {i}: Product Name cannot be empty.")

        input_image_urls = row["Input Image Urls"]
        if not input_image_urls.strip():
            errors.append(f"Row {i}: Input Image Urls cannot be empty.")

    return errors
