from django.urls import path
from . import views

urlpatterns = [
    path('category/', views.CategoryListView.as_view(), name='category-list'),
    path('category/<int:pk>/', views.CategoryDetail.as_view(), name='category-detail'),
    path('reports/', views.ReportListView.as_view(), name='report-list'),
    path('report/<int:pk>/', views.ReportDetailView.as_view(), name='report-detail'),
    path('reports/search/', views.ReportSearchView.as_view(), name='report-search'),
    path('reports/user/', views.MyReportsView.as_view(), name='my-reports'),
]
