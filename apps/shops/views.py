from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from shared.django.pagination import PageSortNumberPagination
from shops.models import Country, Currency, Language, Shop, ShopCategory
from shops.serializer import (CountryModelSerializer, CurrencyModelSerializer,
                              LanguageModelSerializer,
                              ShopCategoryModelSerializer, ShopModelSerializer)


class ShopCreateAPIView(ModelViewSet):
    queryset = Shop.objects.all()
    serializer_class = ShopModelSerializer
    http_method_names = ['get', 'post', 'patch', 'head', 'options']
    permission_classes = [IsAuthenticated, ]
    pagination_class = PageSortNumberPagination

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)

    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = ShopModelSerializer(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ShopCategoryListAPIView(ListAPIView):
    queryset = ShopCategory.objects.all()
    serializer_class = ShopCategoryModelSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        return ShopCategory.objects.filter(shop__owner=self.request.user)


class CurrencyListAPIView(ListAPIView):
    queryset = Currency.objects.all()
    serializer_class = CurrencyModelSerializer
    pagination_class = None


class LanguageListAPIView(ListAPIView):
    queryset = Language.objects.all()
    serializer_class = LanguageModelSerializer
    pagination_class = None


class CountryListAPIView(ListAPIView):
    queryset = Country.objects.all()
    serializer_class = CountryModelSerializer
