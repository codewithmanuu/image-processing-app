from rest_framework import serializers
from .models import RequestObject
from .mixins import create_request_id

class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestObject
        fields = ["input_file"]

    def validate_input_file(self, value):
        if not value.name.endswith('.csv'):
            raise serializers.ValidationError("Only CSV files are allowed.")
        return value

    def create(self, validated_data):
        validated_data['request_id'] = create_request_id()
        return super().create(validated_data)
    
class StatusViewSerializer(serializers.Serializer):
    request_id = serializers.CharField(max_length=500)