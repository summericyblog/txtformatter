import re

patterns_general = []
patterns_general.append(re.compile(r'第[^\s]*?节'))
patterns_general.append(re.compile(r'第[^\s]*?章'))
patterns_general.append(re.compile(r'第[^\s]*?卷'))
patterns_general.append(re.compile(r'第[^\s]*?部'))
patterns_general.append(re.compile(r'第[^\s]*?册'))

patterns_special = []
patterns_special.append({'l': -1, 'p': re.compile(r'序 '), 'i': 0})
patterns_special.append({'l': -1, 'p': re.compile(r'序章'), 'i': 0})
patterns_special.append({'l': -1, 'p': re.compile(r'楔子'), 'i': 0})
patterns_special.append({'l': -1, 'p': re.compile(r'后记'), 'i': -1})
