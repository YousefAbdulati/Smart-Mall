from importlib.resources import read_binary
from itertools import product
from django.db import transaction
from rest_framework import serializers
from .models import *
from account.utils import Util




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
        fields = ["id", "date_created", "name", "email" ,'rating', "description" ,'avg_rating','rating_count' ]
        extra_kwargs={
          'email':{'write_only':True},
        }
    
    def create(self, validated_data):
        product_id = self.context["product_id"]
        review=Review.objects.create(product_id = product_id,  **validated_data)
        
        # Send EMail
        email = validated_data.get('email', '')  # Retrieve email from validated_data
        link = f'http://localhost:3000/update-review/{product_id}/{review.id}'
        body = f'thanks for your Review , your rating : {review.rating} , Click Following Link to update your review ' +  link
        print(email, link)

        data = {
          'subject':'Your Review',
          'body':body,
          'to_email':email,
        }
        Util.send_email(data)
    
        return review



class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id","name", "price"]
        
        
        
