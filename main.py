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
        data = {"username": {self.username}, "password": {self.password}, "submit": "Login"}
        url = 'https://wger.de/en/user/login'
        login_get = requests.get(url=url, headers=self.header)
        self.header['X-CSRFToken'] = login_get.cookies["csrftoken"]
        self.header['Referer'] = 'https://wger.de/en/user/login'
        session_id = login_get.cookies["sessionid"]
        csrf_token = login_get.cookies["csrftoken"]
        cookie_full = f"csrftoken={csrf_token}; sessionid={session_id}"
        self.header["Cookie"] = cookie_full
        req = requests.post(url=url, data=data, headers=self.header)
        print("The login post cookies are: ")
        print(req.cookies)
        print(req.content)
        # print("The login get cookies are: ")
        # print(login_get.cookies)

    def get_req(self, object):
        #get the object for ULR
        g1 = requests.get('https://wger.de/api/v2/')
        g = requests.get(url=g1.json()[object], headers=self.header)
        if g.status_code == 200:
            return g.json()
        else:
            return "Couldn't make the request"

    def post_req(self,object, data):

        g1 = requests.get('https://wger.de/api/v2/')
        url1 = g1.json().get(object)
        if url1 != None:
            req = requests.post(url=url1,data=data,headers=self.header)
            if req.status_code == 201:
                return f'The post request for {object} was done succusefuly'
            else:
                return f'Error {req.status_code}'
        else:
            return 'Invalid url'



    def delete_req(self,object, id):
        g1 = requests.get('https://wger.de/api/v2/')
        url1 = g1.json().get(object)
        url1 = f"{url1}/{id}"
        if url1 != None:
            req = requests.delete(url=url1, headers=self.header)
            return req




    # def get_ingredients(self, limit=20, offset=0):
    #     url = f'https://wger.de/api/v2/ingredient/?limit={limit}&offset={offset}'
    #     r = requests.get(url=url)
    #     if r.status_code == 200:
    #         return r.json()['results']
    #     else:
    #         print("Request Error!")

    def parse_toml(self, toml_file):
        with open(toml_file) as file:
            data = file.read()
        parsed_toml = toml.loads(data)
        return parsed_toml

    # def get_nutrition_plans_list(self):
    #     a = self.parse_toml(toml_file='toml_file.txt')
    #     return a['nutrition_plans']
    #
    # def get_nutrition_plans_meals(self):
    #     b = self.get_nutrition_plans_list()
    #     list1 = list()
    #     list2 = list()
    #     for elem in b:
    #         list1.append(elem)
    #     for elem1 in list1:
    #         list2.append(b[elem1]['meals'])
    #     return list2
    #
    # def get_items_from_meals(self):
    #     list_of_meals = self.get_nutrition_plans_meals()
    #     list1 = list()



    def create_weight_entry(self,date,value):
        data = {
            "date":date,
            "weight":value,
        }
        return self.post_req('weightentry',data)


    def create_nutrition_plan(self,description=None):
        my_date = date.today()
        if description == None:

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

        self.post_req('workout',data)

    def add_day(self,training,description,day):
        data ={
            "training":training,
            "description":description,
            "day":day
        }
        self.post_req('day',data)


    def add_exercise(self,exerciseday,sets,order):
        data = {
            'exerciseday':exerciseday,
            'sets':sets,
            'order':order
        }

        self.post_req('set',data)

    def setting_exercise_set(self, exercise,repetition_unit,reps,weight,weight_unit,rir):

        data = {
            'exercise':exercise,
            'repetition_unit':repetition_unit,
            'reps':reps,
            'weight':weight,
            'weight_unit':weight_unit,
            'rir':rir,
        }

        self.post_req('setting',data)


    def add_schedule(self,name,start_date,is_active,is_loop):
        data = {
            'name':name,
            'start_date':start_date,
            'is_active':is_active,
            'is_loop':is_loop

        }
        self.post_req('schedule',data)


    def add_workout_to_schedule(self,schedule,workout,duration):
        data = {
            'schedule':schedule,
            'workout':workout,
            'duration':duration
        }

        self.post_req('schedulestep',data)


    def delete_workout(self, id):
        workouts = self.get_req('workout')
        list_of_id = list()
        for workout in workouts['results']:
            list_of_id.append(workout['id'])

        if id in list_of_id:
            self.delete_req('workout',id)
            return f"Workout with id {id} was deleted successfully "
        else:
            return f"Workout with id {id} was not found!"




    def delete_exercise(self,id):
        exercises = self.get_req('set')
        list_of_id = list()
        for exercise in exercises['results']:
            list_of_id.append(exercise['id'])

        if id in list_of_id:
            self.delete_req('set',id)
            return f"Exercise with id {id} was deleted successfully "
        else:
            return f"Exercise with id {id} was not found!"



