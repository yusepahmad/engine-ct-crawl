import requests


headers = {
    'Referer': 'https://www.ctdatacollaborative.org/search/field_topic/global-dataset-analysis-36?page=1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
}




class ResponseData():
    def __init__(self):
        super().__init__()

    def resweb(self):
        params = {
            'page': '4',
        }

        response = requests.get(
            'https://www.ctdatacollaborative.org/search/field_topic/global-dataset-analysis-36',
            params=params,
            headers=headers,
        )
        response_text: str = response.text
        return response_text


    def resweb_param(self, link_web):
        response = requests.get(
            link_web
        )
        response_text: str = response.text
        return response_text