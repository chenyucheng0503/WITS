import re

pattern = re.compile(r'\d{6}')
with open("/Users/graham/Downloads/HScode", 'r') as f:
    data = f.read()
    result = pattern.findall(data)
    with open("/Users/graham/Downloads/HS", 'w') as w:
        for r in result:
                w.write(r + "\n")
