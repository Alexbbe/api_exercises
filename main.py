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
        print("The login post cookies are: ")
        print(req.cookies)
        print(req.content)
        # print("The login get cookies are: ")
        # print(login_get.cookies

    def get_req(self, object, offset=None, limit=None):

        g1 = requests.get('https://wger.de/api/v2/')
        url = g1.json().get(object)
        if url != None:
            req1 = requests.get(url=url, headers=self.header)
            count = req1.json().get('count')
            url1 = url + f"?limit={count}&offset=0"
            g = requests.get(url=url1, headers=self.header)
            if g.status_code == 200:
                return g.json()
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
                return req, f'The post request for {object} was done succusefuly'
            else:
                return {req.status_code}, 'Error  {req.status_code}'
        else:
            return False, 'Invalid url'

    def delete_req(self,object, id):

        g1 = requests.get('https://wger.de/api/v2/')
        url1 = g1.json().get(object)
        if url1 != None:
            url = f"{url1}/{id}"
            req = requests.delete(url=url, headers=self.header)
            if req.status_code not in (200,202,204):
                return req.status_code, f"The delete for id {id} couldn't be performed"
            return True, f"The delete for {object} with id {id} was performed" \
                         f"succesfully! Status code is {req.status_code}"
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
        workouts_list = workouts.get('results')
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
        for workout in workouts.get('results',[]):
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

    def get_nutrition_plans_list(self):

        a = self.parse_toml(toml_file='toml_file.toml')
        dict1 = a['nutrition_plans']
        return dict1

    def get_nutrition_plans_meals(self,nutrition_plan):
        b = self.get_nutrition_plans_list()
        dict = b[nutrition_plan]["meals"]
        return dict

    def get_items_from_meals(self,nutrition_plan, meal):

        list_of_meals = self.get_nutrition_plans_meals(nutrition_plan)
        dict = list_of_meals[meal]["items"]
        return dict

    def add_nutrition_plans(self):

        dict1 = self.get_nutrition_plans_list()
        list_of_description = list(dict1.keys())
        for nutrition_plan in list_of_description:
            self.create_nutrition_plan(nutrition_plan)

            if "meals" not in dict1[nutrition_plan]:
                print("There are no meals to be added")
            else:
                dict2 = self.get_nutrition_plans_meals(nutrition_plan)
                list1 = list(dict2.keys())
                a = len(list1)
                nutrition_plans = self.get_req('nutritionplan')

                for plan in nutrition_plans["results"]:
                    if plan["description"] == nutrition_plan:
                        for i in range(a):
                            self.create_meals_for_nutrition_plans(plan["id"])
                        meals = self.get_req('meal')
                        list_of_meal_ids = list()
                        for meal in meals['results']:
                            if meal['plan'] == plan['id']:
                                list_of_meal_ids.append(meal['id'])


                meal_id_name = zip(list_of_meal_ids, list1)
                meal_id_name_set = set(meal_id_name)
                print(meal_id_name_set)

                for meal in meal_id_name_set:
                    if "items" not in dict2[meal[1]]:
                        print ("There are no items in this meal")
                    else:
                        dict3 = self.get_items_from_meals(nutrition_plan,meal[1])
                        for elem in dict3.values():
                            meal_req = meal[0]
                            amount_req = elem['amount']
                            ingredient_req = elem['ingredient']
                            self.add_meal_item(meal_req,ingredient_req,amount_req)





























