from main import WengerApi
from pprint import pprint



login1 = WengerApi("balbaealexandru@gmail.com","12345678abc","Token 5c4f8bef9dd4e6d72f0868971ac142cca0157431")

# req1 = login1.parse_toml(toml_file='workouts.toml')
# pprint(req1)
#
# req2 = login1.get_nutrition_plans_list()
#
# pprint(req2)
#
# req3 = login1.get_nutrition_plans_meals('nutrition_plan1')
# req4 = login1.get_items_from_meals('nutrition_plan1','meal1')
# pprint(req4)


# login1.add_nutrition_plans(None)

# req = login1.add_nutrition_plans_toml('toml_file.toml')

# print("Nutrition list!")
# req2 = login1.get_nutrition_plans_list()
# pprint(req2.keys()[0])
#
#
# print("Print nutrition plan meals")
# req3 = login1.get_nutrition_plans_meals()
# pprint(req3)




login1.add_workouts_toml_file('workouts.toml')


# exercises_day1 = login1.get_exercises('workout1','day1')
# pprint(exercises_day1)
# setting_exercise = login1.get_exercises_settings('workout1','day1','exercise1')
# pprint(setting_exercise)
# setting_informations = login1.get_setting_informations('workout1','day1','exercise1','setting1')
# pprint(setting_informations)
#
# pprint(setting_informations)
#
#
