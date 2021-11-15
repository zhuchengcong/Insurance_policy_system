import requests


def download_insurance_policy(date):
    url = 'http://82.157.144.142/getorder'
    data = {'date': date}
    r = requests.post(url, json=data)
    print(r.text)


download_insurance_policy('2021-11-09')
