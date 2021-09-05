import datetime
import time

from django.utils import timezone
from django.utils.timezone import make_aware


# 时间戳转换成datetime 带时区
def get_datetime_from_timestamp(timestamp):
    # print(time.time())
    # print(time.localtime(timestamp / 1000))
    # time.struct_time(tm_year=2021, tm_mon=4, tm_mday=26, tm_hour=15, tm_min=18, tm_sec=17, tm_wday=0, tm_yday=116,
    # tm_isdst=0)
    # datetime = time.localtime(timestamp / 1000)

    date = datetime.datetime.fromtimestamp(timestamp / 1000)
    aware_datetime = make_aware(date)  # 为本地时间增加时区信息
    return aware_datetime


# 获得当前时间 字符串
def get_now_datestr():
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))


# 字符串转日期  带时区
def get_dateitem_from_str_timezone(datetime_str):
    date = datetime.datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
    aware_datetime = make_aware(date)  # 为本地时间增加时区信息
    return aware_datetime


# 字符串转日期 不带时区
def get_dateitem_from_str(datetime_str):
    date = datetime.datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
    return date


# 不带时区时间 转换
def get_date(datetime_str):
    timezone.datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M:%S.%fZ').replace(tzinfo=None)
