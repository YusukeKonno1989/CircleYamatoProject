from django.db import models
from django.utils import timezone

class Members(models.Model):

    """メンバーテーブル"""
    name = models.TextField("name")
    sex = models.TextField("sex")
    age =models.IntegerField("age")
    update_date = models.DateTimeField("update_date")
    commit_date = models.DateTimeField("commit_date")

    def __str__(self):
        return self.name

    class Meta:
        db_table = "MEMBERS"
        verbose_name = verbose_name_plural = "メンバー"


class Schedule(models.Model):

    """スケジュールテーブル"""
    schedule_date = models.DateField("日付")
    start_time = models.TimeField("開始時間")
    end_time =models.TimeField("終了時間")
    summary =models.TextField("概要", max_length=50)
    description =models.TextField("詳細な内容", blank=True)
    update_date = models.DateTimeField("更新日付")
    commit_date = models.DateTimeField("作成日")

    class Meta:
        db_table = "SCHEDULE"
        verbose_name = verbose_name_plural = "スケジュール"

class Forum(models.Model):

    """掲示板テーブル"""
    posted_date = models.DateTimeField("投稿日付")
    name = models.TextField("名前")
    contents =models.TextField("内容")
    good_count =models.IntegerField("いいねカウント")
    update_date = models.DateTimeField("更新日付")
    commit_date = models.DateTimeField("作成日")

    class Meta:
        db_table = "FORUM"
        verbose_name = verbose_name_plural = "掲示板"