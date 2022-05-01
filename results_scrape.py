import requests
import pandas as pd

df = pd.DataFrame()
columns=[]
is_first_iter = True

htno_start = int(input('Starting HallTicket No. : '))
htno_end = int(input('Ending HallTicket No. : '))
for htno in range(htno_start, htno_end+1):
    # get the url and referer url by sending a sample request to the site via browser
    # -> F12 -> Network -> Request Headers
    url= r'http://results/page/link.aspx?htno=0'+str(htno)
    referer = r'http://referer/url.htm'

    resp = requests.get(url, headers={'referer': referer})
    if resp.content:
        data = pd.read_html(resp.content)
        dictionary = dict()
        each = [data[0].dropna(how='all').to_dict('split'), data[1].dropna(how='all').to_dict('split')]
        if is_first_iter:
            is_first_iter = False
            columns.extend([i[0] for i in each[0]['data']])
            for i in each[1]['data'][1:]:
                if each[1]['data'].index(i) != 2:
                    columns.extend([i[1] + ' ' + each[1]['data'][0][k] for k in [3 , 4]])
                else:
                    columns.extend(['commonsubject ' + each[1]['data'][0][k] for k in [3 , 4]])
            print(columns)
            df = df.reindex(columns= df.columns.tolist() + columns)
            df.to_csv('consolidated_result.csv', mode='w', index=False)
        for i in each[0]['data']:
            dictionary[i[0]] = i[1]
        for i in each[1]['data'][1:]:
            if each[1]['data'].index(i) != 2:
                for j in range(3,5):
                    dictionary[i[1] + ' ' + each[1]['data'][0][j]] = i[j]
            else:
                for j in range(3,5):
                    dictionary['commonsubject ' + each[1]['data'][0][j]] = i[j]
        df= df.append(dictionary, ignore_index=True)
    print(htno, ' done')
df.to_csv('test.csv', mode='a', index=False, header=False)
