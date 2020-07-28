from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.urls import include, path
from . import views
import os

app_name = 'Circle'

urlpatterns = [
    path('', views.index, name="index"),
    path('Circle/', include('django.contrib.auth.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('Circle/schedule/', views.schedule, name="schedule"),
    path('Circle/schedule/month/', views.MonthCalendar.as_view(), name="month"),
    path('Circle/schedule/month/<int:year>/<int:month>/', views.MonthCalendar.as_view(), name="month"),
    path('Circle/schedule/week/', views.WeekCalendar.as_view(), name="week"),
    path('Circle/schedule/week/<int:year>/<int:month>/<int:day>/', views.WeekCalendar.as_view(), name="week"),
    path('Circle/schedule/week_with_schedule/', views.WeekWithScheduleCalendar.as_view(), name="week_with_schedule"),
    path(
        'Circle/schedule/week_with_schedule/<int:year>/<int:month>/<int:day>/',
        views.WeekWithScheduleCalendar.as_view(),
        name="week_with_schedule"
    ),
    path('Circle/schedule/myschedule/', views.MySchedule.as_view(), name="myschedule"),
    path('Circle/schedule/myschedule/<int:year>/<int:month>/<int:day>/', views.MySchedule.as_view(), name="myschedule"),
    path('Circle/contact/', views.ContactFormView.as_view(), name="contact_form"),
    path('Circle/contact/result/', views.ContactResultView.as_view(), name="contact_result"),
]