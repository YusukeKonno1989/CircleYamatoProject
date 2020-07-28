import calendar
import datetime
import itertools
from collections import deque

class BaseCalendarMixin:
    """
    カレンダー関連のベースクラス
    """

    first_week_day = 0
    week_names = ['月', '火', '水', '木', '金', '土', '日']

    def setup_calendar(self):
        """
        週の初めの曜日を設定する処理
        """

        self._calendar = calendar.Calendar(self.first_week_day)

    def get_week_names(self):
        """
        最初に表示される曜日に合わせてweek_namesをシフトする
        """

        week_names = deque(self.week_names)
        week_names.rotate(-self.first_week_day)
        return week_names

class MonthCalendarMixin(BaseCalendarMixin):
    """
    月間カレンダークラス
    """

    def get_previous_month(self, date):
      """
      前月を返す
      """

      if date.month == 1:
          """1月の場合は前年の12月を返す"""
          return date.replace(year=date.year-1, month=12, day=1)
      else:
          return date.replace(month=date.month-1, day=1)

    def get_next_month(self, date):
        """
        次月を返す
        """

        if date.month == 12:
            """12月の場合は次年の1月を返す"""
            return date.replace(year=date.year+1, month=1, day=1)
        else:
            return date.replace(month=date.month+1, day=1)

    def get_month_days(self, date):
        """
        指定した月のすべての日を返す
        """

        return self._calendar.monthdatescalendar(date.year, date.month)

    def get_current_month(self):
        """
        現在月を返す
        """

        month = self.kwargs.get('month')
        year = self.kwargs.get('year')

        if month and year:
            month = datetime.date(year=int(year), month=int(month), day=1)
        else:
            month = datetime.date.today().replace(day=1)
        return month

    def get_month_calendar(self):
        """
        月間カレンダー情報を保持した辞書を返す
        """

        self.setup_calendar()
        current_month = self.get_current_month()
        calendar_data = {
            'now': datetime.date.today(),
            'month_days': self.get_month_days(current_month),
            'month_current': current_month,
            'month_previous': self.get_previous_month(current_month),
            'month_next': self.get_next_month(current_month),
            'week_names': self.get_week_names(),
        }
        return calendar_data

class WeekCalendarMixin(BaseCalendarMixin):
    """
    週間カレンダークラス
    """

    def get_week_days(self):
        """
        その週のすべての日を返す
        """

        month = self.kwargs.get('month')
        year = self.kwargs.get('year')
        day = self.kwargs.get('day')

        if month and year and day:
            date = datetime.date(year=int(year), month=int(month), day=int(day))
        else:
            date = datetime.date.today()

        for week in self._calendar.monthdatescalendar(date.year, date.month):
            if date in week:
                return week

    def get_week_calendar(self):
        """
        週間カレンダー情報を保持した辞書を返す
        """

        self.setup_calendar()
        days = self.get_week_days()
        first = days[0]
        last = days[-1]
        calendar_data = {
            'now': datetime.date.today(),
            'week_days': days,
            'week_previous': first - datetime.timedelta(days=7),
            'week_next': first + datetime.timedelta(days=7),
            'week_names': self.get_week_names(),
            'week_first': first,
            'week_last': last,
        }
        return calendar_data

class WeekWithScheduleMixin(WeekCalendarMixin):
    """
    スケジュール付き週間カレンダークラス
    """

    def get_week_schedules(self, start, end, days):
        """
        日とスケジュールを返す
        """

        lookup = {
            '{}__range'.format(self.date_field): (start, end)
        }

        queryset = self.model.objects.filter(**lookup)

        day_schedules = {day: [] for day in days}
        for schedule in queryset:
            schedule_date = getattr(schedule, self.date_field)
            day_schedules[schedule_date].append(schedule)
        return day_schedules

    def get_week_calendar(self):
        calendar_context = super().get_week_calendar()
        calendar_context['week_day_schedules'] = self.get_week_schedules(
            calendar_context['week_first'],
            calendar_context['week_last'],
            calendar_context['week_days']
        )
        return calendar_context