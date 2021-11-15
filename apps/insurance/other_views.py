import json

import requests
from rest_framework.response import Response
from rest_framework.views import APIView


class download_insurance_policy(APIView):
    def get(self, request):
        '''
        自动下载保单
        '''
        date = request.GET.get("date")
        url = 'http://82.157.144.142/getorder'
        data = {'date': date}
        r = requests.post(url, json=data)
        # print(r.text)
        json_data = json.loads(r.text)
        if json_data['status'] == 200:
            json_data['errorCode'] = 0
        return Response(json_data)
