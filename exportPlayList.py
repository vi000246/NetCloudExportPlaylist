# -*- coding: utf-8 -*-
import json
import sys, io
from urllib.request import urlopen
import re
import requests

enterId = 'Enter the playlist url (Enter ? to get help):'
help = 'To get the id of the playlist, go to the page\ of it and look at the address bar.\ \nPlaylist id is the numbers after \ "http://music.163.com/#/playlist?id="'
errRetrive = 'No data retrived. \nPlease check the playlist id again.'

while 1:
	# 請輸入歌單的分享網址 ex.http://music.163.com/playlist?id=8575496&userid=312404996
	# 會自動將playlist的id取出來
	playlistId = input(enterId)
	urlId = re.compile(r'.*\?id=(\d+).*')
	match = urlId.match(playlistId)
	playlistId = match.group(1)
	#change the playlistId variable 
	if playlistId == '?':
		print
	urladd = "http://music.163.com/api/playlist/detail?id="+ str(playlistId)

	s = requests.session()
	# 註:如果tracks裡只有一首歌的資料，代表需要更新cookie
	# 直接連結到music.163.com或api，看能不能取到最新的cookie
	my_headers = {
		'Referer':'http://music.163.com/',
		'Cookie': 'usertrack=ezq0pFuE55Ijom0mCaC/Ag==; _ntes_nnid=33554f33ef5aee19d4830cd742d83053,1535436692565; _ntes_nuid=33554f33ef5aee19d4830cd742d83053; _ga=GA1.2.1102919721.1535436694; __remember_me=true; MUSIC_U=e24fcb11115d6d88c44093363fa1f5764a0eb4c2a057fefa258f578ae0ab23fa6d0aa0ddb1742d0d1145e241c3cac8eda95d0a65d34820fe8bafcdfe5ad2b092; __csrf=afe33f10d3a1ded7c49bf7e098b51706;',
		'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
		}
	
	res=s.get(urladd,headers = my_headers)
	data = json.loads(res.text)

	output = ""

	if "result" not in data:
		print(errRetrive)
		print(help)
		continue

	tracks = data["result"]["tracks"]
	if(len(tracks)<=1):
		print('Tracks only have one song!!!!!!!')
		continue
	for track in tracks:
		trackName = track["name"]
		artist = track["artists"][0]["name"]
		output += trackName + ' - ' + artist + '\n'
	playlistName = data["result"]["name"].replace('?',' ').replace('!','')


	with open(playlistName+'.txt', 'w',encoding='utf-8') as file:
		file.write(output)

	print('Success.\nCheck the directory of this file and find the .kgl file!')
