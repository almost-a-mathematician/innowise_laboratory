'''Students grade manager'''
from typing import Any, Set
from re import split

# List of dictionaries representing students
students: list[dict[str, Any]] = []

# Set for fast student lookup by name, used where the task doesn't restrict its use
student_index: Set[str] = set()


def add_student() -> None:
    '''
    This function prompts the user to enter a new student's name and adds it to the students list
    Validates name input: only alphabetic characters are allowed.
    Input is normalized (converted to Title Case and side whitespace is removed)
    '''

    # Request and normalize name input
    name: str = input('Enter student name: ').title().strip()
    if not name.replace(' ', '').isalpha():
        print('Name should be not empty and contain only alphabetic characters')
        return

    # Check if student exists in index (O(1) complexity). If student already exists - don't add
    if name in student_index:
        print('Student with this name already exists')
        return

    # Add student to students list and add their name to student_index
    new_student = {'name': name, 'grades': [], 'average': None}
    students.append(new_student)
    student_index.add(new_student['name'])


def add_student_grade() -> None:
    '''
    This function adds one or more grades for a student by his name
    Supports entering a single grade or multiple grades at once, 
    with 'done' input stops the operation
    EXAMPLES:
    Input: 80
    Result: grade 80 is added, input is requested again
    Input: 100 80 30
    Result: grades [100, 80, 30] are added, input is requested again
    Input: 100 80 30 done 20
    Result: grades [100, 80, 30] are added, grades after 'done' are ignored, input stops
    Input: done
    Result: input stops
    '''

    # Request student name input and normalize it
    student_name: str = input('Enter student name: ').title().strip()
    found_student: dict | None = None

    # Perform linear search through students bypassing student_index per task requirements
    for student in students:
        if student['name'] == student_name:
            found_student = student
            break

    # Notify the user and stop function execution if student was not found by name
    if found_student is None:
        print('Student with this name does not exist')
        return

    # Start infinite input loop
    while True:
        done_entered: bool = False

        # Accept user input, normalize and split it by delimiters
        grades_input: list[str] = split(
            r'[,;\s]+', input('Enter a grade (or \'done\' to finish): ').strip().lower()
        )

        # If 'done' is among the elements, trim the list including the found string itself
        if grades_input.count('done'):
            grades_input = grades_input[:grades_input.index('done')]

            # Mark that the function should stop at the end of input processing
            done_entered = True

            # Stop the function early if grades list is empty after excluding 'done'
            if not grades_input:
                break

        # Start the loop through list to validate its elements
        for grade in grades_input:
            # Try to convert element to int. Loop will break on failure
            try:
                grade = int(grade)
            except ValueError:
                print('Enter a valid integer number')
                break

            # Check that grade is in range [0, 100], otherwise break the loop
            if grade < 0 or grade > 100:
                print('Enter an integer number betweet 0 and 100')
                break
        else:
            # If the validation loop wasn't broken, add all grades to student
            for grade in grades_input:
                found_student['grades'].append(int(grade))

            # Calculate student's average grade including new grades and record the result
            found_student['average'] = (sum(found_student['grades'])/len(found_student['grades']))

            # If 'done' was entered, stop function execution
            if done_entered:
                break


def get_report() -> None:
    '''
    This function displays a detailed summary of all students' grades
    and the minimum, maximum, and overall average grade
    among all students who have at least one grade
    '''

    # List to store students' average grades
    average_list: list[float] = []

    print('--- Student Report ---')

    # Iterate through students list
    for student in students:
        try:
            # Try to calculate average grade. We could use the pre-calculated
            # student['average'], but the task requires this specific way of getting the average
            average: str | int = sum(student['grades'])/len(student['grades'])

            # Add an average grade to the list
            average_list.append(average)

            # Formating grade with a limit of one decimal place
            # This is the fastest formatting method, ~25% faster than round
            average = f'{average:.1f}'

        except ZeroDivisionError:
            # In case of ZeroDivisionError, record status indicating no grade
            average: str = 'N/A'

        print(f'{student["name"]}\'s average grade is {average}.')


    if len(average_list) == 0:
        if len(students) == 0:
            # Display a message about absence of students
            print('There is no students')
        else:
            # Display a message about absence of assigned grades
            print('There is no grades')

    else:
        # Output average grades for all the students
        print('--------------------------')
        print(f'Max Average: {max(average_list):.1f}')
        print(f'Min Average: {min(average_list):.1f}')
        print(f'Overall Average: {(sum(average_list)/len(average_list)):.1f}')


def get_top_performer() -> None:
    '''
    This function calculates the student with the highest average grade among all others 
    and displays a message about him.
    '''

    # Create a filtered list of students where each student has an average grade
    graded_students: list[dict] = list(
        filter(lambda student: student['average'] is not None, students)
    )

    # Select a student with the highest average grade. Returns None if students list is empty
    top_performer: dict | None = max(
        graded_students, default=None, key=lambda student: student['average']
    )

    # Display an appropriate message
    if top_performer is None:
        print('There is no student with the highest average grade')
    else:
        print(
            f'The student with the highest average is {top_performer["name"]} \
            with a grade of {top_performer["average"]:.1f}'
        )


# The main program loop
while True:
    print('\n--- Student Grade Analyzer ---')
    print('1. Add a new student')
    print('2. Add grades for a student')
    print('3. Generate a full report')
    print('4. Find the top student')
    print('5. Exit program')

    # Request normalized a menu item input. The ValueError handling is not required here because
    # I don't convert input to int
    user_input: str = input('Enter your choice: ').strip()

    # Match an entered string with one of the possible menu items
    if user_input == '1':
        add_student()
    elif user_input == '2':
        add_student_grade()
    elif user_input == '3':
        get_report()
    elif user_input == '4':
        get_top_performer()
    elif user_input == '5':
        # This menu item stops the program loop
        print('Exiting program.')
        break
    else:
        # If no matching menu item was found for the input, display a message about it
        print('Invalid choice. Please enter a number between 1 and 5.')
