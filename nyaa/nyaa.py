import requests
import re
import time
import pathlib
import subprocess
import threading

sources = [
    {
        'file': 'subsplease.txt',
        'query': lambda q: f'https://nyaa.si/user/subsplease?f=0&c=1_2&q=1080p+-batch+("{q}")',
        'regex': re.compile(r'<tr class=\"success.+?title=\"\[SubsPlease\] (.+?) \(1080p\).+?href=\"(magnet.+?)\">.+?data-timestamp=\"(\d+?)\">.+?</tr>')
    },
    {
        'file': 'erairaws.txt',
        'query': lambda q: f'https://nyaa.si/user/Erai-raws?f=0&c=1_2&q=1080p+hevc+-batch+("{q}")',
        'regex': re.compile(r'<tr class=\"success.+?title=\"\[Erai-raws\] (.+?) \[1080p.+?href=\"(magnet.+?)\">.+?data-timestamp=\"(\d+?)\">.+?</tr>')
    },
]

with open('last_ran_on', 'r+') as f:
    last_ran_on = int(f.read())
    f.seek(0)
    f.write(str(int(time.time())))

pathlib.Path('~/Library/Application Support/uTorrent Web/resume.dat').expanduser().unlink(missing_ok=True)

def download(file, query, regex):
    with open(file, 'r') as f:
        lines = f.read().splitlines()
    url = query('"|"'.join([f'{title.strip()}' for title in lines if title]))
    html = str(requests.get(url).content)
    for title, magnet, timestamp in regex.findall(html):
        if int(timestamp) < last_ran_on:
            break
        print(title)
        subprocess.run(['open', magnet.replace('&amp;', '&')])

for s in sources:
    t = threading.Thread(target=download, args=s.values())
    t.start()
