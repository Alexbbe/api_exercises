from main import WengerApi





login2 = WengerApi("bbadescu", "TryingVPN!", "Token 3a3e4cfc386b8e7c0ea6e98a922b2bda7866ff94")
# print(login2.header)
# print(login1.header)
# print(WengerApi.headers1)
# print("Get days")
# req2 = login2.get_req('day')
# print(req2)
print("Create weight entry")
login2.create_weight_entry('2021-05-31','150')
# print("Get weight entry")
weight_list = login2.get_req('weightentry')
print(weight_list)

# pprint(login2.parse_toml(toml_file='toml_file.txt'))
# pprint(login2.get_nutrition_plans_list())
# pprint(login2.get_nutrition_plans_meals())


#ex2

for i in range(7):
    req1 = login2.create_nutrition_plan()
    print(req1)

req1 = login2.get_req('nutritionplan')
for nutrition in req1['results']:
    for i in range(5):
        login2.create_meals_for_nutrition_plans(nutrition['id'])

    # meal = login2.get_req('')


#ex3



