from rest_framework import serializers
from .models import Category, Product, Review



class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'

    def validate_name(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("Category name must be at least 3 characters.")
        return value


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than 0.")
        return value

    def validate_name(self, value):
        if len(value) < 2:
            raise serializers.ValidationError("Product name is too short.")
        return value


class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = '__all__'

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value

    def validate_text(self, value):
        if len(value) < 5:
            raise serializers.ValidationError("Review text is too short.")
        return value