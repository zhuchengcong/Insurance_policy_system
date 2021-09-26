from django.db.models import Q
from django_filters import rest_framework
from rest_framework.filters import BaseFilterBackend
from rest_framework.compat import coreapi, coreschema, distinct


class InsurancePolicyDateFilterBackend(BaseFilterBackend):
    """
    Filter that only allows users to see their own objects.
    """

    def filter_queryset(self, request, queryset, view):
        # print('''request.query_params.get('startTime')''')
        # print(request.query_params.get('startTime'))
        # print(request.query_params.get('endTime'))
        startTime = '2000-01-01 00:00:00'
        endTime = '2099-01-01 00:00:00'

        InsruanceStartDate = '2000-01-01 00:00:00'
        InsruanceEndDate = '2099-01-01 00:00:00'

        is_no_chanel = None
        if request.query_params.get('is_no_chanel') is not None:
            is_no_chanel = request.query_params.get('is_no_chanel')
        if is_no_chanel is not None:
            print(is_no_chanel == 'true')
            if is_no_chanel == 'true':
                queryset = queryset.filter(chanel_rate_id=None)

        if request.query_params.get('startTime') is not None:
            startTime = request.query_params.get('startTime')
        if request.query_params.get('endTime') is not None:
            endTime = request.query_params.get('endTime')

        if request.query_params.get('InsruanceStartDate') is not None:
            InsruanceStartDate = request.query_params.get('InsruanceStartDate')
        if request.query_params.get('InsruanceEndDate') is not None:
            InsruanceEndDate = request.query_params.get('InsruanceEndDate')

        # print(startTime)
        # print(endTime)
        # print(InsruanceStartDate)
        # print(InsruanceEndDate)
        if request.query_params.get('InsruanceStartDate') is not None and request.query_params.get(
                'InsruanceEndDate') is not None:
            return queryset.filter(Q(
                Q(deleted=None, generation_date__gte=startTime, generation_date__lte=endTime,
                  jiaoqiang_insurance_start_date__gte=InsruanceStartDate,
                  jiaoqiang_insurance_start_date__lte=InsruanceEndDate,
                  ) | Q(commercial_insurance_start_date=None)
            ) |
                                   Q(
                                       Q(
                                           commercial_insurance_start_date__gte=InsruanceStartDate,
                                           commercial_insurance_start_date__lte=InsruanceEndDate)
                                   ) | Q(jiaoqiang_insurance_start_date=None)
                                   ).exclude(
                jiaoqiang_insurance_start_date__gte=InsruanceEndDate,
                commercial_insurance_start_date__gte=InsruanceEndDate
            )
        else:
            return queryset.filter(deleted=None, generation_date__gte=startTime, generation_date__lte=endTime, )

    def get_schema_fields(self, view):
        assert coreapi is not None, 'coreapi must be installed to use `get_schema_fields()`'
        assert coreschema is not None, 'coreschema must be installed to use `get_schema_fields()`'
        return [
            coreapi.Field(
                name='startTime',
                required=False,
                location='query',
                schema=coreschema.String(
                    title='force_str(self.search_title)',
                    description='开始时间'
                )
            ),
            coreapi.Field(
                name='endTime',
                required=False,
                location='query',
                schema=coreschema.String(
                    title='force_str(self.search_title)',
                    description='结束时间'
                )
            ),
            coreapi.Field(
                name='InsruanceStartDate',
                required=False,
                location='query',
                schema=coreschema.String(
                    title='force_str(self.search_title)',
                    description='起保时间'
                )
            ),
            coreapi.Field(
                name='InsruanceEndDate',
                required=False,
                location='query',
                schema=coreschema.String(
                    title='force_str(self.search_title)',
                    description='结保时间'
                )
            )
        ]

    def get_schema_operation_parameters(self, view):
        return [
            {
                'name': 'startTime',
                'required': False,
                'in': 'query',
                'description': '开始时间',
                'schema': {
                    'type': 'string',
                },
            },
            {
                'name': 'endTime',
                'required': False,
                'in': 'query',
                'description': '结束时间',
                'schema': {
                    'type': 'string',
                },
            },
            {
                'name': 'InsruanceStartDate',
                'required': False,
                'in': 'query',
                'description': '起保时间',
                'schema': {
                    'type': 'string',
                },
            },
            {
                'name': 'InsruanceEndDate',
                'required': False,
                'in': 'query',
                'description': '结保时间',
                'schema': {
                    'type': 'string',
                },
            }
        ]


class DoctorsFilter(rest_framework.FilterSet):
    # 交强险 起保 日期范围
    JiaoQiangDate = rest_framework.DateFromToRangeFilter(field_name='jiaoqiang_insurance_start_date',
                                                         lookup_expr='gte', label='交强险起保日期范围')

    # 商业险 起保 日期范围
    CommercialDate = rest_framework.DateFromToRangeFilter(field_name='commercial_insurance_start_date',
                                                          lookup_expr='gte', label='商业险起保日期范围')
