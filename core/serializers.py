from rest_framework import serializers
from .models import Report, Category



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields = '__all__'


class ReportSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='categor.name', read_only=True)

    class Meta:
        model= Report
        fields = [
            'user',
            'id',
            'report_type',
            'status',
            'category',
            'category_name',
            'item_name',
            'colour',
            'description',
            'location',
            'date_incident',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['created_at', 'updated_at', 'category_name', 'id',]
