import re

from bs4 import BeautifulSoup
from ..function.res import ResponseData

class Parser(ResponseData):
    def __init__(self):
        super().__init__()

    def soup(self, res):
        soup = BeautifulSoup(res, 'html.parser')
        return soup

    def links(self):
        res = self.resweb()
        def linked(class_card):
            h2s = class_card.find_all('h2')
            for h2 in h2s:
                a = h2.find_all('a')
                for al in a:
                    l = al.get('href')
                    return l

        soup = BeautifulSoup(res, 'html.parser')

        cards = soup.find_all(class_='view-content row')
        for card in cards:
            classes = card.find_all(class_='views-row')
            links = []
            for class_card in classes:
                link = f'https://www.ctdatacollaborative.org/{linked(class_card)}'
                links.append(link)
            return links

    def title(self, res):
        soup = BeautifulSoup(res, 'html.parser')
        title = soup.find('title').text
        return title

    def data_resource(self, res):
        def cek_ekstensi_file(string):
            pattern = r'\.pdf$|\.csv$|\.xlsx$'
            if re.search(pattern, string, re.IGNORECASE):
                return string

        soup = BeautifulSoup(res, 'html.parser')
        if soup.find(class_='data-and-resources'):
            data = soup.find(class_='data-and-resources')
            a = data.find_all('a')
            links = []
            for al in a:
                l = al.get('href')
                l = cek_ekstensi_file(l)
                if l != None:
                    links.append(l)
            return links
        else:
            links = []
            return links

    def node(self, res):
        soup = BeautifulSoup(res, 'html.parser')
        nodes = soup.find(class_='node__content clearfix').text.strip().replace('\n','')
        return nodes

    def table(self, res):
        soup = BeautifulSoup(res, 'html.parser')
        nodes = soup.find(class_='node__content clearfix')
        tables = nodes.find_all('table')
        return tables


    def tables_2(self, url):
        res = self.resweb_param(url)
        table_data = []
        for table in self.table(res):
            if table.find_next('thead'):
                thead = table.find_next('thead')
                tr = thead.find('tr')
                ths = tr.find_all('th')
                thead_data = []
                for th in ths:
                    thead_data.append(th.text)

        tbody = table.find_next('tbody')
        trs = tbody.find_all('tr')
        tbody_data = []
        for tr in trs:
            tds = tr.find_all('td')
            tds_data = []
            for td in tds:
                tds_data.append(td.text)
            tbody_data.append(tds_data)

        tbody = table.find_next('tbody')
        trs = tbody.find_all('tr')
        tbody_data_1 = []
        for tr in trs:
            tds = tr.find_all('th')
            tds_data = []
            for td in tds:
                tds_data.append(td.text)
            tbody_data_1.append(tds_data)


        for value_list, description_list in zip(tbody_data, tbody_data_1):
            for value, description in zip(value_list, description_list):
                table_data.append({'field': description, 'value': value})

        return table_data


    def tables(self, url):
        res = self.resweb_param(url)
        table_data = []
        for table in self.table(res):
            if table.find_next('caption') != None:
                caption = table.find_next('caption').text
                caption = re.sub("[\\/:\*\?\"<>\|]|[\s.]$|^[\s.].", "", caption).lower().replace(' ', '_')
                if table.find_next('thead'):
                    thead = table.find_next('thead')
                    tr = thead.find('tr')
                    ths = tr.find_all('th')
                    thead_data = []
                    for th in ths:
                        thead_data.append(th.text)

                tbody = table.find_next('tbody')
                trs = tbody.find_all('tr')
                tbody_data = []
                for tr in trs:
                    tds = tr.find_all('td')
                    tds_data = []
                    for td in tds:
                        tds_data.append(td.text)
                    tbody_data.append(tds_data)

                tbody_row = []

                for row in tbody_data:
                    data_row = []

                    if len(row) == len(thead_data):
                        for i, field in enumerate(row, start=0):
                            if thead_data[i] != '':
                                key = thead_data[i]
                                key = re.sub("[\\/:\*\?\"<>\|]|[\s.]$|^[\s.].", "", key).lower().replace(' ',
                                                                                                         '_').replace(
                                    '-', '').replace('(', '').replace(')', '')
                                item = {key: field}
                                data_row.append(item)
                            else:
                                item = {i: field}
                                data_row.append(item)

                    else:
                        for i, field in enumerate(row, start=1):
                            item = {i: field}
                            data_row.append(item)
                    tbody_row.append(data_row)
                table_data.append({caption: tbody_row})
        return table_data


