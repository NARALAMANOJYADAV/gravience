from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.counseling_form_view, name='counseling_form'),
    path('success/', views.success_view, name='success'),
    path('approve/<int:pk>/', views.approve_view, name='approve'),
    path('submissions/', views.submissions_view, name='submissions'),
    path('view-approval/', views.view_approval, name='view_approval'),
    path('status/<str:roll>/', views.status_by_roll, name='status_by_roll'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
]

