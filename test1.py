from main import WengerApi


login2 = WengerApi("bbadescu", "TryingVPN!", "Token 3a3e4cfc386b8e7c0ea6e98a922b2bda7866ff94")

#ex1

# print("Create weight entry")
# login2.create_weight_entry('2021-05-31','150')
# print("Get weight entry")
# weight_list = login2.get_req('weightentry')
# print(weight_list)


#ex2

# for i in range(7):
#     req1 = login2.create_nutrition_plan()
#     print(req1)
#
# req1 = login2.get_req('nutritionplan')
#
# for nutrition in req1["results"][0:3]:
#
#     for i in range(5):
#         req2 = login2.create_meals_for_nutrition_plans(nutrition['id'])
#         print(req2)
#
#
# for nutrition in req1["results"][3:7]:
#     for i in range(5):
#         req2 = login2.create_meals_for_nutrition_plans(nutrition['id'])
#         print(req2)


#ex3


#ex4
name_of_workout = "Workout5"
add_workout = login2.add_workout_day(name_of_workout,"This is workout5")
print(add_workout)
# create days for the added workout

get_workout = login2.get_req('workout')
for workout in get_workout['results']:
    if workout['name'] == name_of_workout:
        id1 = workout['id']
        add_day1 = login2.add_day(workout['id'],"Push",1)
        add_day2 = login2.add_day(workout['id'],"Pull",2)
        add_day3 = login2.add_day(workout['id'],"Legs",3)

        days = login2.get_req('day')
        list_of_days = list()
        for day in days["results"]:
            if day["training"] == id1:
                list_of_days.append(day["id"])

        for id in list_of_days:
            for i in range(6):
                add_exercise_per_day = login2.add_exercise(id,5,2)








#ex 5

# add_schedule = login2.add_schedule("Schedule1","2021-05-21",True,True)
# schedules = login2.get_req("schedule")
# for schedule in schedules["results"]:
#     if schedule["name"] == "Schedule1":
#         for work in get_workout['results']:
#             login2.add_workout_to_schedule(schedule["id"],work["id"],duration=5)


#ex6

# delete_exercise = login2.delete_exercise(270637,137838,262858)
# print(delete_exercise)

#ex7
# workout_id = get_workout["results"][1]["id"]
# delete = login2.delete_workout(workout_id)
# print(delete)