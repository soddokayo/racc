#racp.py

import glob, re

# load all logs
files = glob.glob('./RACCLOG *.txt')

records = []

for file in files:
    fin = open(file, 'r', encoding='utf8')
    lines = fin.readlines()

    record = ''
    matchstr = re.compile(r'\[.*\]')    # detect [*]
    for line in lines:
        if matchstr.match(line) is not None:
            records.append(record)      # add record to records
            record = ''
        else:
            record += line              # add line to record
    records.append(record)

print("total " + str(len(records)) + " records.")

# parse HTML tags
cnt=0
for record in records:
    intext = re.sub(r'\<[^>]*\>','\n',record)     # erase <*> (HTML)
    intext = re.sub(r'\([^)]*\)','\n',intext)     # erase (*) (time)
    intext = re.sub('&lt;','',intext)     # erase &lt; (escape)
    intext = re.sub('&gt;','',intext)     # erase &gt; (escape)
    intext = re.sub('http://www.gagalive.com','',intext)     # erase siteURL;
    for line in intext.split('\n'):
        if '010' in line:     # phone numbers
            cnt+=1
            print(str(cnt) + "(num): " + line)

        eng = re.sub(r'[^a-zA-Z]','',line).strip('\n')
        if eng == '':
            pass
        elif 'SPAM' in line or '스팸' in line:
            pass
        else:                   # ID, URL or email
            cnt+=1
            print(str(cnt) + "(eng): " + line)
