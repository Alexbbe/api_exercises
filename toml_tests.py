from main import WengerApi
from pprint import pprint



login1 = WengerApi("balbaealexandru@gmail.com","12345678abc","Token 5c4f8bef9dd4e6d72f0868971ac142cca0157431")
#
# req1 = login1.parse_toml(toml_file='toml_file.toml')
# pprint(req1["nutrition_plans"])
#
# req2 = login1.get_nutrition_plans_list()
#
# pprint(req2)
#
# req3 = login1.get_nutrition_plans_meals('nutrition_plan1')
# req4 = login1.get_items_from_meals('nutrition_plan1','meal1')
# pprint(req4)


login1.add_nutrition_plans()



# print("Nutrition list!")
# req2 = login1.get_nutrition_plans_list()
# pprint(req2.keys()[0])
#
#
# print("Print nutrition plan meals")
# req3 = login1.get_nutrition_plans_meals()
# pprint(req3)


