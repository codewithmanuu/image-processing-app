from django.conf import settings
from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .mixins import validate_csv
from .models import RequestObject
from .serializers import RequestSerializer, StatusViewSerializer
from .tasks import process_image

# Create your views here.


class UploadApi(GenericAPIView):
    allowed_methods = ["POST"]
    permission_classes = [AllowAny]
    serializer_class = RequestSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            file = request.FILES.get("input_file")
            errors = validate_csv(file)
            if errors:
                return Response({"errors": errors}, status=status.HTTP_400_BAD_REQUEST)
            obj = serializer.save()
            process_image.delay(obj.request_id)
            return Response(
                {"message": "File uploaded successfully", "RequestID": obj.request_id},
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ViewSatus(GenericAPIView):
    allowed_methods = ["POST"]
    permission_classes = [AllowAny]
    serializer_class = StatusViewSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            try:
                request_id = serializer.validated_data.get("request_id")
                req_obj = RequestObject.objects.get(request_id=request_id)
                if req_obj.status == "completed":
                    return Response(
                        {
                            "status": req_obj.status,
                            "Output file": f"{settings.DOMAIN}{req_obj.output_file.url}",
                        },
                        status=status.HTTP_200_OK,
                    )
                else:
                    return Response(
                        {"status": req_obj.status}, status=status.HTTP_200_OK
                    )
            except req_obj.DoesNotExist:
                return Response(
                    {"error": "Invalid request_id"}, status=status.HTTP_404_NOT_FOUND
                )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
