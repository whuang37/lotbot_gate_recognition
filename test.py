import json

dict = {"result": True}

x = json.dumps(dict)

y = json.loads(x)
print(y["result"])

if json.loads(x)["result"] == True:
    print('works')