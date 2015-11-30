__author__ = 'Fingal'
import re
import pprint


def text_counter(text):
    text = re.sub(r'<div.*?>', '', text)
    paragraphs = re.findall(r'<p>(.*?)</p>', text, flags=re.S)
    codes = re.findall(r'<pre><code>(.*?)</code></pre>', text, flags=re.S)
    text = re.sub(r'<pre><code>(.*?)</code></pre>', ' ', text, flags=re.S)
    # pprint.pprint(codes)
    text = re.sub(r'(<.*?>)', ' ', text)
    # print(text)
    return {'words': len(text.split()), 'code_lines': sum([len(code.split('\n')) for code in codes]),
            'codes': len(codes), 'paragraphs': len(paragraphs)}
