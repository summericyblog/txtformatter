import re
import cn2an

import patterns

patterns_general = patterns.patterns_general
patterns_special = patterns.patterns_special
sector_names = ['章', '卷', '册', '部']


class Sector:
    def __init__(self, text):
        self.text = text
        self.title = []
        self.para = []

    def format_title(self):
        paralist = self.text.strip('\n').split('\n')
        signal = False
        for line in paralist:
            temp = line.strip().strip('\t')
            for i, p in enumerate(patterns_general):
                match = p.match(temp)
                if match:
                    low, high = match.span()
                    number_raw = temp[low+1:high-1]
                    if number_raw.isdigit():
                        number = number_raw
                    else:
                        try:
                            number = cn2an.cn2an(number_raw)
                        except Exception:
                            continue
                            number = -1
                    title = temp[high:].strip()
                    this_dict = {'index': i, 'number': number, 'title': title}
                    self.title.append(this_dict)
                    signal = True
                    break
            for p in patterns_special:
                match = p['p'].match(temp)
                if match:
                    low, high = match.span()
                    title = temp[high:].strip()
                    this_dict = {'index': p['l'], 'number': p['i'], 'title': title}
                    self.title.append(this_dict)
                    signal = True
                    break
            if signal:
                signal = False
                continue
            else:
                self.para.append(temp)
        return 0


def para_valid(sec):
    if sec.title:
        return True
    p = sec.para[0]
    if (not p.strip('=')) or p.startswith('内容简介'):
        return False
    return True


def title2text(t):
    text = ''
    if t['index'] == -1:
        if t['number'] == 0:
            text += '序章'
        elif t['number'] == -1:
            text += '后记'
    elif t['index'] >= 0 and t['index'] <= 3:
        text += '第' + str(t['number']) + sector_names[t['index']]
    else:
        return 'Error' + t['title']
    if t['title']:
        text += ' ' + t['title']
    text += '\n'
    return text



class Reader:
    def __init__(self, text):
        self.text = text
        self.sector = []
        self.levels = []
        self.drop_sector = []
    
    def __getitem__(self, position):
        return self.sector[position]

    def load(self):
        paras = self.text.split('\n\n')
        for p in paras:
            this_sector = Sector(p)
            this_sector.format_title()
            self.sector.append(this_sector)
        return 0

    def format(self):
        self.drop_sector = [sec for sec in self.sector if not para_valid(sec)]
        self.sector = [sec for sec in self.sector if para_valid(sec)]
        single_title = [(i, sec.title) for i, sec in enumerate(self.sector) if not sec.para]
        for i, titles in reversed(single_title):
            for t in reversed(titles):
                self.sector[i+1].title.insert(0, t)
        self.sector = [sec for sec in self.sector if sec.para]
        levels = []
        for sec in self.sector:
            levels.extend(list([t['index'] for t in sec.title]))
        levels = sorted(list(set(levels)))
        if levels[0] == -1:
            levels = levels[1:]
            self.levels.append(-1)
        self.levels.extend(list(range(len(levels))))
        for sec in self.sector:
            for t in sec.title:
                if t['index'] == -1:
                    continue
                t['index'] = levels.index(t['index'])            
        return 0

    def to_content(self):
        text = ''
        for sec in self.sector:
            for t in sec.title:
                text += title2text(t)
        return text

    def to_txt(self):
        text = ''
        for sec in self.sector:
            for t in sec.title:
                text += title2text(t)
            text += '\n'.join(sec.para)
            text += '\n\n'
        return text

