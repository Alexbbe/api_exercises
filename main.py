import random

import requests
from datetime import date
import calendar
import toml


class WengerApi:

    headers1 = {'Accept': 'application/json'}
    def __init__(self, username, password,token):
        self.username = username
        self.password = password
        self.token = token
        self.header = WengerApi.headers1.copy()
        self.header["Authorization"] = token
        # call login method when a new object is created
        self.login()

    def login(self):
        """
        This method do the login procedure for the Wger application
        :return:
        - the request body if the login is successfully
        - False if the login couldn't be performed
        """
        data = {"username": {self.username},
                "password": {self.password},
                "submit": "Login"}
        url = 'https://wger.de/en/user/login'
        # get the CSRF token from the login GET request
        login_get = requests.get(url=url, headers=self.header)
        self.header['X-CSRFToken'] = login_get.cookies["csrftoken"]
        self.header['Referer'] = url
        session_id = login_get.cookies.get("sessionid")
        csrf_token = login_get.cookies.get("csrftoken")
        cookie_full = f"csrftoken={csrf_token}; sessionid={session_id}"
        self.header["Cookie"] = cookie_full
        req = requests.post(url=url, data=data, headers=self.header)
        if req.status_code in [200, 201]:
            return req, "The login was performed successfuly"
        else:
            return False, f"Error {req.status_code}"

    def get_req(self, object):
        """
        This method do GET request for specific API
        :param object: the name of the API
        :return: g.json() - Response of the GET req if the request was performed successfully.
                False - if the request couldn't be made or the URL is invalid
        """
        g1 = requests.get('https://wger.de/api/v2/')
        url = g1.json().get(object)
        if url is not None:
            req1 = requests.get(url=url, headers=self.header)
            count = req1.json().get('count')
            url1 = url + f"?limit={count}&offset=0"
            g = requests.get(url=url1, headers=self.header)
            if g.status_code == 200:
                return g.json(), f"The get request for {object} was performed successfully"
            else:
                return False, "Couldn't make the request!"
        else:
            return False, 'Invalid url'

    def post_req(self, object, data):
        """
        This method make POST request for an API
        :param object: the name of the API
        :param data: data in json format containing the parameters of the POST request
        :return:req - The body of the request, if was performed successfully.
                False - if the request couldn't be made or the URL is invalid
        """
        g1 = requests.get('https://wger.de/api/v2/')
        url1 = g1.json().get(object)
        if url1 is not None:
            req = requests.post(url=url1,data=data,headers=self.header)
            if req.status_code == 201:
                return req, f'The post request for {object} was done successfully'
            else:
                return False, f'Error  {req.status_code}'
        else:
            return False, 'Invalid url'

    def name_to_id(self, param1, param1_value, param2, object):
        """
        This method associate a given parameter with another parameter from API
        :param param1: Parameter name you want to associate
        :param param1_value: Parameter value you want to assciate
        :param param2: parameter from API you want to associate with
        :param object: The API name
        :return: Value of the param2 from API for a specific item
                - False if there is no association
        """
        req = self.get_req(object)
        for item in req[0].get('results', []):
            if item.get(param1) == param1_value:
                return item.get(param2), f"The id for {param1} was provided successfully"

        return False, f"The item with {param1} doesn't have id"

    def delete_req(self, object, id=None):
        """
        This method perform DELETE request for API
        :param object: The API name
        :param id: The id of the element you want to delete
        :return: -The request body if the delete was performed successfully
                 -False if the URL doesn't exist or the DELETE request couldn't be performed
        """
        g1 = requests.get('https://wger.de/api/v2/')
        url1 = g1.json().get(object)
        if url1 is not None:
            url = f"{url1}/{id}"
            req = requests.delete(url=url, headers=self.header)
            if req.status_code not in (200, 202, 204):
                return False, f"The delete for id {id} couldn't be performed"
            return req, f"The delete for {object} with id {id} was performed" \
                         f"successfully! Status code is {req.status_code}"
        else:
            return False, "Error! The URL doesn't exists!"

    def create_weight_entry(self, date, value):
        """
        This method create a weight entry
        :param date:the notification date of the weight
        :param value:value of the weight
        """
        data = {
            "date": date,
            "weight": value
        }
        return self.post_req('weightentry',data)

    def create_nutrition_plan(self, description=None):
        """
        This method create a nutrition plan
        :param description: The description of the
        nutrition plan (default is None- will get the current day of week)
        :return:
        """
        if description is None:
            my_date = date.today()
            description = calendar.day_name[my_date.weekday()]
        data = {
            'description': description
        }
        return self.post_req('nutritionplan', data)

    def create_meals_for_nutrition_plans(self, plan, time=None):
        """
        This method create meal for a nutrition plan
        :param plan: the id of the nutrition plan
        :param time: The time of the day when the meal is scheduled
        """
        data = {
            'plan': plan,
            'time': time
        }
        return self.post_req('meal', data)

    def add_meal_item(self, meal, ingredient, amount):
        """
        This method will create an item for a meal
        :param meal: The id of the meal
        :param ingredient: The id of the ingredient
        :param amount:  The quantity of the ingredient
        """
        data = {
            'meal': meal,
            'ingredient': ingredient,
            'amount': amount
        }

        return self.post_req('mealitem',data)

    def add_workout_day(self, name, description):
        """
        This method will create an workout
        :param name: The name of the workout
        :param description: The description of the workout
        """
        data = {
            "name": name,
            "description": description
        }

        return self.post_req('workout', data)

    def add_day(self, training, description, day):
        """
        This method will add a day for an workout
        :param training: The workout id
        :param description: The description of the workout
        :param day: The day of the week
        """
        workouts = self.get_req('workout')
        list_of_workout = list()
        workouts_list = workouts[0].get('results')
        if workouts_list is not None:

            for workout in workouts_list:
                list_of_workout.append(workout["id"])

        if training not in list_of_workout:
            return False, f"The training with id {training} doesn't exists!"
        data ={
            "training": training,
            "description": description,
            "day": day
        }
        return self.post_req('day', data)

    def add_exercise(self, exerciseday, sets, order):
        """
        This method add an exercise for a day
        :param exerciseday: The id of the workout day
        :param sets: The number of sets of exercise
        :param order:
        """
        data = {
            'exerciseday': exerciseday,
            'sets': sets,
            'order': order
        }

        return self.post_req('set', data)

    def setting_exercise_set(self, set, exercise, repetition_unit, reps, weight, weight_unit, rir):
        """
        This method will configure each set of the added exericse
        :param set: The id of the set
        :param exercise: The exercise type
        :param repetition_unit: The unit of te repetitions
        :param reps: The number of repetitions
        :param weight: The weight used for an exercise
        :param weight_unit: The weight unit
        :param rir:
        """
        data = {
            'set': set,
            'exercise': exercise,
            'repetition_unit': repetition_unit,
            'reps': reps,
            'weight': weight,
            'weight_unit': weight_unit,
            'rir': rir,
        }

        return self.post_req('setting',data)


    def add_schedule(self, name, start_date, is_active, is_loop):
        """
        This method add schedule for workout
        :param name: Name of the schedule
        :param start_date: The start date of the schedule
        :param is_active: If the schedule is active or not
        :param is_loop: If the schedule is loop or not
        """
        data = {
            'name': name,
            'start_date': start_date,
            'is_active': is_active,
            'is_loop': is_loop
        }
        return self.post_req('schedule', data)

    def add_workout_to_schedule(self, schedule, workout, duration):
        """
        This method adds the workout to the schedule
        :param schedule: The schedule id
        :param workout: The workout id
        :param duration: The duration of the schedule
        """
        data = {
            'schedule': schedule,
            'workout': workout,
            'duration': duration
        }

        return self.post_req('schedulestep', data)

    def get_random_id(self, object):
        """
        This method return a random id from a list of API valid IDs.
        :param object: The API name
        :return: A random valid id
        """
        object_req = self.get_req(object)
        list_of_ids = list()
        if object_req[0]:
           for elem in object_req[0].get('results'):
               list_of_ids.append(elem.get('id'))
        return random.choice(list_of_ids)

    def delete_workout(self, id=None):
        """
        This method delete a workout
        :param id: The id of the workout to be deleted
        :return: - True is all workouts were deletes
                - False if there no workouts
                - False if some workouts couldn't be deleted
        """
        workouts = self.get_req('workout')
        list_of_id = list()
        for workout in workouts[0].get('results', []):
            list_of_id.append(workout.get('id'))
        if id is not None:
            if id in list_of_id:
                req = self.delete_req('workout', id)
                return req, f"Workout with id {id} was deleted successfully "
            else:
                return False, f"Workout with id {id} was not found!"
        else:
            if len(list_of_id) != 0:
                undeleted_workouts = list()
                for id1 in list_of_id:
                    req2 = self.delete_req('workout', id1)
                    if req2 is False:
                        undeleted_workouts.append(id1)
                if len(undeleted_workouts) == 0:
                    return True, "All existing workouts has been deleted!"
                else:
                    return False, f"The following workouts couldn't be deleted {undeleted_workouts}"
            else:
                return False, "There are no workouts to be deleted"

    def delete_all_nutrition_plans(self):
        """
        This meal delete al nutrition plans
        :return: -True is all nutrition plans were deleted
                 -False, if one nutrition plan couldn't be deleted
        """
        nutrition_plans = self.get_req('nutritionplan')
        for nutrition_plan in nutrition_plans[0].get('results', []):
            req = self.delete_req('nutritionplan', nutrition_plan.get('id'))
            if req[0] is False:
                return False
        return True

    def delete_all_meals_from_nutrition_plan(self):
        """
        This method delete all meals from a nutrtion plan
        :return: - True if all meal were deleted
                - False if one meal couldn't be deleted
        """
        meals = self.get_req('meal')
        for meal in meals[0].get('results', []):
            req = self.delete_req('meal', meal.get('id'))
            if req[0] is False:
                return False
        return True

    def delete_all_items_from_meal(self):
        """
        This method delete all items for a meal
        :return: - True if all items were deleted
                - False if one item couldn't be deleted
        """
        items = self.get_req('mealitem')
        for item in items[0].get('results', []):
            req = self.delete_req('mealitem', item.get('id'))
            if req[0] is False:
                return False
        return True

    def delete_exercise(self, workout_id=None, day_id=None, exercise_id=None):
        """
        This method delete an exercise from the nutrition plan
        :param workout_id: The id of the workout
        :param day_id:  The id of the workout day
        :param exercise_id: The id of the exercise
        :return: Return delete_req function' body
        """
        if workout_id is not None:
            list_of_workouts = self.get_req('workout')
            list_of_workouts_ids = list()
            for workout in list_of_workouts.get('results', []):
                list_of_workouts_ids.append(workout.get('id'))

            if day_id is not None:
                list_of_days = self.get_req('day')
                list_of_days_id = list()
                for day in list_of_days.get('results', []):
                    list_of_days_id.append(day.get('id'))

                if exercise_id is not None:
                    list_of_exercises = self.get_req('set')
                    list_of_exercises_ids = list()
                    for exercise in list_of_exercises.get('results', []):
                        list_of_exercises_ids.append(exercise.get('id'))
                    if exercise_id not in list_of_exercises_ids:
                        return False, f"The exercise with id {exercise_id} doesn't exists in " \
                                      f"day {day_id} and workout {workout_id}"
                    else:
                        req1 = self.delete_req('set', exercise_id)
                        return req1
                else:
                    if day_id not in list_of_days_id:
                        return False, f"The days with id {day_id} doesn't exists in workout {workout_id}"
                    else:
                        req2 = self.delete_req('day', day_id)
                        return req2
            else:
                if workout_id not in list_of_workouts_ids:
                    return False, f"The workout with id {workout_id} doesn't exists"
                else:
                    req3 = self.delete_workout(workout_id)
                    return req3
        else:
            req4 = self.delete_workout()
            return req4

    def delete_nutrition_plan(self, nutrtion_plan_id=None, meal_id=None, item_id=None):
        """
        This method
        -delete item from the nutrition plan (if item_id is not None)
        -delete a meal from the nutrition plan (if item_id is None)
        -delete a nutrition plan (if meal_id is None)
        -delete all nutrition plans if nutrition_plan is None
        :param nutrtion_plan_id: The id of the nutrition plan
        :param meal_id: The id of the meal
        :param item_id: The id of the item
        :return: - The delete_req body
                - False if an id is invalid
        """
        if nutrtion_plan_id is not None:
            list_of_nutrition_plans = self.get_req('nutritionplan')
            list_of_nutrition_plans_ids = list()
            for nutrition_plan in list_of_nutrition_plans[0].get('results', []):
                list_of_nutrition_plans_ids.append(nutrition_plan.get('id'))

            if meal_id is not None:
                list_of_meals = self.get_req('meal')
                list_of_meals_id = list()
                for meal in list_of_meals[0].get('results', []):
                    list_of_meals_id.append(meal.get('id'))

                if item_id is not None:
                    list_of_mealitems = self.get_req('mealitem')
                    list_of_mealitems_ids = list()
                    for item in list_of_mealitems[0].get('results', []):
                        list_of_mealitems_ids.append(item.get('id'))
                    if item_id not in list_of_mealitems_ids:
                        return False, f"The item with id {item_id} doesn't exists in " \
                                      f"meal {meal_id} and nutrition_plan {nutrtion_plan_id}"
                    else:
                        req1 = self.delete_req('mealitem', item_id)
                        return req1
                else:
                    if meal_id not in list_of_meals_id:
                        return False, f"The meal with id {meal_id} doesn't exists in nutrition_plan {nutrtion_plan_id}"
                    else:
                        req2 = self.delete_req('meal', meal_id)
                        return req2
            else:
                if nutrtion_plan_id not in list_of_nutrition_plans_ids:
                    return False, f"The nutrition_plan_id with id {nutrtion_plan_id} doesn't exists"
                else:
                    req3 = self.delete_req('nutritionplan',nutrtion_plan_id)
                    return req3
        else:
            req4 = self.delete_req('nutritionplan')
            return req4

    def get_random_num_outside_list(self, object):
        """
        This method returns an random invalid ID
        :param object: The API name
        :return: The invalid id
        """
        request = self.get_req(object)
        list_of_ids = list()
        for req in request[0].get('results', []):
            list_of_ids.append(req.get('id'))
        num = random.choice(list_of_ids)
        while num in list_of_ids:
            num = random.randint(10000, 99999)
            if num not in list_of_ids:
                return num

    #TOML part
    def parse_toml(self, toml_file):
        """
        This function convert TOML format into python dictionary
        :param toml_file: The file containing the TOML
        :return: The dictionary containing the data from the TOML
        """
        with open(toml_file) as file:
            data = file.read()
        parsed_toml = toml.loads(data)
        return parsed_toml

    #TOML part for nutrition plans
    def add_nutrition_plans_toml(self, toml_file_plans):
        """
        This method add nutrition plans based on TOML data
        :param toml_file_plans: The TOML file containing info about nutrition plans
        """
        parsed_toml = self.parse_toml(toml_file=toml_file_plans)
        if "nutrition_plans" in parsed_toml:
            nutrition_plans_dict = self.get_nutrition_plans_list(toml_file_plans)
            for nutrition_plan_key, nutrition_plan_value in nutrition_plans_dict.items():
                add_plan = self.create_nutrition_plan(description=nutrition_plan_key)
                nutrtion_plan_id = add_plan[0].json().get('id')
                if 'meals' in nutrition_plan_value:
                    meals_dict = nutrition_plan_value.get('meals')
                    self.add_meals_toml(meals_dict, nutrtion_plan_id)

    def add_meals_toml(self, meals_dict, nutrition_plan_id):
        """
        This method adds a meal based on the info from the TOML file
        :param meals_dict: The dictionary containing the meals
        :param nutrition_plan_id: The id of the nutrition plan
        """

        for meal_key, meal_value in meals_dict.items():
            add_meal = self.create_meals_for_nutrition_plans(nutrition_plan_id)
            meal_id = add_meal[0].json().get('id')

            if 'items' in meal_value:
                items_dict = meal_value.get('items')
                self.add_item_toml(items_dict, meal_id)

    def add_item_toml(self, items_dict, meal_id):
        """
        This method adds an item for a meal based on the info from the TOML file
        :param items_dict: The dictionary containing the items
        :param meal_id: The meal id
        """
        for item_key, item_value in items_dict.items():
            self.add_meal_item(meal_id, item_value.get('ingredient'),
                                           item_value.get('amount'))

    #TOML part for Workouts
    def add_workouts_toml_file(self, file):
        """
        This method adds a workout based on the info from TOML file
        :param file: The TOML file
        """
        toml_workouts = self.get_workouts(file=file)
        for workout_key, workout_value in toml_workouts.items():
            self.add_workout_day(workout_value.get('name'),
                                               workout_value.get('description'))

            if "days" in workout_value:
                toml_days = workout_value.get('days')
                self.add_days_for_workouts_toml(toml_days=toml_days, workout=workout_key)

    def add_days_for_workouts_toml(self, toml_days, workout):
        """
        This method adds a day for a specific workout based on the info from the TOML file
        :param toml_days: The dictionary of the days
        :param workout: The workout name
        """
        workout_id_req = self.name_to_id(param1='name', param1_value=workout, param2='id', object='workout')
        workout_id = workout_id_req[0]
        for day_key, day_val in toml_days.items():
            add_day1 = self.add_day(training=workout_id, description=day_val.get("description"),
                                    day=day_val.get('day'))

            day_id = add_day1[0].json().get('id')

            if "exercises" in day_val:
                toml_exercise = day_val.get('exercises')
                self.add_exercise_per_day_toml(exercise_toml=toml_exercise, day_id=day_id)

    def add_exercise_per_day_toml(self, exercise_toml, day_id):
        """
        This method adds an exercise for a specific day.
        :param exercise_toml: The dictionary of the exercise
        :param day_id: The ID of the day
        """
        for exercise_key, exercise_value in exercise_toml.items():
            add_exercise = self.add_exercise(day_id, sets=exercise_value.get('sets'), order=1)
            exercise_id = add_exercise[0].json().get('id')
            if 'settings' in exercise_value:
                toml_settings = exercise_value.get('settings')
                self.add_settings_per_exercise(toml_settings, exercise_id)

    def add_settings_per_exercise(self, toml_settings, exercise_id):
        """
        This method configure the set for a specific exercise based of the info from the TOML file
        :param toml_settings: The dictionary for the setting
        :param exercise_id: The Id of the exercise
        """
        for setting_key,setting_value in toml_settings.items():
            self.setting_exercise_set(              set=exercise_id
                                                    ,exercise=setting_value.get('exercise'),
                                                    repetition_unit=setting_value.get('repetition_unit')
                                                    ,reps=setting_value.get('reps')
                                                    ,weight=setting_value.get('weight')
                                                    ,weight_unit=setting_value.get('weight_unit')
                                                    ,rir=setting_value.get('rir'))


























