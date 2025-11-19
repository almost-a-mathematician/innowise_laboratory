from datetime import datetime


def generate_profile(age: int):
    '''This function determines age group by age'''

    if age < 0:
        return None
    if age <= 12:
        return 'Child'
    elif age <= 19:
        return 'Teenager'
    else:
        return 'Adult'  

print('Hello!')
user_name = input('Enter your full name: ')
birth_year_str = input('Enter your birth year: ')

birth_year = int(birth_year_str)
current_age = datetime.now().year - birth_year

hobbies = []

while True:
    '''This loop forms a hobby list untill the user enters 'stop' '''

    hobby_input = input('Enter a favorite hobby or type \'stop\' to finish: ')
    if hobby_input.lower() == 'stop':
        break
    hobbies.append(hobby_input)

life_stage = generate_profile(current_age)

user_profile = {'name': user_name, 'age': current_age, 'stage': life_stage, 'hobbies': hobbies}

print('\n---')
print('Profile Summary:')
print(f'Name: {user_profile["name"]}')
print(f'Age: {user_profile["age"]}')
print(f'Life Stage: {user_profile["stage"]}')

if hobbies:
    print(f'Favorite Hobbies ({len(hobbies)}):')
    for hobby in hobbies:
        print(f'- {hobby}')
else: 
    print('You didn\'t mention any hobbies')

print('---\n')
