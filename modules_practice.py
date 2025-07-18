import datetime
import os
import json
from collections import Counter

now_date = datetime.datetime.now()

files = os.listdir('.')

zxc = {'name': 'Quiet', 'age': 18, 'adult': True, 'languages': ['Russian', 'English']}
json_str = json.dumps(zxc, ensure_ascii=False)
with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(zxc, f, ensure_ascii=False, indent=4)

json_str_py = json.loads(json_str)
with open('data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

qwe = "Quiet good"

c = Counter(qwe)

print(now_date)
print(files)

print(json_str, type(json_str))
print(json_str_py, type(json_str_py))
print(data, type(data))
print(c)