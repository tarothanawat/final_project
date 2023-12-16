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
    advisor_pending = read_csv('advisor_pending_request.csv')
    member_pending = read_csv('member_pending_request.csv')

    persons_table = Table("persons", persons)
    login_table = Table("login", login)
    project_table = Table('project', project)
    advisor_pending_table = Table('advisor_pending_request', advisor_pending)
    member_pending_table = Table('member_pending_request', member_pending)

    alldata.insert(persons_table)
    alldata.insert(login_table)
    alldata.insert(project_table)
    alldata.insert(advisor_pending_table)
    alldata.insert(member_pending_table)


# define a function called login

def login():

# here are things to do in this function:
   # add code that performs a login task
        # ask a user for a username and password
        # returns [ID, role] if valid, otherwise returning None
    while True:
        login_table = alldata.search('login')
        user = input("Enter Your Username: ")
        password = input("Enter your password: ")

        find_person = login_table.filter(lambda x: x['username'] == user and x['password'] == password)
        if find_person.table != []:
            break
        print("Your Username or password is incorrect! Try again.")
    # print(find_person.table)
    return [find_person.table[0]['ID'], find_person.table[0]['role']]

def get_data(ID):
    persons_table = alldata.search('persons')
    user_data = persons_table.filter(lambda x: x['ID'] == ID)
    # print(user_data.table[0])
    return user_data.table[0]

class Student:
    def __init__(self, data):
        self.data = data
        self.id = data['ID']
        self.first = data['first']
        self.last = data['last']
        self.type = data['type']
        self.project_data = {}
        self.run()

    def __str__(self):
        return (f"You logged in as {self.first} {self.last}. \n"
                f"You are a {self.type}.")

    def update_table(self, table_name, data):
        my_table = alldata.search(table_name)
        my_table.insert_row(data)
        print(my_table)

    def check_inbox(self):
        print("inbox test")

    def create_project(self):
        project_table = alldata.search('project')
        project_id = project_table.filter(lambda x: x['ProjectID'])
        print("To create a project you will be promoted to be a leader and you must deny all pending invites.")
        choice = input("Accept condition? (Y/N): ")
        if choice.lower() == 'n':
            print("Project creation progress has been canceled. Returning to menu.")
            return None
        if choice.lower() == 'y':
            while True:
                id_input = str(input("Enter your project ID. (ID must be 5 digits): "))
                if len(id_input) == 5 and id_input not in project_id.table:
                    break
                print("Your ID must contains 4 digits! Try again.")
                print()
            title = input("Enter your project Title: ")
            self.project_data.update({'ProjectID': id_input, 'Title': title, 'Lead': self.id, 'Member1': None, 'Member2': None, 'Advisor': None, 'Status': 'Pending'})
            self.update_table('project', self.project_data)
            print(self.project_data)

            print("Project has been initialized, Please re-login.")
            return 1

    def run(self):
        print(self)
        print()
        while True:
            print("You have permission to do the following:")
            print("1. Check inbox.")
            print("2. Create a project.")
            print("3. Logout.")
            choice = int(input("Enter your choice: "))
            if choice == 1:
                print()
                self.check_inbox()
            elif choice == 2:
                print()
                self.create_project()
            elif choice == 3:
                break
            print()
        #update all tables call function exit()


class Project:
    def __init__(self):
        pass



# define a function called exit
def exit():
    print("You have logged out.")
    login_table = alldata.search('login')
    persons_table = alldata.search('persons')
    project_table = alldata.search('project')
    advisor_pending_table = alldata.search('advisor_pending_request')
    member_pending_table = alldata.search('member_pending_request')

    login_file = open('login.csv', 'w', newline='')
    login_writer = csv.DictWriter(login_file, fieldnames=login_table.table[0].keys())
    login_writer.writeheader()
    login_writer.writerows(login_table.table)
    login_file.close()

    persons_file = open('persons.csv', 'w', newline='')
    persons_writer = csv.DictWriter(persons_file, fieldnames=persons_table.table[0].keys())
    persons_writer.writeheader()
    persons_writer.writerows(persons_table.table)
    persons_file.close()

    project_file = open('project.csv', 'w', newline='')
    project_writer = csv.DictWriter(project_file, fieldnames=['ProjectID', "Title", "Lead", 'Member1', 'Member2', 'Advisor', 'Status'])
    project_writer.writeheader()
    project_writer.writerows(project_table.table)
    project_file.close()

    advisor_file = open('advisor_pending_request.csv', 'w', newline='')
    advisor_writer = csv.DictWriter(advisor_file, fieldnames=['ProjectID','to_be_advisor','Response','Response_date'])
    advisor_writer.writeheader()
    advisor_writer.writerows(advisor_pending_table.table)
    advisor_file.close()

    member_file = open('member_pending_request.csv', 'w', newline="")
    member_writer = csv.DictWriter(member_file, fieldnames=['ProjectID', 'to_be_member', 'Response', 'Response_date'])
    member_writer.writeheader()
    member_writer.writerows(member_pending_table.table)
    member_file.close()

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
