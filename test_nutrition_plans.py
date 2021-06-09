from main import WengerApi
import pytest

@pytest.fixture()
def setup():
    print("Setting up!!")
    login1 = WengerApi("balbaealexandru@gmail.com",
                       "12345678abc", "Token 5c4f8bef9dd4e6d72f0868971ac142cca0157431")
    yield login1
    # req = login1.delete_all_nutrition_plans()
    # assert req


class TestClass():
    #Positive tests
    def test_add_nutrition_plan(self,setup):
        add_plan = setup.create_nutrition_plan('Description')
        assert add_plan[0]

    def test_add_meal_nutrition_plan(self,setup):
        add_plan = setup.create_nutrition_plan('Description42')
        assert add_plan[0]
        add_meal = setup.create_meals_for_nutrition_plans(add_plan[0].json().get('id'))
        assert add_meal[0]

    def test_add_item_for_meal(self,setup):
        add_plan = setup.create_nutrition_plan('Description56')
        assert add_plan[0]
        add_meal = setup.create_meals_for_nutrition_plans(add_plan[0].json().get('id'))
        assert add_meal[0]
        ingredient = str(setup.get_random_id('ingredient'))
        add_item = setup.add_meal_item(meal = add_meal[0].json().get('id'),ingredient=ingredient,amount=400)
        assert add_item[0]


    def test_add_multiple_nutriton_plans(self,setup):
        assert all(setup.create_nutrition_plan(f"Nutrition_plan{i}") for i in range(0,20))

    def test_add_multiple_meals(self,setup):
        add_plan = setup.create_nutrition_plan('Description3')
        assert add_plan[0]
        for i in range(20):
            assert (setup.create_meals_for_nutrition_plans(plan=add_plan[0].json().get('id')))


    def test_add_multiple_items_per_meal(self,setup):
        add_plan = setup.create_nutrition_plan('Description5')
        assert add_plan[0]
        add_meal = setup.create_meals_for_nutrition_plans(add_plan[0].json().get('id'))
        assert add_meal[0]
        for i in range(20):

            assert (setup.add_meal_item(meal=add_meal[0].json().get('id'),ingredient='11206',amount=350))


    def test_delete_meal_from_nutrition_plan(self,setup):
        add_plan = setup.create_nutrition_plan('Description42')
        assert add_plan[0]
        add_meal = setup.create_meals_for_nutrition_plans(add_plan[0].json().get('id'))
        assert add_meal[0]
        assert setup.delete_nutrition_plan(nutrtion_plan_id=add_plan[0].json().get('id'),meal_id=add_meal[0].json().get('id'))


    def test_delete_item_from_meal(self,setup):
        add_plan = setup.create_nutrition_plan('Description43')
        assert add_plan[0]
        add_meal = setup.create_meals_for_nutrition_plans(add_plan[0].json().get('id'))
        assert add_meal[0]
        add_item = setup.add_meal_item(meal=add_meal[0].json().get('id'), ingredient='11206', amount=400)
        assert add_item[0]
        assert setup.delete_nutrition_plan(nutrtion_plan_id=add_plan[0].json().get('id'),meal_id=add_meal[0].json().get('id'),
                                           item_id=add_item[0].json().get('id'))


    def test_delete_multiple_nutrition_plans(self,setup):
        assert all(setup.create_nutrition_plan(f"Nutrition_plan{i}") for i in range(0, 20))
        assert (setup.delete_all_nutrition_plans())


    def test_delete_multiple_meals(self,setup):
        add_plan = setup.create_nutrition_plan('Description3')
        assert add_plan[0]
        for i in range(20):
            assert (setup.create_meals_for_nutrition_plans(plan=add_plan[0].json().get('id')))
        assert (setup.delete_all_meals_from_nutrition_plan())


    def test_delete_multiple_items(self,setup):
        add_plan = setup.create_nutrition_plan('Description5')
        assert add_plan[0]
        add_meal = setup.create_meals_for_nutrition_plans(add_plan[0].json().get('id'))
        assert add_meal[0]
        for i in range(20):
            assert (setup.add_meal_item(meal=add_meal[0].json().get('id'),ingredient='11206',amount=350))
        assert (setup.delete_all_items_from_meal())


    def test_delete_nutrition_plan_with_meal_item_configured(self,setup):
        add_plan = setup.create_nutrition_plan('Description5')
        assert add_plan[0]
        for i in range (10):
            add_meal = setup.create_meals_for_nutrition_plans(add_plan[0].json().get('id'))
            assert add_meal
            for i in range(5):
                add_item = setup.add_meal_item(meal=add_meal[0].json().get('id'),ingredient='11206',amount=200)
                assert add_item

        delete_plan =  setup.delete_nutrition_plan(nutrtion_plan_id=add_plan[0].json().get('id'))
        assert delete_plan


    # Negative tests
    @pytest.mark.parametrize(
        "time",["-10234","blabala","@!!!@!@!@#@@","25:0:","11:61"])
    def test_add_meal_nutrition_plan_bad_parameters(self,setup,time):
        #add nutrition plan
        add_plan = setup.create_nutrition_plan('Description')
        assert add_plan[0]
        #add meal wrong parameteers
        add_meal = setup.create_meals_for_nutrition_plans(plan=add_plan[0].json().get('id'),time=time)

        assert add_meal[0] is False

    @pytest.mark.parametrize(
        "ingredient,amount",[("11206","buzzuzuz"),("11206","@#@#@#@#@"),("11206","1111111111111111111111"),
                             ("11206","sdadsadsadafdfdshfhfbjhdsbfhdsbfhsbfujhsbfhsbfujhbfhsbfhsbfhsbfhsbfds"),
                             ("11206","100g"),("11206","10o")]
    )
    def test_add_item_invalid_values(self,setup,ingredient,amount):
        #add nutrition plan
        add_plan = setup.create_nutrition_plan('Description',)
        assert add_plan[0]
        #add meal
        add_meal = setup.create_meals_for_nutrition_plans(add_plan[0].json().get('id'))
        assert add_meal[0]
        #add item invalid values
        add_item = setup.add_meal_item(meal=add_meal[0].json().get('id'), ingredient=ingredient, amount=amount)
        assert add_item[0] is False



    def test_add_meal_for_nonexisting_plan(self,setup):
        #create multiple nutrition plans
        add_plan = setup.create_nutrition_plan('Description')
        assert add_plan[0]
        #create meal for nonexisting nutrition plan
        id_plan = str(setup.get_random_num_outside_list('nutritionplan'))
        add_meal = setup.create_meals_for_nutrition_plans(plan=id_plan)
        assert add_meal[0] is False


    def test_add_item_for_nonexisting_meal(self,setup):
        # create add plan
        add_plan = setup.create_nutrition_plan('Description')
        assert add_plan[0]
        #create add meal
        add_meal = setup.create_meals_for_nutrition_plans(add_plan[0].json().get('id'))
        assert add_meal[0]
        #get random invalid meal id
        id_meal = str(setup.get_random_num_outside_list('meal'))
        #create item for inexistent meal
        add_item = setup.add_meal_item(meal=id_meal, ingredient='11206', amount='buzz')
        assert add_item[0] is False


    def test_delete_non_existent_plan(self,setup):
        #create nutrition plan
        add_plan = setup.create_nutrition_plan('Description')
        assert add_plan[0]
        #delete plan
        plan_id = setup.get_random_num_outside_list('nutritionplan')
        delete_plan = setup.delete_nutrition_plan(nutrtion_plan_id=plan_id)
        assert delete_plan[0] is False


    def test_delete_non_existent_meal(self,setup):
        #create nutrition plan
        add_plan = setup.create_nutrition_plan('Description')
        assert add_plan[0]
        #create meal
        add_meal = setup.create_meals_for_nutrition_plans(add_plan[0].json().get('id'))
        assert add_meal[0]
        #delete meal that don't exists
        meal_id = setup.get_random_num_outside_list(object='meal')
        delete_meal =  setup.delete_nutrition_plan(nutrtion_plan_id=add_plan[0].json().get('id'),meal_id=meal_id)
        assert delete_meal[0] is False



    def test_delete_non_existent_item(self,setup):
        #create nutrition plan
        add_plan = setup.create_nutrition_plan('Description')
        assert add_plan[0]
        #create meal
        add_meal = setup.create_meals_for_nutrition_plans(add_plan[0].json().get('id'))
        assert add_meal[0]
        #create item
        add_item = setup.add_meal_item(meal=add_meal[0].json().get('id'), ingredient='11206', amount=400)
        assert add_item[0]
        #get item id that doesn't exists
        item_id = setup.get_random_num_outside_list('mealitem')
        delete_item = setup.delete_nutrition_plan(nutrtion_plan_id=add_plan[0].json().get('id'),
                                                  meal_id=add_meal[0].json().get('id'),item_id=item_id)
        assert delete_item[0] is False


