import datetime
import decimal
import json


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    try:
        columns = [col[0] for col in cursor.description]
        return [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]
    except:
        print('查询数据为 None ')
        return []


# 装换datetime格式到String类型
class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        # print(type(obj))
        if isinstance(obj, datetime.datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        elif isinstance(obj, datetime.date):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        elif isinstance(obj, decimal.Decimal):
            return float(obj)
        else:
            return json.JSONEncoder.default(self, obj)