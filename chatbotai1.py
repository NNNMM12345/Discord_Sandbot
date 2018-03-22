import random
import shelve
import wikipedia as wiki
data = shelve.open("data.pkl")
data = {}

print("Hello User") 

search_term = input("Enter the term you want to search for:")
objective = wiki.page(search_term)

print(objective.title)
print(objective.content)


def func():
    if data.get("age"):
        old = data.get("age")
        name = data.get("name")
        print(f"Your age is {old}, {name}")
    else:
        print("You haven't told me your age yet")


while True:
    if data.get("name"):
        name = data.get("name")
        print(f"Hello {name}, ", end="")
    u_in = input("How can I help? ").strip().lower()

    if u_in == "roll a die":
        num = random.randint(1, 6)
        print(f"The computer rolled = {num}")
    elif u_in == "google something":
        pass

    elif u_in.startswith("call me"):
        name = u_in.split("call me")[1].strip()
        print(f"I will call you {name}")
        data["name"] = name

    elif u_in.startswith("Your age"):
        age = u_in.split("Your age")[1].strip()
        print(f"Your age is {age}")
        data["age"] = age

    elif u_in.startswith('How old am I'):
        func()
