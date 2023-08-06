import re
import jieba
from bs4 import BeautifulSoup

def calc_word(root, depth_weight=0.5, stoptag='body', lang='zh'):
    if isinstance(root, str):
        return None
    
    def filter_node(tag):
        ign = ['script', 'style', 'head']
        if tag.name.lower() in ign:
            return False
        return True
    nodes = root.find_all(name=filter_node, text=re.compile(r'^[^\s]*$'))

    def soup_depth_count(el, stoptag='body'):
        if isinstance(el, str):
            return -1
        prt = el.parent
        count = 0
        while prt and prt.name != stoptag:
            count += 1
            prt = prt.parent
        return count

    for el in nodes:
        cur = el
        while cur:
            txt = ''.join(list(cur.stripped_strings))
            segs = jieba.lcut(txt)
            word_count = cur.attrs['_my_word_count'] if '_my_word_count' in cur.attrs else 0
            cur.attrs['_my_word_count'] = word_count + len(segs)
            prt = cur.parent
            cur = prt if prt and prt.name != stoptag else None

    nodes = root.find_all(True)
    nodes = [{
        'el': o,
        'word_count': o.attrs['_my_word_count'],
        'depth_count': soup_depth_count(o, stoptag) + 1
    } for o in nodes if hasattr(o, 'attrs') and '_my_word_count' in o.attrs]

    for o in nodes:
        o['gscore'] = o['word_count']*(1-depth_weight)+o['depth_count']*depth_weight
        o['gscore'] = int(o['gscore'])
        del o['el'].attrs['_my_word_count']
    return nodes
