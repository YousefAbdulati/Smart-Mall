from importlib.resources import read_binary
from itertools import product
from django.db import transaction
from rest_framework import serializers
from .models import *



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["category_id", "title"]


class ProductSerializer(serializers.ModelSerializer):
    avg_rating = serializers.FloatField(read_only=True)
    rating_count = serializers.IntegerField(read_only=True)
    class Meta:
        model = Product
        fields = '__all__'
    


class ReviewSerializer(serializers.ModelSerializer):
    avg_rating = serializers.FloatField(source='product.avg_rating', read_only=True)
    rating_count = serializers.IntegerField(source='product.rating_count', read_only=True)

    class Meta:
        model = Review
        fields = ["id", "date_created", "name", 'rating', "description" ,'avg_rating','rating_count' ]
    
    def create(self, validated_data):
        product_id = self.context["product_id"]
        return Review.objects.create(product_id = product_id,  **validated_data)


class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id","name", "price"]
        
        
        
