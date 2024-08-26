with open('/Users/yanyuming/Downloads/GitHub/PurePage/main copy 2.py', 'r') as f:
    tw_string = f.read()
import re
print(" ".join(re.findall(r'(tw-[a-z-0-9:]+)', tw_string)))