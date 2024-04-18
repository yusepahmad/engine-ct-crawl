# from playwright.sync_api import Playwright, sync_playwright
#
#
# def run(playwright: Playwright) -> None:
#     csv_urls = []  # Variable list untuk menyimpan URL CSV
#
#     browser = playwright.chromium.launch(headless=True)
#     context = browser.new_context()
#     page = context.new_page()
#
#     # Fungsi untuk menyimpan URL setiap kali mendapat respons CSV
#     def store_csv_url(response):
#         response_url = response.url
#         if '.csv' in response_url:
#             csv_urls.append(response_url)
#
#     # Mendengarkan event 'response' pada semua permintaan
#     page.on("response", store_csv_url)
#
#     # Mengarahkan halaman ke URL yang diinginkan
#     page.goto("https://www.ctdatacollaborative.org/story/abducted-victims")
#
#     # ---------------------
#     context.close()
#     browser.close()
#
#     return csv_urls  # Mengembalikan list URL CSV
#
#
# with sync_playwright() as playwright:
#     csv_urls_list = run(playwright)
#
# # Cetak list URL CSV setelah menjalankan skrip
# print(len(csv_urls_list))

from src.function.hard_code import HardCode
import json
import re

class Main(HardCode):
    def __init__(self):
        super().__init__()

    def tes_table(self):
        res = self.resweb_param('https://www.ctdatacollaborative.org/story/gems2022')
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
                                key = re.sub("[\\/:\*\?\"<>\|]|[\s.]$|^[\s.].", "", key).lower().replace(' ', '_').replace('-','').replace('(','').replace(')','')
                                item = {key: field}
                                data_row.append(item)
                            else:
                                item = {i:field}
                                data_row.append(item)

                    else:
                        for i, field in enumerate(row, start=1):
                            item = {i:field}
                            data_row.append(item)
                    tbody_row.append(data_row)
                table_data.append({caption:tbody_row})
        return table_data



if __name__=="__main__":
    Main().tes_table()
