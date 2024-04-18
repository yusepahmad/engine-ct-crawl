from ..helper.parsing import Parser
from playwright.sync_api import sync_playwright
import requests
import os
import json
import time
from datetime import datetime
import s3fs
from loguru import logger
from dotenv import load_dotenv
load_dotenv()


sekarang = datetime.now()
format_ymd_hms = sekarang.strftime("%Y-%m-%d %H:%M:%S")

class HardCode(Parser):
    def __init__(self):
        super().__init__()

    def table_case_hard(self):
        tables = self.tables('https://www.ctdatacollaborative.org/story/gems2022')
        table_1 = tables[0].get('table_1_calculation_of_odds_ratio_from_the_parameters_of_the_logit_model')
        datas = []
        data_table1 = []
        for ii in range(2, 8):
            for i in range(2, len(table_1)):
                item = {}
                item.update({'title':'table_1_calculation_of_odds_ratio_from_the_parameters_of_the_logit_model'})
                for values in table_1[1][ii].values():
                    item.update({'category': values})
                for values in table_1[i][0].values():
                    item.update({'menu': values})
                for values in table_1[i][1].values():
                    item.update({'sub_menu': values})
                for values in table_1[i][ii].values():
                    item.update({'value':values})
                data_table1.append(item)

        # print(data_table1)


        table_2 = tables[1].get('table_2_odds_ratio_computed_for_the_global_estimates')
        data_table2 = []
        for item_2 in table_2:
            it2 = {}
            for itt2 in item_2:
                it2.update({'title':"table_2_odds_ratio_computed_for_the_global_estimates"})
                it2.update(itt2)
            data_table2.append(it2)

        # print(data_table2)

        table_3 = tables[2].get('table_3_global_estimation_of_forced_sexual_exploitation_of_adults_by_sex')
        # print(table_3)
        data_table3 = []
        for item_3 in table_3:
            it3 = {}
            for itt3 in item_3:
                it3.update({'title':"table_3_global_estimation_of_forced_sexual_exploitation_of_adults_by_sex"})
                it3.update(itt3)
            data_table3.append(it3)



        table_4 = tables[3].get('table_4_number_and_prevalence_of_persons_in_modern_slavery,_by_category,_sex,_age,_and_national_income_grouping')
        # print(table_4)
        data_table4 = []
        for iii in range(2, 16):
            for ii in range(1, 10):
                item = {}
                item.update({'title':'table_1_calculation_of_odds_ratio_from_the_parameters_of_the_logit_model'})
                for value in table_4[0][iii].values():
                     item.update({'category':value})
                for value in table_4[ii][1].values():
                    item.update(({'menu':value}))

                for value in table_4[ii][iii].values():
                    item.update({'value': value})
                data_table4.append(item)

        for data_it in data_table1:
            datas.append(data_it)

        for data_it in data_table2:
            datas.append(data_it)

        for data_it in data_table3:
            datas.append(data_it)

        for data_it in data_table4:
            datas.append(data_it)


        return datas


    def times(self, metadata):
        metadata.update({"crawling_time": format_ymd_hms, "crawling_time_epoch": int(time.time())})


    def play_crawl(self, url):
         with sync_playwright() as p:
             csv_urls = []
             browser = p.chromium.launch(headless=False)
             context = browser.new_context()
             page = context.new_page()
             content = page.query_selector('body').text_content().strip().replace('\n','').replace('\t','').replace('  ','')
             page.goto(url)

             # ---------------------
             context.close()
             browser.close()
             return content


    def crawl_url(self, url):
         with sync_playwright() as p:
             csv_urls = []
             browser = p.firefox.launch(headless=True)
             context = browser.new_context()
             page = context.new_page()
             def store_csv_url(response):
                 response_url = response.url
                 if '.csv' in response_url:
                     csv_urls.append(response_url)
             page.on("response", store_csv_url)
             page.goto(url)

             # ---------------------
             context.close()
             browser.close()

             return csv_urls

    def table_check(self, link):
        data = {}
        res = self.resweb_param(link)
        tab = self.table(res)
        if tab:
            tables = self.tables_2(link)
            data1 = {'table': tables}
            data.update(data1)
        else:
            data2 = {'table':[]}
            data.update(data2)
            print('tidak ada')
        return data

    def download_formated(self):
        for link in self.links():
            res = self.resweb_param(link)
            files = self.data_resource(res)
            datas = self.crawl_url(link)
            metadata = {
                "link": "https://www.ctdatacollaborative.org/search/field_topic/global-dataset-analysis-36",
                "tag": [
                    "ctdatacollaborative",
                    "dataset"
                ],
                "domain": "ctdatacollaborative.org",
                'title': self.title(res),
                'content': self.node(res),
            }
            data_item = []
            for data in datas:
                import pandas as pd
                import re
                file_csv = data
                field = re.sub("[\\/:\*\?\"<>\|]|[\s.]$|^[\s.].","", str(file_csv.split('%20')[0].split('/')[-1].lower().replace('.','').replace('-','_')))
                df = pd.read_csv(file_csv)
                json_output = df.to_dict(orient='records')

                for item in json_output:
                    items = {}
                    items.update({'title': field})
                    for key in item:
                        value = item[key]
                        if value == None:
                            value = ""
                        value = str(value)
                        key = re.sub("[\\/:\*\?\"<>\|]|[\s.]$|^[\s.].", "", key).lower().replace(' ', '')
                        items.update({key: value})
                    data_item.append(items)

            metadata.update({'chart':data_item})
            print(data_item)

            table = self.table_check(link)
            metadata.update(table)
            file_name_json = f"{self.title(res)}"
            file_name_json = file_name_json.replace('/', '').replace(' ', '_').replace('.', '').replace('|','').replace(':','')
            file_name_json = file_name_json.lower()
            file_name_json = f'{file_name_json}.json'
            file_name_json = f'{file_name_json}'

            path_data_raw = [f's3://ai-pipeline-statistics/data/data_raw/Divtik/Global Dataset Victim/json/{file_name_json}']
            path_data_clean = [f's3://ai-pipeline-statistics/data/data_raw/Divtik/Global Dataset Victim/josn/{file_name_json}']
            file_names = [file_name_json]

            for files_download in files:
                url_download = f'https://www.ctdatacollaborative.org{files_download}'
                file_name = files_download.split('/')[-1]
                format = file_name.split('.')[-1]

                file_path = f's3://ai-pipeline-statistics/data/data_raw/Divtik/Global Dataset Victim/{format}/{file_name}'
                file_path_clean = f's3://ai-pipeline-statistics/data/data_clean/Divtik/Global Dataset Victim/{format}/{file_name}'

                path_data_raw.append(file_path)
                path_data_clean.append(file_path_clean)
                file_names.append(file_name)

                self.download_send_s3(url_download, file_path)

            metadata.update({'file_name':file_names})
            metadata.update({'path_data_raw':path_data_raw})
            metadata.update({'path_data_clean':path_data_clean})
            metadata.update({"crawling_time": format_ymd_hms,"crawling_time_epoch": int(time.time())})


            self.send_json_s3_v2(metadata, f's3://ai-pipeline-statistics/data/data_raw/Divtik/Global Dataset Victim/json/{file_name_json}', file_name_json)
            json.dump(metadata, open(f'example/json/satu/{file_name_json}', 'w'), indent=4)
            print('success save data ', file_name_json)


    def download_formated2(self):
            link = 'https://www.ctdatacollaborative.org/story/gems2022'
            res = self.resweb_param(link)
            files = self.data_resource(res)
            datas_csv = self.crawl_url(link)
            metadata = {
                "link": "https://www.ctdatacollaborative.org/search/field_topic/global-dataset-analysis-36",
                "tag": [
                    "ctdatacollaborative",
                    "dataset"
                ],
                "domain": "ctdatacollaborative.org",
                'title': self.title(res),
                'content': self.node(res),
            }
            data_item = []
            for data in datas_csv:
                import pandas as pd
                import re
                file_csv = data
                field = re.sub("[\\/:\*\?\"<>\|]|[\s.]$|^[\s.].","", str(file_csv.split('%20')[0].split('/')[-1].lower().replace('.','').replace('-','_')))
                df = pd.read_csv(file_csv)
                json_output = df.to_dict(orient='records')
                for item in json_output:
                    items = {}
                    items.update({'title': field})
                    for key in item:
                        value = item[key]
                        if value == None:
                            value = ""
                        value = str(value)
                        key = re.sub("[\\/:\*\?\"<>\|]|[\s.]$|^[\s.].", "", key).lower().replace(' ', '')
                        items.update({key: value})
                    data_item.append(items)

            metadata.update({'chart': data_item})
            print(data_item)

            data_tabb = self.table_case_hard()
            table = {'table':data_tabb}
            metadata.update(table)
            file_name_json = f"{self.title(res)}"
            file_name_json = file_name_json.replace('/', '').replace(' ', '_').replace('.', '').replace('|','').replace(':','')
            file_name_json = file_name_json.lower()
            file_name_json = f'{file_name_json}.json'
            file_name_json = f'{file_name_json}'

            path_data_raw = [f's3://ai-pipeline-statistics/data/data_raw/Divtik/Global Dataset Victim/json/{file_name_json}']
            path_data_clean = [f's3://ai-pipeline-statistics/data/data_raw/Divtik/Global Dataset Victim/josn/{file_name_json}']
            file_names = [file_name_json]

            for files_download in files:
                url_download = f'https://www.ctdatacollaborative.org{files_download}'
                file_name = files_download.split('/')[-1]
                format = file_name.split('.')[-1]

                file_path = f's3://ai-pipeline-statistics/data/data_raw/Divtik/Global Dataset Victim/{format}/{file_name}'
                file_path_clean = f's3://ai-pipeline-statistics/data/data_clean/Divtik/Global Dataset Victim/{format}/{file_name}'

                path_data_raw.append(file_path)
                path_data_clean.append(file_path_clean)
                file_names.append(file_name)

                self.download_send_s3(url_download, file_path)

            metadata.update({'file_name':file_names})
            metadata.update({'path_data_raw':path_data_raw})
            metadata.update({'path_data_clean':path_data_clean})
            metadata.update({"crawling_time": format_ymd_hms,"crawling_time_epoch": int(time.time())})

            # print(metadata)
            self.send_json_s3_v2(metadata, f's3://ai-pipeline-statistics/data/data_raw/Divtik/Global Dataset Victim/json/{file_name_json}', file_name_json)
            json.dump(metadata, open(f'example/json/satu/{file_name_json}', 'w'), indent=4)
            # print('success save data ', file_name_json)



    def index_human(self):
            link = 'https://www.ctdatacollaborative.org/page/index-human-trafficking-open-data-sources'
            res = self.resweb_param(link)
            files = self.data_resource(res)
            datas_csv = self.crawl_url(link)
            metadata = {
                "link": "https://www.ctdatacollaborative.org/page/index-human-trafficking-open-data-sources",
                "tag": [
                    "ctdatacollaborative",
                    "dataset"
                ],
                "domain": "ctdatacollaborative.org",
                'title': self.title(res),
                'content': self.node(res),
            }
            data_item = []
            for data in datas_csv:
                import pandas as pd
                import re
                file_csv = data
                field = re.sub("[\\/:\*\?\"<>\|]|[\s.]$|^[\s.].","", str(file_csv.split('%20')[0].split('/')[-1].lower().replace('.','').replace('-','_')))
                df = pd.read_csv(file_csv)
                json_output = df.to_dict(orient='records')
                for item in json_output:
                    items = {}
                    items.update({'title': field})
                    for key in item:
                        value = item[key]
                        if value == None:
                            value = ""
                        value = str(value)
                        key = re.sub("[\\/:\*\?\"<>\|]|[\s.]$|^[\s.].", "", key).lower().replace(' ', '')
                        items.update({key: value})
                    data_item.append(items)

            metadata.update({'chart': data_item})
            print(data_item)

            data_tabb = self.table_check(link)
            metadata.update(data_tabb)
            file_name_json = f"{self.title(res)}"
            file_name_json = file_name_json.replace('/', '').replace(' ', '_').replace('.', '').replace('|','').replace(':','')
            file_name_json = file_name_json.lower()
            file_name_json = f'{file_name_json}.json'
            file_name_json = f'{file_name_json}'

            path_data_raw = [f's3://ai-pipeline-statistics/data/data_raw/Divtik/INDEX OF HUMAN TRAFFICKING OPEN DATA SOURCES/json/{file_name_json}']
            path_data_clean = [f's3://ai-pipeline-statistics/data/data_raw/Divtik/INDEX OF HUMAN TRAFFICKING OPEN DATA SOURCES/josn/{file_name_json}']
            file_names = [file_name_json]

            for files_download in files:
                url_download = f'https://www.ctdatacollaborative.org{files_download}'
                file_name = files_download.split('/')[-1]
                format = file_name.split('.')[-1]

                file_path = f's3://ai-pipeline-statistics/data/data_raw/Divtik/INDEX OF HUMAN TRAFFICKING OPEN DATA SOURCES/{format}/{file_name}'
                file_path_clean = f's3://ai-pipeline-statistics/data/data_clean/Divtik/INDEX OF HUMAN TRAFFICKING OPEN DATA SOURCES/{format}/{file_name}'

                path_data_raw.append(file_path)
                path_data_clean.append(file_path_clean)
                file_names.append(file_name)

                self.download_send_s3(url_download, file_path)

            metadata.update({'file_name':file_names})
            metadata.update({'path_data_raw':path_data_raw})
            metadata.update({'path_data_clean':path_data_clean})
            metadata.update({"crawling_time": format_ymd_hms,"crawling_time_epoch": int(time.time())})

            # print(metadata)
            self.send_json_s3_v2(metadata, f's3://ai-pipeline-statistics/data/data_raw/Divtik/INDEX OF HUMAN TRAFFICKING OPEN DATA SOURCES/json/{file_name_json}', file_name_json)
            json.dump(metadata, open(f'example/json/satu/{file_name_json}', 'w'), indent=4)
            # print('success save data ', file_name_json)


    def download_send_s3(self, link, path):
        response = requests.get(link)
        file_name = link.split('/')[-1]
        client_kwargs = {
            'key': os.getenv('KEY'),
            'secret': os.getenv('SECRET_KEY'),
            'endpoint_url': os.getenv('ENDPOINT_URL'),
            'anon': False
        }

        s3 = s3fs.core.S3FileSystem(**client_kwargs)
        download_s3 = path
        if response.status_code == 200:
            try:
                with s3.open(os.path.join(download_s3), "wb") as file:
                    file.write(response.content)
                logger.success(f"File successfully saved in {download_s3}.")
            except Exception as e:
                logger.error(f'Gagal menyimpan file {file_name} di {download_s3}: {e}')
        else:
            logger.error(f"Failed to download file. Status Code: {response.status_code}")

    def send_json_s3_v2(self, metadata, path_data_raw, file_name_json):
        client_kwargs = {
            'key': os.getenv('KEY'),
            'secret': os.getenv('SECRET_KEY'),
            'endpoint_url': os.getenv('ENDPOINT_URL'),
            'anon': False
        }

        s3 = s3fs.core.S3FileSystem(**client_kwargs)
        json_s3 = str(path_data_raw)
        json_data = json.dumps(metadata, indent=4, ensure_ascii=False)
        try:
            with s3.open(json_s3, 'w') as s3_file:
                s3_file.write(json_data)
            logger.success(f'File {file_name_json} berhasil diupload ke S3.')
        except Exception as e:
            logger.error(f'Gagal mengunggah file {file_name_json} ke S3: {e}')



    def download_files(self, url, raw, clean, files_name):
        data = []
        file_name = url.split('/')[-1]
        format = file_name.split('.')[-1]

        file_path = f's3://ai-pipeline-statistics/data/data_raw/Divtik/INDEX OF HUMAN TRAFFICKING OPEN DATA SOURCES/{format}/{file_name}'
        file_path_clean = f's3://ai-pipeline-statistics/data/data_clean/Divtik/INDEX OF HUMAN TRAFFICKING OPEN DATA SOURCES/{format}/{file_name}'


        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        response = requests.get(url, headers=headers, verify=False)

        if response.status_code == 200:
            os.makedirs('example/download/dua', exist_ok=True)
            with open(os.path.join('example/download/dua', url.split('/')[-1]), "wb") as file:
                file.write(response.content)
            raw.append(file_path)
            clean.append(file_path_clean)
            files_name.append(file_name)
            data.append(file_path)
            data.append(file_path_clean)
            data.append(file_name)
            print(f"File {url.split('/')[-1]} successfully saved in {file_name}.")
        else:
            print(f"Failed to download file. Status Code: {response.status_code}")
        return data


    def download_files_part2(self, url, raw, clean, files_name, format):
        client_kwargs = {
            'key': os.getenv('KEY'),
            'secret': os.getenv('SECRET_KEY'),
            'endpoint_url': os.getenv('ENDPOINT_URL'),
            'anon': False
        }

        s3 = s3fs.core.S3FileSystem(**client_kwargs)
        data = []
        if format != 'html':
            file_name = url.split('/')[-1]
            if format in file_name:
                file_name = file_name
            else:
                file_name = f'{file_name}.{format}'

            file_path = f's3://ai-pipeline-statistics/data/data_raw/Divtik/INDEX OF HUMAN TRAFFICKING OPEN DATA SOURCES/{format}/{file_name}'
            file_path_clean = f's3://ai-pipeline-statistics/data/data_clean/Divtik/INDEX OF HUMAN TRAFFICKING OPEN DATA SOURCES/{format}/{file_name}'


            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
            response = requests.get(url, headers=headers, verify=False)

            if response.status_code == 200:
                with s3.open(os.path.join(file_path), "wb") as file:
                    file.write(response.content)
                logger.success(f"File successfully saved in {file_path}.")
                raw.append(file_path)
                clean.append(file_path_clean)
                files_name.append(file_name)
                data.append(file_path)
                data.append(file_path_clean)
                data.append(file_name)
            else:
                print(f"Failed to download file. Status Code: {response.status_code}")
        return data