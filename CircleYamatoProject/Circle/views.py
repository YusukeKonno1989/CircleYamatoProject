import mysql.connector
import os
import traceback
import datetime
import const
from sshtunnel import SSHTunnelForwarder
from Circle.models import Members
from Circle.models import Schedule
from django.template.response import TemplateResponse
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.views.generic.edit import FormView
from django.views.generic import TemplateView
from django.contrib.auth import mixins
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from . import mixinCalendar
from _datetime import date
from .forms import ScheduleForm
from .forms import ContactForm

def index(request):

#     members = Members.objects.all()
#
#     print(members.values("age"))

    return TemplateResponse(request, os.path.join(os.path.dirname(__file__), 'templates/index.html'))

def login(request):
    return TemplateResponse(request, os.path.join(os.path.dirname(__file__), 'templates/login.html'))

class ContactFormView(FormView):
    """
    お問い合わせフォーム表示処理
    """
    template_name = os.path.join(os.path.dirname(__file__), 'templates/contact_form.html')
    form_class = ContactForm
    success_url = reverse_lazy('Circle:contact_result')

    def form_valid(self, form):
        form.send_email()
        return super().form_valid(form)

class ContactResultView(TemplateView):
    """
    お問い合わせ結果フォーム表示処理
    """
    template_name = os.path.join(os.path.dirname(__file__), 'templates/contact_result.html')

    def get_context_date(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['success'] = "お問い合わせは送信されました。"
        return context

@login_required
def schedule(request):
    return TemplateResponse(request, os.path.join(os.path.dirname(__file__), 'templates/schedule.html'))


class MonthCalendar(mixinCalendar.MonthCalendarMixin, generic.TemplateView):
    """
    月間カレンダー表示処理
    """
    template_name = os.path.join(os.path.dirname(__file__), 'templates/month.html')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        calendar_context = self.get_month_calendar()
        context.update(calendar_context)
        return context

class WeekCalendar(mixinCalendar.WeekCalendarMixin, generic.TemplateView):
    """
    週間カレンダー表示処理
    """
    template_name = os.path.join(os.path.dirname(__file__), 'templates/week.html')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        calendar_context = self.get_week_calendar()
        context.update(calendar_context)
        return context


class WeekWithScheduleCalendar(mixinCalendar.WeekWithScheduleMixin, generic.TemplateView):
    """
    スケジュール付き週間カレンダー表示処理
    """
    template_name = os.path.join(os.path.dirname(__file__), 'templates/week_with_schedule.html')
    model = Schedule
    date_field = 'schedule_date'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        calendar_context = self.get_week_calendar()
        context.update(calendar_context)
        return context

class MySchedule(mixinCalendar.MonthCalendarMixin, mixinCalendar.WeekWithScheduleMixin, generic.CreateView):
    """
    月間カレンダー、週間カレンダー、スケジュール登録画面をまとめたビュー
    """

    template_name = os.path.join(os.path.dirname(__file__), 'templates/myschedule.html')
    model = Schedule
    date_field = 'schedule_date'
    form_class = ScheduleForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        week_calendar_context = self.get_week_calendar()
        month_calendar_context = self.get_month_calendar()
        context.update(week_calendar_context)
        context.update(month_calendar_context)
        return context

    def form_valid(self, form):
        month = self.kwargs.get('month')
        year = self.kwargs.get('year')
        day = self.kwargs.get('day')
        if month and year and day:
            date = datetime.date(year=int(year), month=int(month), day=int(day))
        else:
            date = datetime.date.today()
        schedule = form.save(commit=False)
        schedule.schedule_date = date
        schedule.commit_date = datetime.date.today()
        schedule.update_date = datetime.date.today()
        schedule.save()
        return redirect('Circle:myschedule', year=date.year, month=date.month, day=date.day)
