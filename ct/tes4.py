import pandas as pd
import re
import json
from bs4 import BeautifulSoup
from src.function.hard_code import HardCode
import requests


class Main(HardCode):
    def __init__(self):
        super().__init__()

    def path(self, metadata):
        path_data_raw = [
            f's3://ai-pipeline-statistics/data/data_raw/Divtik/INDEX OF HUMAN TRAFFICKING OPEN DATA SOURCES/json/{metadata.get("id")}.json']
        path_data_clean = [
            f's3://ai-pipeline-statistics/data/data_raw/Divtik/INDEX OF HUMAN TRAFFICKING OPEN DATA SOURCES/josn/{metadata.get("id")}.json']
        file_names = [f'{metadata.get("id")}.json']

        metadata.update({'path_data_raw': path_data_raw, 'path_data_clean': path_data_clean, 'file_name': file_names})

    def tes(self):

        url_html = []
        df = pd.read_excel('publicHTdata_v0_1.xlsx')
        json_output = df.to_dict(orient='records')
        links = []
        for item in json_output:
            metadata = {
                "link": "https://www.ctdatacollaborative.org/page/index-human-trafficking-open-data-sources",
                "tag": [
                    "ctdatacollaborative",
                    "dataset"
                ],
                "domain": "ctdatacollaborative.org",
            }
            for key in item:
                value = item[key]
                value = str(value)
                if value == 'nan':
                    value = None
                key = re.sub("[\\/:\*\?\"<>\|]|[\s.]$|^[\s.].", "", key).lower().replace(' ', '').replace('(','').replace(')','')
                if key == 'link':
                    key = 'link_source'
                metadata.update({key: value})
            format = metadata.get('fileformat')
            url_link = metadata.get('link_source')
            if 'html' in format :
                if 'www.police.gov.bd' in url_link:
                    pass
                else:
                    url_html.append(url_link)
                    if 'https://www.state.gov/' in url_link:
                        link_content = []
                        res = self.resweb_param(url_link)
                        soup =  self.soup(res)
                        container = soup.find(class_='wp-block-report-content report row')
                        content_data = container.find_all(class_='report__content__inner entry-content')
                        for content in content_data:
                            title = content.find_next(class_='report__section-title').text.strip().replace('\n','').replace('\t','').replace('  ','')
                            data = content.find_next('p').text
                            link_content.append({'title':title, 'content':data})
                        metadata.update({'link_content':link_content})
                        self.path(metadata)
                    elif 'ec.europa.eu' in url_link:
                        metadata.update({'link_content': [self.europa()]})
                        self.path(metadata)

                    else:
                        res = self.resweb_param(url_link)
                        metadata.update({'link_content': [self.all_content(res)]})
                        self.path(metadata)
            else:
                link_content = []
                metadata.update({'link_content': link_content})
                path_data_raw = [f's3://ai-pipeline-statistics/data/data_raw/Divtik/INDEX OF HUMAN TRAFFICKING OPEN DATA SOURCES/json/{metadata.get("id")}.json']
                path_data_clean = [f's3://ai-pipeline-statistics/data/data_raw/Divtik/INDEX OF HUMAN TRAFFICKING OPEN DATA SOURCES/josn/{metadata.get("id")}.json']
                file_names = [f'{metadata.get("id")}.json']


                try:
                    if format == 'html':
                        pass
                    if format == 'htm':
                        pass
                    if 'https://www.myria.be/en/publications/' in url_link:
                        res = self.resweb_param(url_link)
                        soup = self.soup(res)
                        do = soup.find(class_='download')
                        href = do.get_attribute('href')
                        href = f'https://www.myria.be{href}'
                        self.download_files_part2(href, path_data_raw, path_data_clean, file_names, format)
                    elif 'https://mb.gov.al/annual-report-2015/' == url_link:
                        res = self.resweb_param(url_link)
                        soup = self.soup(res)
                        do = soup.find(class_='pageDescription')
                        href = do.get_attribute('href')
                        href = f'https://mb.gov.al/{href}'
                        self.download_files_part2(href, path_data_raw, path_data_clean, file_names, format)
                    else:
                        self.download_files_part2(url_link, path_data_raw, path_data_clean, file_names, format)
                except:
                    ...
                metadata.update({'path_data_raw': path_data_raw, 'path_data_clean': path_data_clean, 'file_name': file_names})

            self.times(metadata)
            self.send_json_s3_v2(metadata, f's3://ai-pipeline-statistics/data/data_raw/Divtik/INDEX OF HUMAN TRAFFICKING OPEN DATA SOURCES/json/{metadata.get("id")}.json', f'{metadata.get("id")}.json')



    def europa(self):
        link_content = [
            {
                'title': 'Together Against Trafficking in Human Beings',
                'content': "Trafficking in human beings is a crime that should have no place in today’s society. It destroys individuals’ lives by depriving people of their dignity, freedom and fundamental rights. It is often a violent crime committed by organised crime networks.",
            },
            {
                'title': "Facts about trafficking in human beings",
                'content': "37% of the victims of trafficking in the EU are EU citizens, and a significant number of them are trafficked within their own country. However, non-EU victims have increased in recent years and they now outnumber victims with an EU citizenship. The majority of victims in the EU are women and girls who are mainly trafficked for sexual exploitation. The ratio of male victims has more than doubled in the last years.Around 15% of victims of trafficking in the EU are children.The most common forms of trafficking in the EU is sexual exploitation and labour exploitation. Both forms of exploitation amount to an equal share of victims. Most traffickers in the EU are EU citizens and often of the same nationality as their victims. More than three quarters of perpetrators are men."
            },
            {
                'title': "Links with organised crime",
                'content': "This crime brings high profits to criminals and carries with it enormous human, social and economic costs. Trafficking in human beings is often linked with other forms of organised crime such as migrant smuggling, drug trafficking, extortion, money laundering, document fraud, payment card fraud, property crimes, cybercrime and other.This complex criminal phenomenon continues to be systematically addressed in a wide range of EU policy areas and initiatives from security to migration, justice, equality, fundamental rights, research, development and cooperation, external action and employment to name a few."
            }
        ]
        return link_content

    def all_content(self, res):
        soup = self.soup(res)

        title = soup.find('title').text
        content = soup.find('body').text.strip().replace('\n','').replace('  ','').replace('\t','')

        link_content = {
            'title': title,
            'content': content
        }
        return link_content

if __name__=="__main__":
    Main().tes()
