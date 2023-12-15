# import database module
import database
from database import read_csv, DB, Table, write_csv
import csv
# define a funcion called initializing

def initializing():


# here are things to do in this function:
    # create an object to read all csv files that will serve as a persistent state for this program

    # create all the corresponding tables for those csv files

    # see the guide how many tables are needed

    # add all these tables to the database
    persons = read_csv('persons.csv')
    login = read_csv('login.csv')
    project = read_csv('project.csv')

    persons_table = Table("persons", persons)
    login_table = Table("login", login)
    project_table = Table('project', project)

    alldata.insert(persons_table)
    alldata.insert(login_table)
    alldata.insert(project_table)


# define a function called login

def login():

# here are things to do in this function:
   # add code that performs a login task
        # ask a user for a username and password
        # returns [ID, role] if valid, otherwise returning None
    login_table = alldata.search('login')
    user = input("Enter Your Username: ")
    password = input("Enter your password: ")

    find_person = login_table.filter(lambda x: x['username'] == user and x['password'] == password)
    if find_person.table == []:
        return None
    # print(find_person.table)
    return [find_person.table[0]['ID'], find_person.table[0]['role']]

def get_data(ID):
    persons_table = alldata.search('persons')
    user_data = persons_table.filter(lambda x: x['ID'] == ID)
    # print(user_data.table[0])
    return user_data.table[0]

class Student:
    def __init__(self, data):
        self.id = data['ID']
        self.first = data['first']
        self.last = data['last']
        self.type = data['type']
        self.requests = []
        self.run()

    def __str__(self):
        return (f"You logged in as {self.first} {self.last}. \n"
                f"You are a {self.type}.")
    def check_inbox(self):
        print("inbox test")

    def create_project(self):
        print("To create a project you will be promoted to be a leader and you must deny all pending invites.")
        choice = input("Accept condition? (Y/N): ")


    def run(self):
        print(self)
        while True:
            print("You have permission to do the following:")
            print("1. Check inbox.")
            print("2. Create a project.")
            print("3. Save changes and logout.")
            choice = int(input("Enter your choice: "))
            if choice == 1:
                self.check_inbox()
            elif choice == 2:
                self.create_project()
            elif choice == 3:
                break
        #update all tables call function exit()

class Project:
    def __init__(self):
        pass






# define a function called exit
def exit():
    pass

# here are things to do in this function:
   # write out all the tables that have been modified to the corresponding csv files
   # By now, you know how to read in a csv file and transform it into a list of dictionaries. For this project, you also need to know how to do the reverse, i.e., writing out to a csv file given a list of dictionaries. See the link below for a tutorial on how to do this:
   
   # https://www.pythonforbeginners.com/basics/list-of-dictionaries-to-csv-in-python


# make calls to the initializing and login functions defined above
alldata = DB()
initializing()
val = login()
user_data = get_data(val[0])


# based on the return value for login, activate the code that performs activities according to the role defined for that person_id

if val[1] == 'admin':
    #see and do admin related activities
    pass
elif val[1] == 'student':
    #see and do student related activities
    student1 = Student(user_data)
elif val[1] == 'member':
    #see and do member related activities
    pass
elif val[1] == 'lead':
    #see and do lead related activities
    pass
elif val[1] == 'faculty':
    #see and do faculty related activities
    pass
elif val[1] == 'advisor':
    #see and do advisor related activities
    pass



# once everyhthing is done, make a call to the exit function
exit()
