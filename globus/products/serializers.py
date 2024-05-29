from rest_framework import serializers

from .models import (
    Product,
    Category,
    SubCategory,
)


class ProductSerializer(serializers.ModelSerializer):
    img = serializers.SerializerMethodField()

    price = serializers.SerializerMethodField()
    old_price = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = "__all__"

    def get_img(self, obj):
        if obj.img:
            return f"https://globus.store{obj.img.url}"
        return None
    
    def get_old_price(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            if user.user_roll == '2':
                return f'{obj.wholesale_price}'
            return f'{obj.old_price}'
        return f'{obj.old_price}'

    def get_price(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            if user.user_roll == '2':
                return None
            return f'{obj.price}'
        return f'{obj.price}'
            

    
    


class SubCategoriesListSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = "__all__"


class CategoriesListSerializer(serializers.ModelSerializer):
    img = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ["id", "name", "img"]

    def get_img(self, obj):
        return f"https://globus.store{obj.img.url}"