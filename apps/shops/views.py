from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView, GenericAPIView, UpdateAPIView, CreateAPIView, ListCreateAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from shared.django.pagination import PageSortNumberPagination
from shared.django.permissions import IsOwnerBasePermission
from shops.models import Country, Currency, Language, Shop, ShopCategory, Category
from shops.serializer import (CountryModelSerializer, CurrencyModelSerializer,
                              LanguageModelSerializer,
                              ShopCategoryModelSerializer, ShopModelSerializer, CategoryModelSerializer)


class ShopModelViewSet(ModelViewSet):
    queryset = Shop.objects.all()
    serializer_class = ShopModelSerializer
    pagination_class = PageSortNumberPagination

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        shop = self.get_object()
        serializer = self.get_serializer(shop, data=self.request.data, partial=True, context={'request': self.request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ShopCategoryListAPIView(ListAPIView):
    queryset = ShopCategory.objects.all()
    serializer_class = ShopCategoryModelSerializer


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


@extend_schema(tags=['Category'])
class CategoryCreateAPIView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryModelSerializer
    pagination_class = PageSortNumberPagination
    permission_classes = [IsOwnerBasePermission]

    def get_queryset(self):
        return super().get_queryset().filter(shop__owner=self.request.user)

    def category(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
