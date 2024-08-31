import logging

import pandas as pd
from celery import shared_task
from django.conf import settings
from PIL import Image

from .mixins import compress_image, generate_output_csv, upload_to_s3
from .models import RequestObject

logger = logging.getLogger("error_payload")


@shared_task
def process_image(request_id):
    try:
        req_obj = RequestObject.objects.get(request_id=request_id)
        input_csv_path = req_obj.input_file.path
        req_obj.status = "processing"
        req_obj.save()

        input_csv = pd.read_csv(input_csv_path)
        urls = input_csv["Input Image Urls"]
        output_urls = []
        for idx, url in enumerate(urls):
            idx += 1
            output = compress_image(url)
            output_url = upload_to_s3(output, request_id, idx)
            output_urls.append(output_url)

        if generate_output_csv(req_obj, input_csv, output_urls):
            req_obj.status = "completed"
            req_obj.save()
        else:
            req_obj.status = "failed"
            req_obj.save()

    except Exception as e:
        logger.debug(f"Failed to process image for request_id {request_id}: {e}")
        req_obj.status = "failed"
        req_obj.save()
