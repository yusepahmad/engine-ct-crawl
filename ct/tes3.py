from bs4 import BeautifulSoup
from  src.function.res import ResponseData
import json



res = ResponseData().resweb_param('https://www.state.gov/reports/2019-trafficking-in-persons-report-2/armenia/')

soup = BeautifulSoup(res, 'html.parser')

content = soup.find(class_='entry-content').text.strip().replace('\n','').replace('  ','')


metadata = {
"link": "https://www.ctdatacollaborative.org/page/index-human-trafficking-open-data-sources",
                "tag": [
                    "ctdatacollaborative",
                    "dataset"
                ],
                "domain": "ctdatacollaborative.org",
    "id":10,
    "geography":'Armenia',
    "geo":None,
    "geo_more":None,
    "file_format":'html',
    'file_flabel':'webpage',
    'link_source':'https://www.state.gov/reports/2019-trafficking-in-persons-report-2/armenia/',
    'note':'webpage',
    'link_content':content,
    'file_name':'10.json',
    'path_data_raw': 's3://ai-pipeline-statistics/data/data_raw/Divtik/INDEX OF HUMAN TRAFFICKING OPEN DATA SOURCES/json/10.json',
    'path_data_clean': 's3://ai-pipeline-statistics/data/data_raw/Divtik/INDEX OF HUMAN TRAFFICKING OPEN DATA SOURCES/json/10.json',
    "crawling_time": "2024-03-19 01:34:19",
    "crawling_time_epoch": 1710786948
}

json.dump(metadata, open('10.json', 'w'), indent=4)