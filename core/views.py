from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CategorySerializer, ReportSerializer
from .models import Report, Category
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django.http import Http404
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q

# Create your views here.


class CategoryListView(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryDetail(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            category = Category.objects.get(pk=pk)
            return category
        except Category.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        category = self.get_object(pk)
        serializer = CategorySerializer(category)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        category = self.get_object(pk)
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        category = self.get_object(pk)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ReportPagination(PageNumberPagination):
    page_size = 2
    max_page_size = 20
    page_size_query_param = 'page_size'


class ReportListView(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        reports = Report.objects.all().order_by('created_at')

        # Filter
        report_type = request.query_params.get('lost_item')
        status = request.query_params.get('lost_item')
        category = request.query_params.get('category')
        colour = request.query_params.get('colour')
        location = request.query_params.get('location')

        # Conditons
        if report_type is not None:
            reports = reports.filter(report_type__iexact=report_type)
        if status is not None:
            reports = reports.filter(status__iexact=report_type)
        if category is not None:
            reports = reports.filter(category__iexact=category)
        if colour is not None:
            reports = reports.filter(colour__iexact=colour)
        if location is not None:
            reports = reports.filter(loation__iexact=colour)

        # Pagination
        paginator = ReportPagination()
        page = paginator.paginate_queryset(reports, request)
        if page is not None:
            serializer = ReportSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)

        serializer = ReportSerializer(reports, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ReportSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReportDetailView(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_ojects(self, pk):
        try:
            report = Report.objects.get(pk=pk)
            return report
        except Report.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        report = self.get_ojects(pk)
        serializer = ReportSerializer(report)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        report = self.get_ojects(pk)
        serializer = ReportSerializer(report, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        report = self.get_ojects(pk)
        report.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ReportSearchView(APIView):

    def get(self, request):
        reports = Report.objects.all()
        search_item = request.query_params.get('search_item')
        if search_item is not None:
            reports = reports.filter(Q(item_name__icontains=search_item) | Q(description__icontains=search_item) | Q(
                colour__icontains=search_item) | Q(category__title__icontains=search_item) | Q(location__icontains=search_item)).distinct()
        serializer = ReportSerializer(reports, many=True)
        return Response(serializer.data)


class MyReportsView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        reports = Report.objects.filter(user=user)
        serializer = ReportSerializer(reports, many=True)
        return Response(serializer.data)
