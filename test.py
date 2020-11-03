import requests
import json

# Timezones
# https://stackoverflow.com/questions/13866926/is-there-a-list-of-pytz-timezones

url = 'http://127.0.0.1:8080'
url_with_tz = url + '/Europe/Moscow'
print(requests.get(url).text)
print(requests.get(url_with_tz).text)
print('split("\\n")[1] - ' + requests.get(url_with_tz).text.split('\n')[1])
print('mistake in timezone - ' + requests.get(url_with_tz + ' ').text)
print()


data = {'tz_start': 'Europe/Moscow', 'type': 'date'}
print('post, date -\t\t' + requests.post(url=url, data=json.dumps(data)).text)

data = {'tz_start': 'Asia/Tomsk', 'type': 'time'}
print('post, time -\t\t' + requests.post(url=url, data=json.dumps(data)).text)

data = {'type': 'time'}
print('post, time, no tz -\t' + requests.post(url=url, data=json.dumps(data)).text)


print()
data = {'tz_start': 'Asia/Tomsk', 'type': 'time'}
print('not json date - ' + requests.post(url=url, data=data).text)

data = {'tz_start': 'Asia/Tomsk'}
print('no "type" in params - ' + requests.post(url=url, data=json.dumps(data)).text)

data = {'tz_start': 'Asia/Tomsk', 'type': 'tim'}
print('mistake in "type" - ' + requests.post(url=url, data=json.dumps(data)).text)

data = {'tz_start': 'Asia/Toms', 'type': 'time'}
print('mistake in timezones - ' + requests.post(url=url, data=json.dumps(data)).text)
print()


data = {'tz_start': 'Asia/Tomsk', 'tz_end': 'Europe/Moscow', 'type': 'datediff'}
print('post, diff_1 -\t\t\t' + requests.post(url=url, data=json.dumps(data)).text)

data = {'tz_start': 'Europe/Moscow', 'tz_end': 'Asia/Tomsk', 'type': 'datediff'}
print('post, diff_2 -\t\t\t' + requests.post(url=url, data=json.dumps(data)).text)

data = {'tz_start': 'Etc/GMT-14', 'tz_end': 'Etc/GMT+12', 'type': 'datediff'}
print('+26 hours exp -\t\t\t' + requests.post(url=url, data=json.dumps(data)).text)
# +26 hours

data = {'tz_start': 'Etc/GMT+12', 'tz_end': 'Etc/GMT-14', 'type': 'datediff'}
print('-26 hours exp -\t\t\t' + requests.post(url=url, data=json.dumps(data)).text)
# -26 hours

data = {'tz_start': 'Europe/Moscow', 'tz_end': 'Europe/Moscow', 'type': 'datediff'}
print('two similar arguments -\t' + requests.post(url=url, data=json.dumps(data)).text)

data = {'type': 'datediff'}
print('without params- \t\t' + requests.post(url=url, data=json.dumps(data)).text)

data = {'tz_start': 'Europe/Moscow', 'type': 'datediff'}
print('one param tz_start -\t' + requests.post(url=url, data=json.dumps(data)).text)

data = {'tz_end': 'Europe/Moscow', 'type': 'datediff'}
print('one param tz_end -\t\t' + requests.post(url=url, data=json.dumps(data)).text)


