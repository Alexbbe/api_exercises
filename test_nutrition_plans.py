from main import WengerApi
import pytest

@pytest.fixture(scope='module')
def setup():
    print("Setting up!!")
    login1 = WengerApi("balbaealexandru@gmail.com",
                       "12345678abc", "Token 5c4f8bef9dd4e6d72f0868971ac142cca0157431")
    yield login1
    login1.delete_all_nutrition_plans()

@pytest.fixture()
def add_nutrition_plan(setup):
    req = setup.create_nutrition_plan('Description')
    return req[0]

@pytest.fixture()
def add_meal_for_nutrition_plan(setup,add_nutrition_plan):
    req = setup.create_meals_for_nutrition_plans(add_nutrition_plan.json().get('id'))
    return req[0]

@pytest.fixture()
def add_item_for_meal_nutrition_plan(setup,add_meal_for_nutrition_plan):
    req = setup.add_meal_item(add_meal_for_nutrition_plan.json().get('id'),'61972',333)
    return req[0]


@pytest.fixture()
def add_multiple_nutrition_plans(setup):
    for i in range(10):
        req = setup.create_nutrition_plan(f'Nutrition plan {i}')
        if req[0] == False:
            return False
    return True

@pytest.fixture()
def add_multiple_meals(setup,add_nutrition_plan):
    for i in range(10):
        req = setup.create_meals_for_nutrition_plans(add_nutrition_plan.json().get('id'))
        if req[0] == False:
            return False
    return True

@pytest.fixture()
def add_multiple_items(setup,add_meal_for_nutrition_plan):
    for i in range(10):
        req = setup.add_meal_item(add_meal_for_nutrition_plan.json().get('id'),'61972',i + 10)
        if req[0] == False:
            return False
    return True

@pytest.fixture()
def delete_nutrition_plan(setup,add_nutrition_plan):
    req = setup.delete_nutrition_plan(nutrtion_plan_id=add_nutrition_plan.json().get('id'))
    print(req)
    return req[0]

@pytest.fixture()
def delete_nutrition_plan(setup,add_nutrition_plan):
    req = setup.delete_nutrition_plan(nutrtion_plan_id=add_nutrition_plan.json().get('id'))
    print(req)
    return req[0]

@pytest.fixture()
def delete_nutrition_plan(setup,add_nutrition_plan):
    req = setup.delete_nutrition_plan(nutrtion_plan_id=add_nutrition_plan.json().get('id'))
    print(req)
    return req[0]

@pytest.fixture()
def delete_meal_from_nutrition_plan(setup,add_nutrition_plan,add_meal_for_nutrition_plan):
    req = setup.delete_nutrition_plan(nutrtion_plan_id=add_nutrition_plan.json().get('id')
                                      ,meal_id=add_meal_for_nutrition_plan.json().get('id'))
    return req[0]

@pytest.fixture()
def delete_item_from_meal(setup,
                          add_nutrition_plan,
                          add_meal_for_nutrition_plan,
                          add_item_for_meal_nutrition_plan):
    req = setup.delete_nutrition_plan(nutrtion_plan_id=add_nutrition_plan.json().get('id')
                                      , meal_id=add_meal_for_nutrition_plan.json().get('id'),
                                      item_id=add_item_for_meal_nutrition_plan.json().get('id'))
    return req[0]


@pytest.fixture()
def delete_multiple_nutrition_plans(setup,add_multiple_nutrition_plans):
    req = setup.delete_all_nutrition_plans()
    return req


@pytest.fixture()
def delete_multiple_meals(setup,add_multiple_meals):
    req = setup.delete_all_meals_from_nutrition_plan()
    return req

@pytest.fixture()
def delete_multiple_items(setup,add_multiple_items):
    req = setup.delete_all_items_from_meal()
    print(req)
    return req


@pytest.fixture()
def add_meal_nutrition_plan_bad_parameters(setup, add_nutrition_plan):
    req = setup.create_meals_for_nutrition_plans(add_nutrition_plan.json().get('id'),'gfgffg')
    return req[0]

@pytest.fixture()
def add_item_invalid_values(setup,add_meal_for_nutrition_plan):
    req = setup.add_meal_item(add_meal_for_nutrition_plan.json().get('id'),'dfffdf','$#$#$#')
    return req[0]

@pytest.fixture()
def add_meal_for_nonexisting_plan(setup):
    req = setup.create_meals_for_nutrition_plans('0000')
    return req[0]


@pytest.fixture()
def add_item_for_nonexisting_meal(setup):
    req = setup.add_meal_item('0000','61972',333)
    return req[0]

@pytest.fixture()
def delete_non_existent_plan(setup):
    req = setup.delete_nutrition_plan('44444')
    return req[0]

@pytest.fixture()
def delete_non_existent_meal(setup,add_nutrition_plan):
    req = setup.delete_nutrition_plan(nutrtion_plan_id=add_nutrition_plan.json().get('id')
                                      ,meal_id='4444')
    return req[0]

@pytest.fixture()
def delete_non_existent_item(setup,add_nutrition_plan,add_meal_for_nutrition_plan,add_item_for_meal_nutrition_plan):
    req = setup.delete_nutrition_plan(nutrtion_plan_id=add_nutrition_plan.json().get('id')
                                      ,meal_id=add_meal_for_nutrition_plan.json().get('id')
                                      ,item_id='55555')
    return req[0]


#Positive tests

def test_add_nutrition_plan(add_nutrition_plan):
    assert add_nutrition_plan

def test_add_meal_nutrition_plan(add_meal_for_nutrition_plan):
    assert add_meal_for_nutrition_plan

def test_add_item_for_meal(add_item_for_meal_nutrition_plan):
    assert add_item_for_meal_nutrition_plan

def test_add_multiple_nutriton_plans(add_multiple_nutrition_plans):
    assert add_multiple_nutrition_plans

def test_add_multiple_meals(add_multiple_meals):
    assert add_multiple_meals

def test_add_multiple_items_per_meal(add_multiple_items):
    assert add_multiple_items

def test_delete_nutrition_plan(delete_nutrition_plan):
    assert delete_nutrition_plan

def test_delete_meal_from_nutrition_plan(delete_meal_from_nutrition_plan):
    assert delete_meal_from_nutrition_plan

def test_delete_item_from_meal(delete_item_from_meal):
    assert delete_item_from_meal

def test_delete_multiple_nutrition_plans(delete_multiple_nutrition_plans):
    assert delete_multiple_nutrition_plans

def test_delete_multiple_meals(delete_multiple_meals):
    assert delete_multiple_meals

def test_delete_multiple_items(delete_multiple_items):
    assert delete_multiple_items

# Negative tests

def test_add_meal_nutrition_plan_bad_parameters(add_meal_nutrition_plan_bad_parameters):
    assert add_meal_nutrition_plan_bad_parameters is False

def test_add_item_invalid_values(add_item_invalid_values):
    assert add_item_invalid_values is False

def test_add_meal_nonexisting_plan(add_meal_for_nonexisting_plan):
    assert add_meal_for_nonexisting_plan is False

def test_add_item_nonexisting_meal(add_item_for_nonexisting_meal):
    assert add_item_for_nonexisting_meal is False

def test_delete_non_existent_plan (delete_non_existent_plan):
    assert delete_non_existent_plan is False

def test_delete_non_existent_meal (delete_non_existent_meal):
    assert delete_non_existent_meal is False

def test_delete_non_existent_item(delete_non_existent_item):
    assert delete_non_existent_item is False