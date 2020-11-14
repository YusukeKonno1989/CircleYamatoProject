import mysql.connector
import os
import traceback
import datetime
import pytz
import const
from sshtunnel import SSHTunnelForwarder
from Circle.models import Members, Schedule, Forum
from django.template.response import TemplateResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.views.generic.edit import FormView
from django.views.generic import TemplateView
from django.contrib.auth import mixins
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from . import mixinCalendar
from _datetime import date
from .forms import ScheduleForm, ContactForm, ForumForm
from django.utils import timezone
from django.views.generic.list import ListView
from pure_pagination.mixins import PaginationMixin

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

class MySchedule(LoginRequiredMixin, mixinCalendar.MonthCalendarMixin, mixinCalendar.WeekWithScheduleMixin, generic.CreateView):
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

class ForumFormView(LoginRequiredMixin, PaginationMixin, generic.CreateView, ListView):
    """
    掲示板用ビュー
    """

    template_name = os.path.join(os.path.dirname(__file__), 'templates/forum.html')
    model = Forum
    form_class = ForumForm
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self):
        return Forum.objects.all().order_by("posted_date").reverse()

    def form_valid(self, form):

        contents = form.data["contents"]

        forum = form.save(commit=False)

        """データ設定"""
        forum.name = self.request.user
        forum.contents = contents
        forum.good_count = 0
        forum.posted_date = datetime.datetime.now(pytz.timezone('Asia/Tokyo'))
        forum.update_date = datetime.datetime.now(pytz.timezone('Asia/Tokyo'))
        forum.commit_date = datetime.datetime.now(pytz.timezone('Asia/Tokyo'))
        forum.save()

        return redirect('Circle:forum')

    def form_invalid(self, form):
        test = ""

class ForumFormLikeView(LoginRequiredMixin, PaginationMixin, generic.CreateView, ListView):
    """
    掲示板用ビュー(いいね押下時)
    """

    template_name = os.path.join(os.path.dirname(__file__), 'templates/forum.html')
    model = Forum
    form_class = ForumForm
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        save_id = self.kwargs.get('id', 0)
        forum = Forum.objects.get(id=save_id)

        """データ設定"""
        forum.good_count = forum.good_count + 1
        forum.update_date = datetime.datetime.now(pytz.timezone('Asia/Tokyo'))
        forum.save()

        return context

    def get_queryset(self):
        return Forum.objects.all().order_by("posted_date").reverse()

    def form_valid(self, form):

        paginate_by = 3
        contents = form.data["contents"]

        forum = form.save(commit=False)

        """データ設定"""
        forum.name = self.request.user
        forum.contents = contents
        forum.good_count = 0
        forum.posted_date = datetime.datetime.now(pytz.timezone('Asia/Tokyo'))
        forum.update_date = datetime.datetime.now(pytz.timezone('Asia/Tokyo'))
        forum.commit_date = datetime.datetime.now(pytz.timezone('Asia/Tokyo'))
        forum.save()

        return redirect('Circle:forum')
