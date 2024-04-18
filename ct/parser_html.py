import pandas as pd

df = pd.read_excel('publicHTdata_v0_1.xlsx')

json_data = df.to_dict(orient='records')

# print(df.columns)

non_html = []
html = []
for data in json_data:
    link_down = data.get('Link')
    format  = data.get('File format')
    if format != 'html' and format != 'hml':
        non_html.append(link_down)
    else:
        html.append(link_down)


state = []
europa = []
indan = []
abstrack = []

for source in html:
    domain = source.split('/')[2]
    if 'state' in domain:
        state.append(source)
    elif 'ec.europa.eu' in domain:
        europa.append(source)
    elif 'insanalveri' in domain:
        indan.append(source)
    else:
        abstrack.append(source)

print(indan)
