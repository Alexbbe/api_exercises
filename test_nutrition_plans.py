from main import WengerApi
import pytest

@pytest.fixture()
def setup():
    """
     1. return object login1 of class WengerApi, that is used for tests.
     2. Delete all the nutrition plans after a test is executed.
     3. Verify the nutrition plans were deleted.
    """
    print("Setting up!!")
    login1 = WengerApi("balbaealexandru@gmail.com",
                       "12345678abc", "Token 5c4f8bef9dd4e6d72f0868971ac142cca0157431")
    yield login1
    # req = login1.delete_all_nutrition_plans()
    # assert req


class TestClass:
    #Positive tests
    def test_add_nutrition_plan(self,setup):
        """
        1. Add a nutrition plan
        2. Test if the nutrition plan was added.
        """
        add_plan = setup.create_nutrition_plan('Description')
        assert add_plan[0]

    def test_add_meal_nutrition_plan(self,setup):
        """
        1. Add a nutrition plan.
        2. Test if the nutrition plan was added.
        3. Add a meal for the added nutrition plan.
        4. Verify the meal was added.
        """
        add_plan = setup.create_nutrition_plan('Description42')
        assert add_plan[0]
        add_meal = setup.create_meals_for_nutrition_plans(add_plan[0].json().get('id'), time='08:05:43')
        assert add_meal[0]

    def test_add_item_for_meal(self,setup):
        """
        1. Add a nutrition plan.
        2. Test if the nutrition plan was added.
        3. Add a meal for the added nutrition plan.
        4. Verify the meal was added.
        5. Add an item for the added meal.
        6. Verify the item was added.
        """
        add_plan = setup.create_nutrition_plan('Description56')
        assert add_plan[0]
        add_meal = setup.create_meals_for_nutrition_plans(add_plan[0].json().get('id'))
        assert add_meal[0]
        ingredient = str(setup.get_random_id('ingredient'))
        add_item = setup.add_meal_item(meal = add_meal[0].json().get('id'), ingredient=ingredient, amount=400)
        assert add_item[0]

    def test_add_multiple_nutriton_plans(self,setup):
        """
        1. Add multiple nutrition plans
        2. Verify all nutrition plans were added.
        """
        assert all(setup.create_nutrition_plan(f"Nutrition_plan{i}") for i in range(0,20))

    def test_add_multiple_meals(self, setup):
        """
        1. Added a nutrition plan
        2. Verify the nutrition plan was added
        3. For the added nutrition plan add multiple meals
        4. Verify all meals were added successfully
        """
        add_plan = setup.create_nutrition_plan('Description3')
        assert add_plan[0]
        for i in range(20):
            assert (setup.create_meals_for_nutrition_plans(plan=add_plan[0].json().get('id')))

    def test_add_multiple_items_per_meal(self, setup):
        """
        1. Add a nutrition plan.
        2. Test if the nutrition plan was added.
        3. Add a meal for the added nutrition plan.
        4. Verify the meal was added.
        5. For the added meal, add multiple items.
        6. Verify all items were added successfully
        """
        add_plan = setup.create_nutrition_plan('Description5')
        assert add_plan[0]
        add_meal = setup.create_meals_for_nutrition_plans(add_plan[0].json().get('id'))
        assert add_meal[0]
        for i in range(20):

            assert (setup.add_meal_item(meal=add_meal[0].json().get('id'), ingredient='11206', amount=350))

    def test_delete_meal_from_nutrition_plan(self,setup):
        """
        1. Add a nutrition plan.
        2. Verify the nutrition plan was added.
        3. Add a meal for the added nutrition plan.
        4. Verify the meal was added.
        5. Delete the added meal.
        6. Verify the meal was deleted successfully.
        """
        add_plan = setup.create_nutrition_plan('Description42')
        assert add_plan[0]
        add_meal = setup.create_meals_for_nutrition_plans(add_plan[0].json().get('id'))
        assert add_meal[0]
        assert setup.delete_nutrition_plan(nutrtion_plan_id=add_plan[0].json().get('id'), meal_id=add_meal[0].json().get('id'))

    def test_delete_item_from_meal(self,setup):
        """
        1. Add a nutrition plan.
        2. Verify the nutrition plan was added.
        3. Add a meal for the added nutrition plan.
        4. Verify the meal was added.
        5. Add an item for the added meal.
        6. Verify the item was added.
        7. Delete the added item.
        8. Verify the item was deleted.
        """
        add_plan = setup.create_nutrition_plan('Description43')
        assert add_plan[0]
        add_meal = setup.create_meals_for_nutrition_plans(add_plan[0].json().get('id'))
        assert add_meal[0]
        add_item = setup.add_meal_item(meal=add_meal[0].json().get('id'), ingredient='11206', amount=400)
        assert add_item[0]
        assert setup.delete_nutrition_plan(nutrtion_plan_id=add_plan[0].json().get('id'), meal_id=add_meal[0].json().get('id'),
                                           item_id=add_item[0].json().get('id'))

    def test_delete_multiple_meals(self,setup):
        """
        1. Add a nutrition plan.
        2. Verify the plan was added.
        3. For the added nutrition plan add multiple meals.
        4. Verify all the meals were added
        5. Delete all added meals
        6. Verify all meals were deleted
        """
        add_plan = setup.create_nutrition_plan('Description3')
        assert add_plan[0]
        for i in range(20):
            assert (setup.create_meals_for_nutrition_plans(plan=add_plan[0].json().get('id')))
        assert (setup.delete_all_meals_from_nutrition_plan())

    def test_delete_multiple_items(self,setup):
        """
        1. Add a nutrition plan.
        2. Verify the plan wad added.
        3. Add meal for the added nutrition plan.
        4. Verify the meal was added.
        5. Add multiple items for the added meal.
        6. Verify all items were added.
        7. Delete the added items.
        8. Verify the items were deleted.
        """
        add_plan = setup.create_nutrition_plan('Description5')
        assert add_plan[0]
        add_meal = setup.create_meals_for_nutrition_plans(add_plan[0].json().get('id'))
        assert add_meal[0]
        for i in range(20):
            assert (setup.add_meal_item(meal=add_meal[0].json().get('id'), ingredient='11206', amount=350))
        assert (setup.delete_all_items_from_meal())

    def test_delete_nutrition_plan_with_meal_item_configured(self, setup):
        """
        1. Add a nutrition plan.
        2. Verify the plan was added.
        3. For the added plan add multiple meals.
        4. Verify the meals were added.
        5. For each of the added meals add multiple items.
        6. Verify the items were added.
        7. Delete the nutrition plan.
        8. Verify the added nutrition plan was deleted.
        """
        add_plan = setup.create_nutrition_plan('Description5')
        assert add_plan[0]
        for i in range (10):
            add_meal = setup.create_meals_for_nutrition_plans(add_plan[0].json().get('id'))
            assert add_meal
            for i in range(5):
                add_item = setup.add_meal_item(meal=add_meal[0].json().get('id'), ingredient='11206', amount=200)
                assert add_item

        delete_plan = setup.delete_nutrition_plan(nutrtion_plan_id=add_plan[0].json().get('id'))
        assert delete_plan

    # Negative tests
    @pytest.mark.parametrize(
        "time",["-10234","blabala","@!!!@!@!@#@@","25:0:","11:61"])
    def test_add_meal_nutrition_plan_bad_parameters(self, setup, time):
        """
        1. Add nutrition plan.
        2. Verify the nutrition plan were added.
        3. Add a meal and provide invalid value for time parameter.
        4. Verify the meal couldn't be added.
        """
        #add nutrition plan
        add_plan = setup.create_nutrition_plan('Description')
        assert add_plan[0]
        #add meal wrong parameteers
        add_meal = setup.create_meals_for_nutrition_plans(plan=add_plan[0].json().get('id'),time=time)

        assert add_meal[0] is False

    @pytest.mark.parametrize(
        "ingredient,amount",[("11206","buzzuzuz"),("11206","@#@#@#@#@"),("11206","1111111111111111111111"),
                             ("11206","sdadsadsadafdfdshfhfbjhdsbfhdsbfhsbfujhsbfhsbfujhbfhsbfhsbfhsbfhsbfds"),
                             ("11206","100g"),("11206","10o")])
    def test_add_item_invalid_values(self, setup, ingredient, amount):
        """
        1. Add a nutrition plan.
        2. Test if the nutrition plan was added.
        3. Add a meal for the added nutrition plan.
        4. Verify the meal was added.
        5. Add an item for the added meal and provide invalid values for ingredient and amount.
        6. Verify the item couldn't be added.
        """
        #add nutrition plan
        add_plan = setup.create_nutrition_plan('Description',)
        assert add_plan[0]
        #add meal
        add_meal = setup.create_meals_for_nutrition_plans(add_plan[0].json().get('id'))
        assert add_meal[0]
        #add item invalid values
        add_item = setup.add_meal_item(meal=add_meal[0].json().get('id'), ingredient=ingredient, amount=amount)
        assert add_item[0] is False

    def test_add_meal_for_nonexisting_plan(self, setup):
        """
        1. Add a nutrition plan.
        2. Test if the nutrition plan was added.
        3. Add a meal for the added non-existent nutrition plan.
        4. Verify the meal wasn't added.
        """
        #create multiple nutrition plans
        add_plan = setup.create_nutrition_plan('Description')
        assert add_plan[0]
        #create meal for nonexisting nutrition plan
        id_plan = str(setup.get_random_num_outside_list('nutritionplan'))
        add_meal = setup.create_meals_for_nutrition_plans(plan=id_plan)
        assert add_meal[0] is False

    def test_add_item_for_nonexisting_meal(self, setup):
        """
        1. Add nutrition plan.
        2. Verify the nutrition plan was added.
        3. Add meal for nutrition plan.
        4. Verify the meal was added.
        5. Add item for an non-existent meal from the added nutrition plan.
        6. Verify the item couldn't be added.
        """
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

    def test_delete_non_existent_plan(self, setup):
        """
        1. Add nutrition plan.
        2. Verify the nutrition plan was added.
        3. Delete a non existent nutrition plan.
        4. Verify the non existent nutrition plan couldn't be deleted
        """
        #create nutrition plan
        add_plan = setup.create_nutrition_plan('Description')
        assert add_plan[0]
        #delete plan
        plan_id = setup.get_random_num_outside_list('nutritionplan')
        delete_plan = setup.delete_nutrition_plan(nutrtion_plan_id=plan_id)
        assert delete_plan[0] is False

    def test_delete_non_existent_meal(self, setup):
        """
        1. Add nutrition plan.
        2. Verify the nutrition plan was added.
        3. Add a meal for the nutrition plan.
        4. Verify the meal was added.
        5. Delete a non existent meal from the nutrition plan.
        6. Verify the meal couldn't be deleted.
        """
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

    def test_delete_non_existent_item(self, setup):
        """
        1. Add nutrition plan.
        2. Verify the nutrition plan was added.
        3. Add a meal for the nutrition plan.
        4. Verify the meal was added.
        5. Add an item for the added meal.
        6. Delete an non existent item.
        7. Verify the item couldn't be deleted.
        """
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


