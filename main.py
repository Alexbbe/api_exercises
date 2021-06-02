import requests
from pprint import pprint
import json
import pyramid.httpexceptions as exc
from datetime import date
import calendar
import toml
from pprint import pprint


class WengerApi:

    headers1 = {'Accept': 'application/json'
               }

    def __init__(self, username, password,token):
        self.username = username
        self.password = password
        self.token = token
        self.header = WengerApi.headers1.copy()
        self.header["Authorization"] = token
        self.login()

    def login(self):
        data = {"username": {self.username},
                "password": {self.password},
                "submit": "Login"}
        url = 'https://wger.de/en/user/login'
        login_get = requests.get(url=url, headers=self.header)
        self.header['X-CSRFToken'] = login_get.cookies["csrftoken"]
        self.header['Referer'] = url
        session_id = login_get.cookies.get("sessionid")
        csrf_token = login_get.cookies.get("csrftoken")
        cookie_full = f"csrftoken={csrf_token}; sessionid={session_id}"
        self.header["Cookie"] = cookie_full
        req = requests.post(url=url, data=data, headers=self.header)
        if req.status_code in  [200,201]:
            return req, "The login was performed successfuly"
        else:
            return False, f"Error {req.status_code}"

    def get_req(self,object):
        g1 = requests.get('https://wger.de/api/v2/')
        url = g1.json().get(object)
        if url != None:
            req1 = requests.get(url=url, headers=self.header)
            count = req1.json().get('count')
            url1 = url + f"?limit={count}&offset=0"
            g = requests.get(url=url1, headers=self.header)
            if g.status_code == 200:
                return g.json(), f"The get request for {object} was performed successfully"
            else:
                return g.status_code, "Couldn't make the request!"
        else:
            return False, 'Invalid url'

    def post_req(self,object, data):

        g1 = requests.get('https://wger.de/api/v2/')
        url1 = g1.json().get(object)

        if url1 != None:
            req = requests.post(url=url1,data=data,headers=self.header)
            if req.status_code == 201:
                return req, f'The post request for {object} was done successfully'
            else:
                return {req.status_code}, 'Error  {req.status_code}'
        else:
            return False, 'Invalid url'

    def name_to_id(self, name, object):
        req = self.get_req(object)
        for item in req[0].get('results', []):
            if item.get('name') == name:
                return item.get('id'), f"The id for {name} was provided successfully"
            else:
                return False, f"The item with name {name} doesn't have id"


    def delete_req(self,object, id):

        g1 = requests.get('https://wger.de/api/v2/')
        url1 = g1.json().get(object)
        if url1 != None:
            url = f"{url1}/{id}"
            req = requests.delete(url=url, headers=self.header)
            if req.status_code not in (200,202,204):
                return req.status_code, f"The delete for id {id} couldn't be performed"
            return req, f"The delete for {object} with id {id} was performed" \
                         f"successfully! Status code is {req.status_code}"
        else:
            return False, "Error! The URL doesn't exists!"

    def create_weight_entry(self,date,value):

        data = {
            "date":date,
            "weight":value,
        }

        return self.post_req('weightentry',data)

    def create_nutrition_plan(self,description=None):

        if description == None:
            my_date = date.today()
            description = calendar.day_name[my_date.weekday()]
        data = {
            'description': description
        }
        return self.post_req('nutritionplan', data)

    def create_meals_for_nutrition_plans(self,plan):

        data = {
            'plan': plan
        }
        return self.post_req('meal',data)

    def add_meal_item(self,meal,ingredient,amount):

        data = {
            'meal':meal,
            'ingredient':ingredient,
            'amount':amount
        }

        return self.post_req('mealitem',data)

    def add_workout_day(self,name,description):

        data = {

            "name":name,
            "description":description
        }

        return self.post_req('workout',data)

    def add_day(self,training,description,day):

        workouts = self.get_req('workout')
        list_of_workout = list()
        workouts_list = workouts[0].get('results')
        if workouts_list != None:

            for workout in workouts_list:
                list_of_workout.append(workout["id"])

        if training not in list_of_workout:
            return False, f"The training with id {training} doesn't exists!"
        data ={

            "training":training,
            "description":description,
            "day":day
        }
        return self.post_req('day',data)

    def add_exercise(self,exerciseday,sets,order):

        data = {
            'exerciseday': exerciseday,
            'sets': sets,
            'order': order
        }

        return self.post_req('set',data)

    def setting_exercise_set(self, set, exercise,repetition_unit,reps,weight,weight_unit,rir):

        data = {
            'set':set,
            'exercise':exercise,
            'repetition_unit':repetition_unit,
            'reps':reps,
            'weight':weight,
            'weight_unit':weight_unit,
            'rir':rir,
        }

        return self.post_req('setting',data)

    def add_schedule(self,name,start_date,is_active,is_loop):

        data = {
            'name':name,
            'start_date':start_date,
            'is_active':is_active,
            'is_loop':is_loop

        }
        return self.post_req('schedule',data)

    def add_workout_to_schedule(self,schedule,workout,duration):

        data = {
            'schedule':schedule,
            'workout':workout,
            'duration':duration
        }

        return self.post_req('schedulestep',data)

    def delete_workout(self, id=None):

        workouts = self.get_req('workout')
        list_of_id = list()
        for workout in workouts[0].get('results',[]):
            list_of_id.append(workout.get('id'))
        if id is not None:
            if id in list_of_id:
                req = self.delete_req('workout',id)
                return req, f"Workout with id {id} was deleted successfully "
            else:
                return False, f"Workout with id {id} was not found!"
        else:
            if len(list_of_id) != 0:
                undeleted_workouts = list()
                for id1 in list_of_id:
                    req2 = self.delete_req('workout',id1)
                    if req2 is False:
                        undeleted_workouts.append(id1)
                if len(undeleted_workouts) == 0:
                    return True, "All existing workouts has been deleted!"
                else:
                    return undeleted_workouts, f"The following workouts couldn't be deleted {undeleted_workouts}"
            else:
                return False, "There are no workouts to be deleted"

    def delete_nutrition_plans(self):
        nutrition_plans = self.get_req('nutritionplan')
        for nutrition_plan in nutrition_plans.get('results',[]):
            self.delete_req('nutritionplan',nutrition_plan.get('id'))

    def delete_exercise(self, workout_id = None, day_id = None, exercise_id = None):
        if workout_id is not None:
            list_of_workouts = self.get_req('workout')
            list_of_workouts_ids = list()
            for workout in list_of_workouts.get('results',[]):
                list_of_workouts_ids.append(workout.get('id'))

            if day_id is not None:
                list_of_days = self.get_req('day')
                list_of_days_id = list()
                for day in list_of_days.get('results',[]):
                    list_of_days_id.append(day.get('id'))

                if exercise_id is not None:
                    list_of_exercises = self.get_req('set')
                    list_of_exercises_ids = list()
                    for exercise in list_of_exercises.get('results',[]):
                        list_of_exercises_ids.append(exercise.get('id'))
                    if exercise_id not in list_of_exercises_ids:
                        return False, f"The exercise with id {exercise_id} doesn't exists in " \
                                      f"day {day_id} and workout {workout_id}"
                    else:
                        req1 = self.delete_req('set',exercise_id)
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



    #TOML part



    def parse_toml(self, toml_file):
        with open(toml_file) as file:
            data = file.read()
        parsed_toml = toml.loads(data)
        return parsed_toml

    def get_nutrition_plans_list(self,toml_file):
        a = self.parse_toml(toml_file=toml_file)
        dict1 = a.get('nutrition_plans')
        return dict1

    def get_nutrition_plans_meals(self,nutrition_plan,toml_file):
        b = self.get_nutrition_plans_list(toml_file)
        dict = b.get(nutrition_plan,{}).get("meals",{})
        return dict

    def get_items_from_meals(self,nutrition_plan, meal,toml_file):
        list_of_meals = self.get_nutrition_plans_meals(nutrition_plan,toml_file)
        dict = list_of_meals.get(meal,{}).get("items",{})
        return dict

    def get_workouts(self,file):
        a = self.parse_toml(toml_file=file)
        dict = a.get('workouts',{})
        return dict

    def get_workout_days(self,file, workout=None):
            a = self.get_workouts(file)
            dict = a.get(workout,{}).get("days",{})
            return dict


    def get_exercises(self,file,workout=None,day=None):
        a = self.get_workout_days(file=file,workout=workout)
        dict = a.get(day,{}).get('exercises')
        return dict

    def get_exercises_settings(self,workout,day,exercise,file):
        a = self.get_exercises(workout=workout,day=day,file=file)
        dict = a.get(exercise,{}).get('settings',{})
        return dict

    def get_setting_informations(self,workout,day,exercise,setting,file):
        a = self.get_exercises_settings(workout,day,exercise,file)
        dict = a.get(setting,{})
        return dict


    def add_nutrition_plans_toml(self,toml_file_plans):
        parsed_toml = self.parse_toml(toml_file=toml_file_plans)
        if "nutrition_plans" in parsed_toml:
            nutrition_plans_dict = self.get_nutrition_plans_list(toml_file_plans)
            for nutrition_plan in nutrition_plans_dict:
                add_plan = self.create_nutrition_plan(description=nutrition_plan)
                nutrtion_plan_id = add_plan[0].json().get('id')
                if 'meals' in nutrition_plans_dict[nutrition_plan]:
                    meals_dict = self.get_nutrition_plans_meals(nutrition_plan,toml_file_plans)
                    self.add_meals_toml(meals_dict, nutrtion_plan_id, nutrition_plan, toml_file_plans)


    def add_meals_toml(self,meals_dict,nutrition_plan_id,nutrition_plan,toml_file_planes):

        for meal in meals_dict:
            add_meal = self.create_meals_for_nutrition_plans(nutrition_plan_id)
            meal_id = add_meal[0].json().get('id')
            print(meal_id)

            if 'items' in meals_dict.get(meal):
                items_dict = self.get_items_from_meals(nutrition_plan=nutrition_plan,meal=meal,toml_file=toml_file_planes)
                self.add_item_toml(items_dict,meal_id)


    def add_item_toml(self,items_dict,meal_id):
        for item in items_dict:
            self.add_meal_item(meal_id,items_dict.get(item,{}).get('ingredient')
                                           ,items_dict.get(item,{}).get('amount'))


    def add_workouts_toml_file(self,file):
        toml_parsed_file = self.parse_toml(file)
        if "workouts" in toml_parsed_file:
            toml_workouts = self.get_workouts(file=file)
            for workout in toml_workouts:
                req = self.add_workout_day(toml_workouts.get(workout,{}).get('name'),
                                                   toml_workouts.get(workout,{}).get('description'))
                workout_id = req[0].json().get('id')
                if "days" in toml_workouts.get(workout).keys():
                    toml_days = self.get_workout_days(file=file,workout=workout)
                    self.add_days_for_workouts_toml(workout_id=workout_id,toml_days=toml_days,workout=workout,file=file)


    def add_days_for_workouts_toml(self,workout_id,toml_days,workout,file):
        for day in toml_days:
            add_day1 = self.add_day(training=workout_id,description=toml_days.get(day,{}).get("description"),
                                    day=toml_days.get(day,{}).get('day'))
            day_id = add_day1[0].json().get('id')

            if "exercises" in toml_days.get(day).keys():
                toml_exercise = self.get_exercises(file=file,workout=workout,day=day)
                self.add_exercise_per_day_toml(exercise_toml=toml_exercise,day_id=day_id,
                                               workout=workout,day=day,file=file)


    def add_exercise_per_day_toml(self,exercise_toml,day_id,workout,day,file):
        for exercise in exercise_toml:
            add_exercise = self.add_exercise(day_id,sets=exercise_toml.get(exercise,{}).get('sets'),order=1)
            exercise_id = add_exercise[0].json().get('id')
            if 'settings' in exercise_toml.get(exercise).keys():
                toml_settings = self.get_exercises_settings(workout=workout, day=day, exercise=exercise, file=file)
                self.add_settings_per_exercise(toml_settings,exercise_id)



    def add_settings_per_exercise(self,toml_settings,exercise_id):
        for setting in toml_settings:
            self.setting_exercise_set(              set=exercise_id
                                                    ,exercise=toml_settings.get(setting,{}).get('exercise'),
                                                    repetition_unit=toml_settings.get(setting,{}).get('repetition_unit')
                                                    ,reps=toml_settings.get(setting,{}).get('reps')
                                                    ,weight=toml_settings.get(setting,{}).get('weight')
                                                    ,weight_unit=toml_settings.get(setting,{}).get('weight_unit')
                                                    ,rir=toml_settings.get(setting,{}).get('rir'))



























