#!/usr/bin/python
import os
import urllib2
if __name__ == '__main__':
	if not os.path.isdir('manga-down') :
		os.mkdir('manga-down')
	print 'download start!'
	req = urllib2.Request('http://fufufuu02.imgur.com/')
	r = urllib2.urlopen(req)
	source = r.read()
	items = []
	cnt = 0
	max = source.count('<div id="album-')
	while source.find('<div id="album-') != -1 :
		source = source[source.find('<div id="album-')+len('<div id="album-'):]
		item_url = source[0:source.find('"')]
		source = source[source.find('data-title="')+len('data-title="'):]
		item_title = source[0:source.find('"')]
		item_title = item_title.replace('/', '-').replace('\\', '-')+'.zip'
		
		req = urllib2.Request('http://s.imgur.com/a/'+item_url+'/zip')
		r = urllib2.urlopen(req)
		
		output = open('manga-down/'+item_title,'wb')
		output.write(r.read())
		output.close()
		cnt += 1
		print '"'+item_title+'" download complete. [%d/%d]' % (cnt, max)
	print 'done!'
