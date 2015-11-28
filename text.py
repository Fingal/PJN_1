__author__ = 'Fingal'
import re
import pprint
text=open('text','r',encoding='utf-8').read()
text=re.sub(r'<div.*?>','',text)
codes=re.findall(r'<pre><code>(.*?)</code></pre>',text,flags=re.S)
text=re.sub(r'<pre><code>(.*?)</code></pre>',' ',text,flags=re.S)
#pprint.pprint(codes)
text=re.sub(r'(<.*?>)',' ',text)
#print(text)
print(len(codes),sum([len(code.split('\n')) for code in codes]),len(text.split('\n')))