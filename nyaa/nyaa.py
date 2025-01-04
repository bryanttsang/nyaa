import requests
import re
import time
import pathlib
import subprocess

regex = re.compile(r'<tr class=\"success.+?title=\"\[SubsPlease\] (.+?) \(1080p\).+?href=\"(magnet.+?)\">.+?data-timestamp=\"(\d+?)\">.+?</tr>')

pathlib.Path('~/Library/Application Support/uTorrent Web/resume.dat').expanduser().unlink(missing_ok=True)

with open('anime.txt', 'r') as f:
    lines = f.read().splitlines()
query = '"|"'.join([f'{title.strip()}' for title in lines if title])
url = f'https://nyaa.si/user/subsplease?f=0&c=1_2&q=1080p+-batch+("{query}")'

with open('last_ran_on', 'r+') as f:
    last_ran_on = int(f.read())
    f.seek(0)
    f.write(str(int(time.time())))

html = str(requests.get(url).content)
for title, magnet, timestamp in regex.findall(html):
    if int(timestamp) < last_ran_on:
        break
    print(title)
    subprocess.run(['open', magnet.replace('&amp;', '&')])
