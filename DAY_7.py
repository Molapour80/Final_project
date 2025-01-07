import random

first_names_male = [
    "Ali", "Reza", "Mohammad", "Omid", "Farid",
    "Saeed", "Navid", "Kaveh", "Arash", "Amir"
]

first_names_female = [
    "Fatemeh", "Zahra", "Sara", "Niloofar", "Leila",
    "Parisa", "Shirin", "Nazanin", "Mina", "Yasaman"
]

last_names = [
    "Ahmadzadeh", "Mohammadi", "Karimi", "Javan", "Sadeghi",
    "Hosseini", "Rezaei", "Gholami", "Khodadadi", "Fakhradi"
]

def generate_random_name(gender='male'):
    
    if gender == 'male':
        first_name = random.choice(first_names_male) 
    elif gender == 'female':
        first_name = random.choice(first_names_female)  
    else:
        raise ValueError("name is  must be male or female ")

    last_name = random.choice(last_names)  
    return f"{first_name} {last_name}"  

def main():
    
    num_names = int(input("chose your 'male' or 'female' :"))
    
    print(f"name male :{first_names_male}")
    for _ in range(num_names):
        print(generate_random_name('male'))

    print(f"name female :{first_names_female}")
    for _ in range(num_names):
        print(generate_random_name('female'))

if __name__ == "__main__":
    main()