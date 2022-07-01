from multiprocessing import context
from urllib import response
from webbrowser import get
from rest_framework.response import responses
from rest_framework.decorators import api_view
from rest_framework import status

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import customers
from .serializers import *

@api_view(['GET', 'POST'])
def customers_list(request):
    if request.method == "GET":
        data = []
        nextPage = 1
        previusPage = 1
        customers = customers.objects.all()
        page = request.GET.get('page', 1)
        paginator = Paginator(customers, 10)
        try:
            data = paginator.page(page)
        except PageNotAnInteger:
            data = paginator.page(1)
        except EmptyPage:
            data = paginator.page(paginator.num_pages)

        serializers = CustomersSerializer(data, context={'request' : request}, many=True)
        if data.has_next():
            nextPage = data.next_page_number()
        if data.has_previous():
            previusPage = data.previous_page_number()
        
        return response({'data' : serializers.data, 'count' : paginator.count, 'numpages' : paginator.num_pages, 'nextlink' : '/api/customers/?page=' + nextPage, 'prevlink' : '/api/customers/?page=' + previusPage}) 

    elif request.method == 'POST':
        serializer = CustomersSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response(serializer.data, status=status.HTTP_201_CREATED)
        return response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def customers_detail(request, pk):
    try:
        customers = customers.objects.get(pk=pk)
    except customers.DoesNotExist:
        return response(status = status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializers = CustomersSerializer(customers, context={'request' : request})
        return response(serializers.data)
    elif request.method == 'PUT':
        serializers = CustomersSerializer(customers, data=request.data, context={'request' : request})
        if serializers.is_valid():
            serializers.save
            return response(serializers.data)
        return response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        customers.delete()
        return response(status=status.HTTP_204_NO_CONTENT)

