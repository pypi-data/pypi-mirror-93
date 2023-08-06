import pandas as pd
from bs4 import BeautifulSoup as bs
import re

file = "/Users/fcruz1022/OneDrive - CBS Corporation/Work/promo/Dly_IREG.doc"

soup = bs(open(file, encoding = 'ISO-8859-1').read())
[s.extract() for s in soup(['style', 'script'])]
tmpText = soup.get_text()
text3 = "".join("".join(tmpText.split('\t')).split('\n')).encode('utf-8').strip()

d = re.search(r'Date\:(.*?)Time\:', tmpText).group(1).strip()
bb = re.search(r'\t[0-9](.*?)Broadcast Irregularity Report', tmpText, re.DOTALL)
bb0= bb.group()
#print(bb)
print(bb0)

#text_file = open("Output.txt", "w")
#text_file.write(textu)
#text_file.close()

column_names = ["clear","scheduled_time", "program_name", "comm","discrepancy","explanation"]
df = pd.DataFrame(columns = column_names)
#df = pd.DataFrame([x.split('\t') for x in bb0], columns=column_names)
lines = bb0.split('\n')
i = 0
for x in lines:
    row = x.split('\t')
    if len(row) == 6:
        df.loc[len(df)] = row
    elif (len(row) == 5) and (row[3] != 'Yes' or  row[3] != 'No'):
        row.insert(3, "")
        df.loc[len(df)] = row
