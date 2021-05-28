import random
from pprint import pprint

from main import WengerApi

login1 = WengerApi("balbaealexandru@gmail.com","12345678abc","Token 5c4f8bef9dd4e6d72f0868971ac142cca0157431")


def exercise1():
    print("Create weight entry")
    login1.create_weight_entry('2021-05-31','150')
    print("Get weight entry")
    weight_list = login1.get_req("weightentry")
    print(weight_list)


def exercise2():
    login1.delete_nutrition_plans()

    days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    for day in days_of_week:
        login1.create_nutrition_plan(day)


    nutrition_plans = login1.get_req('nutritionplan')

    for nutrition in nutrition_plans.get("results"):
        req2 = login1.create_meals_for_nutrition_plans(nutrition.get('id'))
        print(req2)

    list_of_total_meals = list()

    meals1 = login1.get_req('meal')
    print(meals1)

    for meal in meals1.get('results'):
        list_of_total_meals.append(meal)

    amount = 100
    ingredients_req = login1.get_req('ingredient')
    list_of_ingredients = ingredients_req.get('results')
    for nutrition in nutrition_plans.get('results'):
        for meal in list_of_total_meals:
            kcal = 0
            if meal.get('plan') == nutrition.get('id'):
                if nutrition.get('description') in ['Monday', 'Tuesday', 'Wednesday']:
                    while True:
                        ingredient = random.choice(list_of_ingredients)
                        kcal += ingredient.get('energy') * (amount/100)
                        if kcal > 1750:
                            print(kcal)
                            break
                        add_item = login1.add_meal_item(meal.get('id'),ingredient.get('id'),amount)
                        print(add_item)
                elif nutrition.get('description') in ['Thursday', 'Friday', 'Saturday', 'Sunday']:
                    while True:
                        ingredient = random.choice(list_of_ingredients)
                        add_item = login1.add_meal_item(meal.get('id'), ingredient.get('id'),amount)
                        print(add_item)
                        kcal += ingredient.get('energy') * (amount/100)
                        if kcal > 1750:
                            print(kcal)
                            break


def exercise4():
    name_of_workout = "Workout50"
    add_workout = login1.add_workout_day(name_of_workout,"This is workout10")
    print(add_workout)

    exercises_get_total = login1.get_req('exercise')
    list_of_exercises = exercises_get_total.get('results')

    chest_exercises_list = list()
    back_exercises_list = list()
    legs_exercises_list = list()
    abs_exercises_list = list()
    arms_exercises_list = list()
    sholders_exercises_list = list()
    calves_exercises_list = list()
    exercises_category = {
            8:  arms_exercises_list,
            9:  legs_exercises_list,
            10: abs_exercises_list,
            11: chest_exercises_list,
            12: back_exercises_list,
            13: sholders_exercises_list,
            14: calves_exercises_list
    }
    for exercise in list_of_exercises:
        for key in exercises_category.keys():
            if exercise.get('category') == key:
                exercises_category[key].append(exercise)

    get_workout = login1.get_req('workout')
    for workout in get_workout.get('results'):
        if workout.get('name') == name_of_workout:
            id1 = workout.get('id')
            login1.add_day(id1,"Push",1)
            login1.add_day(id1,"Pull",2)
            login1.add_day(id1,"Legs",3)

    days = login1.get_req('day')
    for day in days.get('results'):
        if day.get('training') == id1:
            id_day = day.get('id')
            for i in range(6):
                number_of_set = 4
                order = 2
                login1.add_exercise(day.get('id'),number_of_set,order)

            dict1 = {
                "Push": random.choice(chest_exercises_list),
                "Pull": random.choice(back_exercises_list),
                "Legs": random.choice(calves_exercises_list)
            }

            list_of_exercises_day = list()
            list_of_exercises_day.append(random.choice(back_exercises_list))
            list_of_exercises_day.append(random.choice(chest_exercises_list))
            list_of_exercises_day.append(random.choice(arms_exercises_list))
            list_of_exercises_day.append(random.choice(sholders_exercises_list))
            list_of_exercises_day.append(random.choice(legs_exercises_list))
            for key in dict1.keys():
                if day.get('description') == key:
                    list_of_exercises_day.append(dict1[key])


            all_exercise_comments = login1.get_req('exercisecomment')
            with open(f"{day.get('description')}_comments.txt","w") as comment_file:
                for exe in list_of_exercises_day:
                    for comments in all_exercise_comments.get('results'):
                        if exe.get('id') == comments.get('exercise'):
                            comment_file.write(f"The exercise with id <{exe.get('id')}> has comment <{comments.get('comment')}> \n")


            sets_req = login1.get_req('set')
            list_of_sets = list()
            for set in sets_req.get('results'):
                if set.get('exerciseday') == id_day:
                    list_of_sets.append(set)
            exercise_set_match = zip(list_of_exercises_day,list_of_sets)

            for exercises_match in exercise_set_match:
                setting_req = login1.setting_exercise_set(exercises_match[1].get('id'),exercises_match[0].get('id'),1,6,"70.00",1,"0.5")
                print(setting_req)


def exercise5():
    get_workout = login1.get_req('workout')
    add_schedule = login1.add_schedule("Schedule1","2021-05-21",True,True)
    print(add_schedule)
    schedules = login1.get_req("schedule")
    for schedule in schedules.get("results"):
        if schedule.get("name") == "Schedule1":
            for work in get_workout.get('results'):
                login1.add_workout_to_schedule(schedule.get("id"),work.get("id"),duration=5)


def exercise6():
    delete_exercise = login1.delete_exercise(272071),
    print(delete_exercise)


def exercise7():
    delete = login1.delete_workout()
    print(delete)


if __name__ == "__main__":
    exercise7()
    # exercise1()
    # exercise2()
    exercise4()
    # exercise5()
    # exercise6()
