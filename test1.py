import random

from main import WengerApi
from pprint import pprint
login1 = WengerApi("balbaealexandru@gmail.com","12345678abc","Token 5c4f8bef9dd4e6d72f0868971ac142cca0157431")

#ex1
print("Create weight entry")
login1.create_weight_entry('2021-05-31','150')
print("Get weight entry")
weight_list = login1.get_req('weightentry')


#ex2

days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
for day in days_of_week:
    req1 = login1.create_nutrition_plan(day)


nutrition_plans = login1.get_req('nutritionplan')

for nutrition in nutrition_plans.get("results"):
    req2 = login1.create_meals_for_nutrition_plans(nutrition.get('id'))
    print(req2)

list_of_total_meals = list()
limit = 20
meals1 = login1.get_req('meal',0,20)
print(meals1)
meals2 = login1.get_req('meal',20,20)
print(meals2)
for meal in meals1.get('results'):
    list_of_total_meals.append(meal)
for meal in meals2.get('results'):
    list_of_total_meals.append(meal)

print(list_of_total_meals)

for nutrition in nutrition_plans.get('results'):

    for meal in list_of_total_meals:
        if meal.get('plan') == nutrition.get('id') and nutrition.get('description') in ['Monday', 'Tuesday', 'Wednesday']:
            kcal = 0
            while True:
                amount = 100
                ingredients_req = login1.get_req('ingredient')
                list_of_ingredients = ingredients_req.get('results')
                ingredient = random.choice(list_of_ingredients)
                print(ingredient)
                kcal += ingredient.get('energy') * (amount/100)
                if kcal > 1750:
                    print(kcal)
                    break
                add_item = login1.add_meal_item(meal.get('id'),ingredient.get('id'),amount)
                print(add_item)

        elif meal.get('plan') == nutrition.get('id') and nutrition.get('description') in ['Thursday', 'Friday', 'Saturday', 'Sunday']:
            kcal= 0
            while True:
                amount = 100
                ingredients_req = login1.get_req('ingredient')
                list_of_ingredients = ingredients_req.get('results')
                ingredient = random.choice(list_of_ingredients)
                print(ingredient)
                add_item = login1.add_meal_item(meal.get('id'), ingredient.get('id'),amount)
                print(add_item)
                kcal += ingredient.get('energy') * (amount/100)
                if kcal > 1900:
                    print(kcal)
                    break

# ex4
name_of_workout = "Workout38"
add_workout = login1.add_workout_day(name_of_workout,"This is workout10")
print(add_workout)

exercises_get = login1.get_req('exercise')
limit = exercises_get.get('count')
exercises_get_total = login1.get_req('exercise',0,limit)
list_of_exercises = exercises_get_total.get('results')

chest_exercises_list = list()
back_exercises_list = list()
legs_exercises_list = list()
abs_exercises_list = list()
arms_exercises_list = list()
sholders_exercises_list = list()
calves_exercises_list = list()

for exercise in list_of_exercises:
    if exercise.get('category') == 11:
        chest_exercises_list.append(exercise)
    elif exercise.get('category') == 12:
        back_exercises_list.append(exercise)
    elif exercise.get('category') == 9:
        legs_exercises_list.append(exercise)
    elif exercise.get('category') == 13:
        sholders_exercises_list.append(exercise)
    elif exercise.get('category') == 8:
        arms_exercises_list.append(exercise)
    elif exercise.get('category') == 14:
        calves_exercises_list.append(exercise)
    else:
        abs_exercises_list.append(exercise)


get_workout = login1.get_req('workout')
for workout in get_workout.get('results'):
    if workout.get('name') == name_of_workout:
        id1 = workout.get('id')
        add_day1 = login1.add_day(id1,"Push1",1)
        add_day2 = login1.add_day(id1,"Pull1",2)
        add_day3 = login1.add_day(id1,"Legs1",3)

days = login1.get_req('day',0,200)
for day in days.get('results'):
    if day.get('training') == id1:
        id_day = day.get('id')
        for i in range(6):
            number_of_set = 4
            order = 2
            req4 = login1.add_exercise(day.get('id'),number_of_set,order)

        list_of_exercises_day = list()
        if day.get('description') == 'Push1':
            list_of_exercises_day.append(random.choice(back_exercises_list))
            list_of_exercises_day.append(random.choice(chest_exercises_list))
            list_of_exercises_day.append(random.choice(sholders_exercises_list))
            list_of_exercises_day.append(random.choice(abs_exercises_list))
            list_of_exercises_day.append(random.choice(chest_exercises_list))
            list_of_exercises_day.append(random.choice(arms_exercises_list))
        elif day.get('description') == 'Pull1':
            list_of_exercises_day.append(random.choice(back_exercises_list))
            list_of_exercises_day.append(random.choice(back_exercises_list))
            list_of_exercises_day.append(random.choice(chest_exercises_list))
            list_of_exercises_day.append(random.choice(abs_exercises_list))
            list_of_exercises_day.append(random.choice(sholders_exercises_list))
            list_of_exercises_day.append(random.choice(arms_exercises_list))
        elif day.get('description') == 'Legs1':
            list_of_exercises_day.append(random.choice(back_exercises_list))
            list_of_exercises_day.append(random.choice(legs_exercises_list))
            list_of_exercises_day.append(random.choice(chest_exercises_list))
            list_of_exercises_day.append(random.choice(legs_exercises_list))
            list_of_exercises_day.append(random.choice(calves_exercises_list))
            list_of_exercises_day.append(random.choice(abs_exercises_list))
        pprint(list_of_exercises_day)

        exercise_comments = login1.get_req('exercisecomment')
        comment_limit = exercise_comments.get('count')
        exercise_images = login1.get_req('exerciseimage')
        images_limit = exercise_images.get('count')
        all_exercise_comments = login1.get_req('exercisecomment',offset=0,limit=comment_limit)
        all_exercise_images = login1.get_req('',offset=0,limit=images_limit)
        f = open(f"{day.get('description')}_comments.txt","w")
        for exe in list_of_exercises_day:
            for comments in all_exercise_comments.get('results'):
                if exe.get('id') == comments.get('exercise'):
                    f.write(f"The exercise with id <{exe.get('id')}> has comment <{comments.get('comment')}> \n")
        f.close()

        sets_req = login1.get_req('set',offset=0,limit=400)
        list_of_sets = list()
        for set in sets_req.get('results'):
            if set.get('exerciseday') == id_day:
                list_of_sets.append(set)
        exercise_set_match = zip(list_of_exercises_day,list_of_sets)

        for exercises_match in exercise_set_match:
            setting_req = login1.setting_exercise_set(exercises_match[1].get('id'),exercises_match[0].get('id'),1,6,"70.00",1,"0.5")


#ex 5
add_schedule = login1.add_schedule("Schedule1","2021-05-21",True,True)
schedules = login1.get_req("schedule")
for schedule in schedules["results"]:
    if schedule["name"] == "Schedule1":
        for work in get_workout['results']:
            login1.add_workout_to_schedule(schedule["id"],work["id"],duration=5)

#ex6

delete_exercise = login1.delete_exercise()
print(delete_exercise)

#ex7
delete = login1.delete_workout()
print(delete)