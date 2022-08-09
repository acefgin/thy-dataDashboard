import requests
import json

# Now we have to request our JSON data through
# the API package
res = requests.get("https://jsonplaceholder.typicode.com/todos")
todos = json.loads(res.text)

# To view your Json data, type var and hit enter
todos

# Now our Goal is to find the User who have
# maximum completed their task !!
# i.e we would count the True value of a
# User in completed key.
# {
	# "userId": 1,
	# "id": 1,
	# "title": "Hey",
	# "completed": false, # we will count
						# this for a user.
# }

# Note that there are multiple users with
# unique id, and their task have respective
# Boolean Values.


def find(todo):
	check = todo["completed"]
	# max_var = todo["userId"] in users
	return check 

# To find the values.

Value = list(filter(find, todos))

# To write these value to your disk

with open("sample.json", "w") as data:
	# Value = list(filter(keep, todos))
	json.dump(Value, data, indent = 2)

curUser = 0
cur_max = 0
global_max = 0
for data in Value:
	if data["userId"] != curUser:
		cur_max = 1
		curUser = data["userId"]
	cur_max += 1
	if cur_max > global_max:
		global_max = cur_max
		best_user = curUser

print(best_user)