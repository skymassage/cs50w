import json

a = {"one": 1, "two":2, "three":3}
b = {"four":4, "five":5, "six":6}
l = [a,b]
# print(l)
# print(str(l))
_a = '{"one": 1, "two":2, "three":3}'
print(str(a))
# print(json.loads("str(a)"))
json.loads("{}".format(str(a)))