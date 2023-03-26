import requests
import json

BASE_URL = "https://www.hellofresh.co.uk"
RECIPE_URL = BASE_URL + "/gw/recipes/recipes/search?country=GB&locale=en-GB&min-rating=3.3"
# url = "https://www.hellofresh.co.uk/gw/recipes/recipes/search?country=GB&locale=en-GB&min-rating=3.3&take=1000"
payload={}
headers = {
  'authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2ODIxMzczNjYsImlhdCI6MTY3OTUwNzYyMywiaXNzIjoic2VuZiIsImp0aSI6IjA5MDlmMWI2LWQ2YTAtNDJlMS04MWYxLTlkNmVjNDhiYTU2YSJ9.PQwt8JWr5_WbJI1CHkycPBCu9zqqEaQTTjGx16WGdMk',
}
IMAGE_URL = "https://img.hellofresh.com/ar_1,w_3840,q_auto,f_auto,c_fill,fl_lossy/hellofresh_s3"

def get_total_recipes():
    response = requests.request("GET", RECIPE_URL + "&take=1", headers=headers, data=payload)
    return response.json()["total"]

def get_recipes():
    skip = 0
    take = 250
    total = get_total_recipes()

    recipes = []

    print(total)
    while skip < total:
        response = requests.request("GET", RECIPE_URL + f"&skip={skip}&take={take}", headers=headers, data=payload)
        data = response.json()
        recipes += data["items"]
        skip += take
        print(skip)

    print(len(recipes))
    return recipes

def save_data(data, name):
    with open(name, 'w') as outfile:
        json.dump(data, outfile, indent=4)

def load_data(data):
    with open(data) as json_file:
        return json.load(json_file)

def parse_data(recipes):
    ingredients = []
    categories  = []
    allergies   = []
    cuisines    = []

    for recipe in recipes:
        # ingredients
        for ingredient in recipe["ingredients"]:
            if ingredient["name"] not in ingredients:
                ingredients.append(ingredient["name"])
        
        # categories
        if recipe["category"] is not None:
            if recipe["category"]["name"] not in categories:
                categories.append(recipe["category"]["name"])

        

        # allergies
        for allergy in recipe["allergens"]:
            if allergy["name"] not in allergies:
                allergies.append(allergy["name"])

        # cuisines
        for cuisine in recipe["cuisines"]:
            if cuisine["name"] not in cuisines:
                cuisines.append(cuisine["name"])

    # for ingredient in ingredients:
    #     print(ingredient)
    # print(len(ingredients))

    for category in categories:
        print(category)
    print(len(categories))

    # for allergy in allergies:
    #     print(allergy)
    # print(len(allergies))

    # for cuisine in cuisines:
    #     print(cuisine)
    # print(len(cuisines))



def filter_data(recipes):
    data = {
        "ingredients": [],
        "categories": [],
        "allergies": [],
        "cuisines": [],
        "recipes": []
    }

    for recipe in recipes:

        ## Adding recipe to data
        # filter out recipes with G\u00fc 
        if "G\u00fc" in recipe["name"]:
            continue
        # filter out recipes with Re:Nourish
        if "Re:Nourish" in recipe["name"]:
            continue
        

        if recipe["prepTime"] is None:
            recipe["prepTime"] = "PT"
        
        # extract time out of PT1H30M30S
        recipe["prepTime"] = recipe["prepTime"].replace("PT", "")
        # filter out xHxMxS
        time = 0
        if "H" in recipe["prepTime"]:
            time += int(recipe["prepTime"].split("H")[0]) * 60
            recipe["prepTime"] = recipe["prepTime"].split("H")[1]
        if "M" in recipe["prepTime"]:
            time += int(recipe["prepTime"].split("M")[0])
            recipe["prepTime"] = recipe["prepTime"].split("M")[1]
        
        recipe["prepTime"] = time


        if recipe["totalTime"] is None:
            recipe["totalTime"] = "PT"
        
        recipe["totalTime"] = recipe["totalTime"].replace("PT", "")
        # filter out xHxMxS
        time = 0
        if "H" in recipe["totalTime"]:
            time += int(recipe["totalTime"].split("H")[0]) * 60
            recipe["totalTime"] = recipe["totalTime"].split("H")[1]
        if "M" in recipe["totalTime"]:
            time += int(recipe["totalTime"].split("M")[0])
            recipe["totalTime"] = recipe["totalTime"].split("M")[1]


        recipe["totalTime"] = time



        new_recipe = {
            "name": recipe["name"],
            "headline": recipe["headline"],
            "description": recipe["description"],
            "category": None,
            "cuisine": None,
            "difficulty": recipe["difficulty"],
            "time": recipe["prepTime"] + recipe["totalTime"], # in minutes
            "imageLink" : IMAGE_URL + recipe["imagePath"],
            "link" : recipe["websiteUrl"],
            "ingredients": [],
            "allergies": []
        }
        if len(recipe["cuisines"]) > 0:
            new_recipe["cuisine"] = recipe["cuisines"][0]["name"].lower()
        
        if recipe["category"] is not None:
            new_recipe["category"] = recipe["category"]["name"].lower()

        for ingredient in recipe["ingredients"]:
            new_recipe["ingredients"].append(ingredient["name"].lower())

        for allergy in recipe["allergens"]:
            new_recipe["allergies"].append(allergy["name"].lower())

        data["recipes"].append(new_recipe)

        ## Adding ingredients to data
        for ingredient in recipe["ingredients"]:
            if ingredient["name"].lower() not in data["ingredients"]:
                data["ingredients"].append(ingredient["name"].lower())
        
        ## Adding categories to data
        if recipe["category"] is not None:
            if recipe["category"]["name"].lower() not in data["categories"]:
                data["categories"].append(recipe["category"]["name"].lower())
        
        ## Adding allergies to data
        for allergy in recipe["allergens"]:
            if allergy["name"].lower() not in data["allergies"]:
                data["allergies"].append(allergy["name"].lower())
        
        ## Adding cuisines to data
        for cuisine in recipe["cuisines"]:
            if cuisine["name"].lower() not in data["cuisines"]:
                data["cuisines"].append(cuisine["name"].lower())
        
    
    return data


# recipes = load_data()
# recipes = get_recipes()

# save_data(recipes, "data_old.json")
recipes = load_data("data_old.json")
data = filter_data(recipes)

save_data(data, "data.json")

