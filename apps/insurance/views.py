import traceback
import uuid, os, sys, requests, json, re, time, datetime, random, hashlib, hmac, base64, xml, subprocess, threading
from copy import deepcopy
from decimal import Decimal

from django.db import connection, transaction
from django.db.models import F, Q
from django.http import JsonResponse
from django.utils.timezone import make_aware
from rest_framework import serializers, status, generics, mixins, viewsets
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.forms.models import model_to_dict
# 官方JWT
# from rest_framework_jwt.utils import jwt_payload_handler, jwt_encode_handler ,jwt_response_payload_handler
# from rest_framework_jwt.authentication import JSONWebTokenAuthentication
# 缓存配置
from django.core.cache import cache
# 自定义的JWT配置 公共插件
from utils.datetime_util import get_dateitem_from_str
from utils.utils import jwt_decode_handler, jwt_encode_handler, jwt_payload_handler, jwt_payload_handler, \
    jwt_response_payload_handler, google_otp, VisitThrottle, getDistance, NormalObj, \
    wechat_mini_login, wechat_app_login, get_wechat_token
from utils.WeChatCrypt import WXBizDataCrypt
from utils.AliMsg import create_code, SendSmsObject
from utils.jwtAuth import JWTAuthentication
from utils.pagination import Pagination
from utils.permissions import JWTAuthPermission, AllowAllPermission, BaseAuthPermission
from .filters import InsurancePolicyDateFilterBackend, DoctorsFilter
from .models import *
from .serializers import *
from functools import reduce
from urllib.parse import unquote_plus
from django.conf import settings
from utils.db_util import dictfetchall


# 根据渠道匹配规则 匹配渠道
def match_insurance_chanel():
    sql = '''select a.*, a.id as insuranceid,b.channel_name,c.id as channelid from insurance_policy a 
    join channel_match b on a.applicant = b.applicant and b.insured = a.insured and b.vehicel_owner = a.vehicel_owner
    left join channel_rate c on c.chanel = b.channel_name
    where a.chanel_rate_id_id is null
    '''
    cur = connection.cursor()
    cur.execute(sql)
    data = dictfetchall(cur)

    succ_count = 0

    for i in data:
        if i['channelid'] is not None:
            insurance = InsurancePolicy.objects.get(id=i['insuranceid'])
            insurance.chanel_rate_id = ChannelRate.objects.get(id=i['channelid'])
            insurance.save()
            i['matched'] = '成功匹配' + i['channel_name'] + '渠道'
            succ_count = succ_count + 1
        else:
            channels = ChannelRate.objects.filter(chanel=i['channel_name'])
            if len(channels) == 0:
                channel = ChannelRate.objects.create(chanel=i['channel_name'])
                insurance = InsurancePolicy.objects.get(id=i['insuranceid'])
                insurance.chanel_rate_id = channel
                insurance.save()
                i['matched'] = '匹配成功，系统新创建' + i['channel_name'] + '渠道'
                succ_count = succ_count + 1
            else:
                insurance = InsurancePolicy.objects.get(id=i['insuranceid'])
                insurance.chanel_rate_id = channels[0]
                insurance.save()
                i['matched'] = '成功匹配' + i['channel_name'] + '渠道'
                succ_count = succ_count + 1

    data = {'message': 'ok', 'errorCode': 0, 'succ_count': succ_count, 'data': data}
    return data


# 传入的 headers column 均为 pandas.Series对象
def get_model_from_pandas(model_instance, headers, column):
    row_index = list(headers.index)
    # print('row_index', row_index)
    arr_fields = model_instance._meta.fields
    for i in arr_fields:
        try:
            # print('字段类型:', type(i).__name__)
            # print(i.name, json_info[i.name])

            # 复制 row_index  index相当于索引   headers, column 是一个 pandas.Series 对象

            for index in row_index:
                # print('headers[index]', headers[index])
                if i.verbose_name in headers[index]:

                    # 去掉 空值
                    if str(column[index]) == 'nan':
                        pass
                    else:
                        setattr(model_instance, i.name, column[index])
                    # 去掉一个匹配的属性，避免重复对比
                    headers.drop(index)
        except KeyError as e:
            traceback.print_exc()
            pass
            # if e.__str__() == '\'id\'':
            #     # 新增时没有id
            #     pass
            # else:
            #     import traceback
            #     traceback.print_exc()    # 打印到控制台
            #     traceback.format_exc()   # 返回str
            #     # 这里需要写入错误日志
    return model_instance


def get_model_from_json(model_instance, json_info):
    arr_fields = model_instance._meta.fields
    for i in arr_fields:
        try:
            # print('字段类型:', type(i).__name__)
            # print(i.name, json_info[i.name])

            if hasattr(model_instance, i.name):
                # 时间戳转换成datetime
                if type(i).__name__ == 'DateTimeField':
                    # print('转换成日期') 判断是否是日期类型，是就不转换
                    # print(type(json_info[i.name]))
                    # print(isinstance(json_info[i.name], datetime.datetime))
                    if isinstance(json_info[i.name], datetime.datetime):
                        date = json_info[i.name]
                        # 为本地时间增加时区信息
                        date = make_aware(date)
                    else:
                        date = json_info[i.name]
                    setattr(model_instance, i.name, date)
                else:
                    setattr(model_instance, i.name, json_info[i.name])
        except KeyError as e:
            pass
            # if e.__str__() == '\'id\'':
            #     # 新增时没有id
            #     pass
            # else:
            #     import traceback
            #     traceback.print_exc()    # 打印到控制台
            #     traceback.format_exc()   # 返回str
            #     # 这里需要写入错误日志
    return model_instance


class FeeFieldViewset(ModelViewSet):
    '''费率字段管理'''
    queryset = FeeField.objects.order_by('-create_time')
    authentication_classes = (JWTAuthentication,)
    permission_classes = [BaseAuthPermission, ]
    throttle_classes = [VisitThrottle]
    serializer_class = FeeFieldSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter,)
    search_fields = ('name',)
    filter_fields = ('name',)
    ordering_fields = ('update_time', 'create_time',)
    pagination_class = Pagination

    def get_serializer_class(self):
        if self.action in ['list']:
            return ALlFeeFieldSerializer
        else:
            return FeeFieldSerializer


class ChannelRateViewset(ModelViewSet):
    '''渠道管理'''
    queryset = ChannelRate.objects.order_by('-create_time')
    authentication_classes = (JWTAuthentication,)
    permission_classes = [BaseAuthPermission, ]
    throttle_classes = [VisitThrottle]
    serializer_class = ChannelRateSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter,)
    search_fields = ('chanel',)
    filter_fields = ('chanel',)
    ordering_fields = ('update_time', 'create_time',)
    pagination_class = Pagination


class ChannelEffectiveTimeViewset(ModelViewSet):
    '''渠道生效时间管理'''
    queryset = ChannelEffectiveTime.objects.order_by('create_time')
    authentication_classes = (JWTAuthentication,)
    permission_classes = [BaseAuthPermission, ]
    throttle_classes = [VisitThrottle]
    serializer_class = ListChannelEffectiveTimeSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter,)
    search_fields = ('chanel_id',)
    filter_fields = ('chanel_id',)
    ordering_fields = ('update_time', 'create_time',)
    pagination_class = Pagination

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update', 'retrieve']:
            return ChannelEffectiveTimeSerializer
        else:
            return ListChannelEffectiveTimeSerializer

    @action(methods=['post'], detail=False, permission_classes=[AllowAllPermission])
    def update_effective_time(self, request):
        # print('request.data ------------------------------------------')
        # print(request.data)

        time_start = request.data['time_start']
        time_end = request.data['time_end']
        id = request.data['id']

        channelEffectiveTime = ChannelEffectiveTime.objects.get(id=id)

        # str 转换成 datetime.date
        time_tuple = time.strptime(time_start, '%Y-%m-%d')
        year, month, day = time_tuple[:3]
        time_start_ = datetime.date(year, month, day)

        time_tuple = time.strptime(time_end, '%Y-%m-%d')
        year, month, day = time_tuple[:3]
        time_end_ = datetime.date(year, month, day)

        time_arr = ChannelEffectiveTime.objects.exclude(id=id).filter(chanel_id=channelEffectiveTime.chanel_id.id)

        time_boolean_flag = False
        for item in time_arr:
            # 时间为空则跳过
            if item.time_start is not None or item.time_end is not None:
                if item.time_start <= time_start_ <= item.time_end:
                    time_boolean_flag = True
                    break
                if item.time_start <= time_end_ <= item.time_end:
                    time_boolean_flag = True
                    break

        if time_boolean_flag:
            raise serializers.ValidationError({'message': '修改失败,时间范围不能重叠'})
        else:

            channelEffectiveTime.time_start = time_start_
            channelEffectiveTime.time_end = time_end_
            channelEffectiveTime.save()

            data = {'message': 'ok', 'errorCode': '0'}
            return Response(data)


class ManyInsurancePolicyViewset(mixins.ListModelMixin, GenericViewSet):
    '''
        保单管理  渠道结算金额查询
        '''
    queryset = InsurancePolicy.objects.order_by('-create_time')
    authentication_classes = (JWTAuthentication,)
    permission_classes = [BaseAuthPermission, ]
    throttle_classes = [VisitThrottle]
    serializer_class = ManyListInsurancePolicySerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter, InsurancePolicyDateFilterBackend)
    search_fields = ('$jiaoqiang_insure_no', '$jiaoqiang_insurance_no', '$commercial_insure_no',
                     '$commercial_insurance_no',
                     '$chanel_rate_id__chanel', '$settlement_status', '$engine_number', '$nature_of_use',
                     '$business_source', '$salesman', '$license_plate', '$chassis_number', '$vehicel_owner')
    filter_fields = (
        'jiaoqiang_insure_no', 'nature_of_use', 'chanel_rate_id__chanel', 'settlement_status', 'business_source')
    ordering_fields = ('update_time', 'create_time',)
    pagination_class = Pagination


class InsurancePolicyViewset(ModelViewSet):
    '''
    保单管理
    '''
    queryset = InsurancePolicy.objects.order_by('-create_time')
    authentication_classes = (JWTAuthentication,)
    permission_classes = [BaseAuthPermission, ]
    throttle_classes = [VisitThrottle]
    serializer_class = InsurancePolicySerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter,)  # InsurancePolicyDateFilterBackend
    search_fields = ('$jiaoqiang_insure_no', '$nature_of_use', '$chanel_rate_id__chanel', '$settlement_status',
                     '$business_source', '$salesman')
    filter_fields = ('jiaoqiang_insure_no', 'nature_of_use', 'chanel_rate_id__chanel', 'settlement_status',
                     'business_source', 'auto_download_date')
    ordering_fields = ('update_time', 'create_time',)
    pagination_class = Pagination

    @action(detail=False, methods=['post', 'option'], permission_classes=[AllowAllPermission])
    def upload_json(self, request):
        try:
            print('request.data')
            print(request.data)
            insraunces = request.data['insurance_arr']
            auto_download_date = request.data['date']
            succes = 0
            chongfu = 0
            for i in insraunces:
                # 去掉id,防止已有的保单被修改
                if 'id' in i:
                    del i['id']

                # 跳过重复的保单
                q = InsurancePolicy.objects.filter(Q(commercial_insurance_no=i['commercial_insurance_no']) |
                                                   Q(jiaoqiang_insurance_no=i['jiaoqiang_insurance_no']))
                if len(q) > 0:
                    chongfu += 1
                else:
                    insurance_policy = get_model_from_json(InsurancePolicy(), i)
                    insurance_policy.auto_download_date = auto_download_date
                    insurance_policy.save()
                    succes += 1
            shibai = len(insraunces) - succes - chongfu
            return_str = '成功数量：' + str(succes) + ' 重复数量：' + str(chongfu) + ' 失败数量：' + str(shibai)
            json_data = {"message": "ok", "errorCode": 0, "data": return_str}
            query = AutoDownloadRecord.objects.filter(auto_download_date=auto_download_date)
            if len(query) <= 0:
                AutoDownloadRecord.objects.create(auto_download_date=auto_download_date, download_count=1,
                                                  log=return_str)
            else:
                for item in query:
                    item.auto_download_date = auto_download_date
                    item.download_count += 1
                    item.log = return_str
                    item.save()
            return Response(json_data)
        except Exception as e:
            traceback.print_exc()
            return Response({"message": "出现了无法预料的view视图错误：%s" % e.__str__(), "errorCode": 1, "data": {}})

    @action(detail=False, methods=['post', 'option'], permission_classes=[AllowAllPermission])
    def upload_excel(self, request):
        # 获取文件
        try:
            file_i = request.FILES.items()

            json_data = {"message": "ok", "errorCode": 0, "data": {}}
            # 这里面filename是用户上传的文件的key upfile是用户上传的文件名
            upload_file_list = []
            upload_host_url_list = []
            for key_name, up_file in file_i:
                print(key_name, up_file.name, up_file.size, up_file.read)

                file_name = up_file.name
                file_size = up_file.size
                check_file = file_name.split('.')[-1]
                new_file_name = 'upload_file'  # str(uuid.uuid1())
                if check_file.lower() not in ['xlsx', 'xls']:
                    json_data['message'] = file_name + '不是规定的类型(%s)！' % '/'.join(settings.FILE_CHECK)
                    json_data['errorCode'] = 2
                    return Response(json_data)
                if file_size > settings.FILE_SIZE:
                    json_data['message'] = file_name + '文件超过64mb，无法上传！'
                    json_data['errorCode'] = 2
                    return Response(json_data)
                # 获取存储的文件名
                save_file_name = new_file_name + '.' + check_file
                # 获取当前文件的绝对路径
                base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                upfile_base_dir = os.path.join(base_path, 'upload_file')
                is_have = os.path.exists(upfile_base_dir)
                if is_have:
                    save_path = os.path.join(upfile_base_dir, save_file_name)
                else:
                    os.makedirs(upfile_base_dir)
                    save_path = os.path.join(upfile_base_dir, save_file_name)
                with open(save_path, 'wb') as u_file:
                    for part in up_file.chunks():
                        u_file.write(part)
            # 文件路径
            print(save_path)
            host_file_url = 'http://' + settings.SERVER_NAME + '/upload_file/' + save_file_name

            json_data['data'] = host_file_url

            import pandas as pd

            df = pd.read_excel(save_path, header=None, dtype=object)

            print("行索引：{}".format(list(df.index)))
            row_index = list(df.index)
            print("列索引：{}".format(list(df.columns)))
            # column_index = list(df.columns)

            headers = None

            id_arr = []
            print('row_index_length', len(row_index))
            for i in row_index:
                if i == 0:
                    headers = df.iloc[i]
                else:
                    insurance_policy = get_model_from_pandas(InsurancePolicy(), headers, df.iloc[i])
                    insurance_policy.save()
                    id_arr.append(insurance_policy.pk)

            print('id_arr_length', len(row_index))
            match_insurance_chanel()
            queryset = InsurancePolicy.objects.filter(id__in=id_arr)
            serializer = InsurancePolicySerializer(queryset, many=True)
            return Response(serializer.data)
        except Exception as e:
            traceback.print_exc()
            return Response({"message": "出现了无法预料的view视图错误：%s" % e.__str__(), "errorCode": 1, "data": {}})

    @action(detail=False, methods=['get'], permission_classes=[AllowAllPermission])
    def get_insurance_model(self, request):
        pass

        model = self.get_serializer_class().Meta.model
        arr_fields = model()._meta.fields
        data = {}
        for i in arr_fields:
            # print('字段类型:', type(i).__name__)
            # print(i.name, i.verbose_name)
            data[i.name] = i.verbose_name

        json_data = {"message": "ok", "errorCode": 0, "data": data}
        return Response(json_data)

    def get_serializer_class(self):
        if self.action in ['list']:
            return ListInsurancePolicySerializer
        else:
            return InsurancePolicySerializer


class SettlementsViewset(ModelViewSet):
    '''
    结算管理
    get_settlements_insurance: 渠道结算金额查询
    '''
    queryset = Settlements.objects.order_by('-create_time')
    authentication_classes = (JWTAuthentication,)
    permission_classes = [BaseAuthPermission, ]
    throttle_classes = [VisitThrottle]
    serializer_class = SettlementsSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter,)
    search_fields = ('id',)
    filter_fields = ('id',)
    ordering_fields = ('update_time', 'create_time',)
    pagination_class = Pagination

    def get_serializer_class(self):
        if self.action in ['list']:
            return ListSettlementsSerializer
        else:
            return SettlementsSerializer

    # 批量结算保单  也适用于单个结算
    @action(detail=False, methods=['post', 'option'], permission_classes=[AllowAllPermission])
    @transaction.atomic()
    def sub_settlements(self, request):
        ids = request.data['insurance_arr']
        settlement = Settlements()
        settlement.actual_settlement_fee = request.data['actual_settlement_fee']
        # 字符串转换成日期
        settlement_date = get_dateitem_from_str(request.data['settlement_date'])
        settlement.settlement_date = settlement_date
        settlement.settlement_method = request.data['settlement_method']
        settlement.receiving_account = request.data['receiving_account']

        settlement.note = request.data['note']
        settlement.save()
        for i in ids:
            insurancePolicy = InsurancePolicy.objects.get(pk=i)
            insurancePolicy.settlements_id = settlement
            insurancePolicy.settlement_status = True
            insurancePolicy.save()

        data = {'message': 'ok', 'errorCode': 0}
        return Response(data)

    # 渠道结算金额查询
    @action(detail=False, methods=['post', 'option'], permission_classes=[AllowAllPermission])
    def get_settlements_insurance(self, request):
        try:
            insurance_id = request.data['insurance_id']
            generation_date = request.data['generation_date']
            nature_of_use = request.data['nature_of_use']

            # print(request.data)

            sql = '''select a.id, group_concat( concat_ws('-', e.name, e.fee)) as fee ,a.commercial_insurance_amount, 
                    a.jiaoqiang_insurance_amount  
                    from insurance_policy a 
                    join channel_rate b on a.chanel_rate_id_id = b.id
                    join  insurance_channeleffectivetime c on c.chanel_id_id = b.id
                    join insurance_channeleffectivetime_fee_field d on d.channeleffectivetime_id = c.id
                    join fee_field e on e.id = d.feefield_id
                    where a.id = {insurance_id} 
                    and '{generation_date}' >= c.time_start and '{generation_date}' <= c.time_end
                    and e.name like '%{nature_of_use}%'
                    and a.deleted is null
                    and b.deleted is null
                    and c.deleted is null
                    group by a.id;'''

            cur = connection.cursor()

            # print(sql.format(insurance_id=insurance_id, generation_date=generation_date, nature_of_use=nature_of_use))
            cur.execute(
                sql.format(insurance_id=insurance_id, generation_date=generation_date, nature_of_use=nature_of_use))
            data = dictfetchall(cur)

            if len(data) == 0:
                row_data = {'id': insurance_id, 'commercial_insurance_amount_fee': '暂无匹配费率',
                            'jiaoqiang_insurance_amount_fee': '暂无匹配费率'}
                data = {'message': 'ok', 'errorCode': 0, 'data': row_data}
                return Response(data)
            else:
                row_data = data[0]

                fee_str = row_data['fee'].split(',')
                print(row_data, fee_str)

                shangyefee = None
                jiaoqiangfee = None
                # + nature_of_use 全部字段是否相等，提取对应费率
                for item in fee_str:
                    if '商业险' + nature_of_use in item.split('-')[0]:
                        shangyefee = Decimal(item.split('-')[1])
                    if '交强险' + nature_of_use in item.split('-')[0]:
                        jiaoqiangfee = Decimal(item.split('-')[1])

                if shangyefee is not None:
                    if row_data['commercial_insurance_amount'] is None:
                        row_data['commercial_insurance_amount'] = 0
                    row_data['commercial_insurance_amount_fee'] = row_data[
                                                                      'commercial_insurance_amount'] * shangyefee / 100

                    row_data['commercial_fee'] = shangyefee
                else:
                    row_data['commercial_insurance_amount_fee'] = '暂无匹配费率'

                if jiaoqiangfee is not None:
                    if row_data['jiaoqiang_insurance_amount'] is None:
                        row_data['jiaoqiang_insurance_amount'] = 0
                    row_data['jiaoqiang_insurance_amount_fee'] = row_data[
                                                                     'jiaoqiang_insurance_amount'] * jiaoqiangfee / 100
                    row_data['jiaoqiang_fee'] = jiaoqiangfee
                else:
                    row_data['jiaoqiang_insurance_amount_fee'] = '暂无匹配费率'
                data = {'message': 'ok', 'errorCode': 0, 'data': row_data}
                return Response(data)
        except:
            traceback.print_exc()


class RemitViewset(ModelViewSet):
    '''
    打款明细管理
    '''
    queryset = Remit.objects.order_by('-create_time')
    authentication_classes = (JWTAuthentication,)
    permission_classes = [BaseAuthPermission, ]
    throttle_classes = [VisitThrottle]
    serializer_class = RemitSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter,)
    search_fields = ('id', 'settlement')
    filter_fields = ('id', 'settlement')
    ordering_fields = ('update_time', 'create_time',)
    pagination_class = Pagination


class HandlingFeeViewset(ModelViewSet):
    '''
    手续费管理
    '''
    queryset = HandlingFee.objects.order_by('-create_time')
    authentication_classes = (JWTAuthentication,)
    permission_classes = [BaseAuthPermission, ]
    throttle_classes = [VisitThrottle]
    serializer_class = HandlingFeeSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter,)
    search_fields = ('id',)
    filter_fields = ('id',)
    ordering_fields = ('update_time', 'create_time',)
    pagination_class = Pagination


class ChannelMatchViewset(ModelViewSet):
    '''
    渠道匹配管理
    match_insurance: 按照规则匹配所有未匹配渠道的保单
    '''
    queryset = ChannelMatch.objects.order_by('-create_time')
    authentication_classes = (JWTAuthentication,)
    permission_classes = [BaseAuthPermission, ]
    throttle_classes = [VisitThrottle]
    serializer_class = ChannelMatchSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter,)
    search_fields = ('channel_name', 'applicant', 'insured', 'vehicel_owner')
    filter_fields = ('id',)
    ordering_fields = ('update_time', 'create_time',)
    pagination_class = Pagination

    # 按照规则 匹配 所有 未匹配渠道的 保单
    @action(methods=['get'], detail=False, permission_classes=[AllowAllPermission])
    @transaction.atomic()
    def match_insurance(self, request):
        data = match_insurance_chanel()
        return Response(data)


class AutoDownloadRecordViewset(ModelViewSet):
    '''
    自动下载记录
    match_insurance: 按照规则匹配所有未匹配渠道的保单
    '''
    queryset = AutoDownloadRecord.objects.order_by('-create_time')
    authentication_classes = (JWTAuthentication,)
    permission_classes = [BaseAuthPermission, ]
    throttle_classes = [VisitThrottle]
    serializer_class = AutoDownloadRecordSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter,)
    search_fields = ('auto_download_date',)
    filter_fields = ('id', 'auto_download_date')
    ordering_fields = ('update_time', 'create_time',)
    pagination_class = Pagination
