import json
f = open('BACKEND_FLOW_EXPLANATION.ipynb', encoding='utf-8')
nb = json.load(f)
print(f"Cells: {len(nb['cells'])}")
f.close()
