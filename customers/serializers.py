from dataclasses import fields
from pyexpat import model
from rest_framework import serializers
from .models import customers

class CustomersSerializer(serializers.ModelSerializer):
    class Meta:
        model = customers
        fields = ('pk','first_name', 'last_name', 'email', 'phone','address','description')
