from rest_framework import serializers
from .models import Category, Quote

class CategorySerializer(serializers.ModelSerializer):
    quotes = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'created_at', 'quotes']  # Include related quotes if needed

class QuoteSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)  # Display category details
    created_by = serializers.StringRelatedField()  # Display the username or related field of the user

    class Meta:
        model = Quote
        fields = [
            'id',
            'text',
            'author',
            'source',
            'category',
            'created_by',
            'is_featured',
            'created_at',
            'updated_at',
            'display_count'
        ]
