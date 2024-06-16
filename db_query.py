import os
# import fil
import sys

for i,arg in enumerate(sys.argv):
    print(i, arg)
# if len(sys.argv) < 2:
#     print("Usage: python repeater.py <text>")
# else:
    # Join all the arguments except the script name
query_or_file = ' '.join(sys.argv[1:])
print(f'searching for {query_or_file}')
if os.path.exists(query_or_file):
    with open(query_or_file) as f:
        query = f.read()
print(f'query is:\n{query}')
    # res = fil.sql(query)
    # for row in res:
    #     print(row)