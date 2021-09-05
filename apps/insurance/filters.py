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
        if request.query_params.get('startTime') is not None:
            startTime = request.query_params.get('startTime')
        if request.query_params.get('endTime') is not None:
            endTime = request.query_params.get('endTime')
        return queryset.filter(deleted=None, generation_date__gte=startTime, generation_date__lte=endTime)

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
            }
        ]
