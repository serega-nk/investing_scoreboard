import http.client
import json


def get_data(pair_id, index):
    uri = "/instruments/sentiments/recentsentimentsAjax"
    body = "action=get_sentiments_rows&sentiments_category=pairs&pair_ID={}&sentimentsBulkCount={}".format(pair_id, index)
    headers = {
        'Host': 'ru.investing.com',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Origin': 'https://ru.investing.com',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept-Encoding': 'deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
    }

    conn = http.client.HTTPSConnection('ru.investing.com')
    conn.request('POST', uri, body, headers)
    print('GET', '{}?{}'.format(uri, body))
    response = conn.getresponse()
    text = response.read().decode('utf8')
    conn.close()

    res = json.loads(text)
    keys = ('start_date', 'user_id', 'username', 'iconType', 'open', 'end_date',)
    res = [[item[key] for key in keys] for item in res['rowsData']]

    return res


def create_csv(pair_id):
    max_page = 10

    res = []
    for i in range(max_page):
        data = get_data(pair_id, i)
        if not len(data): break
        print(i, len(data))
        res += data

    for i in res:
        i[5], _, i6 = i[5].partition(' @ ')
        i.append(i6)

    keys = ['start_date', 'user_id', 'username', 'type', 'open', 'end_date', 'close']
    iterable = [keys,] + res

    fn = 'out_{}.csv'.format(pair_id)
    with open(fn, 'wb') as f_out:
        for row in iterable:
            line = ';'.join(row) + '\n'
            b = line.encode("cp1251", "replace")
            f_out.write(b)


import argparse

parser = argparse.ArgumentParser()
parser.add_argument('pair_id', metavar='pair_id', type=int, help='pair_id')

args = parser.parse_args()
if args.pair_id:
    # Прогнозы - MGNT, pair_id = 13693
    create_csv(args.pair_id)
