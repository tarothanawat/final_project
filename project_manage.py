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

def change_role(ID, role):
    persons_table = alldata.search('persons')
    persons_table.update_row('ID', ID, 'type', role)

    login_table = alldata.search('login')
    login_table.update_row('ID', ID, 'role', role)

def get_data(ID):
    persons_table = alldata.search('persons')
    user_data = persons_table.filter(lambda x: x['ID'] == ID)
    # print(user_data.table[0])
    return user_data.table[0]

def get_role(ID):
    persons_table = alldata.search('persons')
    type = persons_table.filter(lambda x: x['ID'] == ID).aggregate(lambda x: x, 'type')
    print(type)
    return type

def get_project(leader_id):
    project_table = alldata.search('project')
    find_project = project_table.filter(lambda x: x['Lead'] == leader_id)
    # print(find_project.table[0])
    return find_project.table[0]


class Student:
    def __init__(self, data):
        self.data = data
        self.id = data['ID']
        self.first = data['first']
        self.last = data['last']
        self.type = data['type']

        # print(self.project_id)
        self.pending_request = {}
        self.project_data = {}
        self.run()

    def __str__(self):
        return (f"You logged in as {self.first} {self.last}. \n"
                f"You are a {self.type}.")

    def update_table(self, table_name, data):
        my_table = alldata.search(table_name)
        my_table.insert_row(data)

    def check_inbox(self):
        project_table = alldata.search('project')
        pending_req_table = alldata.search('member_pending_request')
        find_req = pending_req_table.filter(lambda x: x['to_be_member'] == self.id)
        print(f"You have {len(find_req.table)} pending request(s).")
        for data in find_req.table:
            find_project = project_table.filter(lambda x: x['ProjectID'] == data['ProjectID'])
            project_data = find_project.table[0]
            get_leader = get_data(project_data['Lead'])
            print(f"{get_leader['first']} {get_leader['last']} has invited you to join their project group.")
            print(f"ProjectID: {project_data['ProjectID']} Title: {project_data['Title']}")
            print()

        print("Choose which request you want to response to.")
        while True:
            project_res = str(input("Enter the ProjectID: "))
            find_req = pending_req_table.filter(lambda x: x['ProjectID'] == project_res)
            if find_req != []:
                break
            print("Invalid ProjectID. Try again.")
        find_req = pending_req_table.filter(lambda x: x['ProjectID'] == project_res)
        while True:
            response = str(input("What is your response? (Accept/Deny): "))
            if response.lower() == 'accept':
                find_req.update_row('to_be_member', self.id, 'Response', 'Accept')
                date = str(input("Enter the date of response (Date/Month): "))
                find_req.update_row('to_be_member', self.id, 'Response_date', date)
                print(f"You have accepted the request to projectID({project_res}).")
                print("Returning to menu...")
                break
            elif response.lower() != 'deny':
                find_req.update_row('to_be_member', self.id, 'Response', 'Deny')
                date = str(input("Enter the date of response (Date/Month): "))
                find_req.update_row('to_be_member', self.id, 'Response_date', date)
                print(find_req.table)
                print(f"You have denied the request to projectID({project_res}).")
                print("Returning to menu...")
                break
            elif response.lower() != 'accept' or response.lower() != 'deny':
                print("Your response is invalid. Tryagain.")
                continue

    def create_project(self):
        project_table = alldata.search('project')
        project_id = project_table.aggregate(lambda x: str(x), 'ProjectID')
        # print(project_id)
        print("To create a project you will be promoted to be a leader and you must deny all pending invites.")
        choice = input("Accept condition? (Y/N): ")
        if choice.lower() == 'n':
            print("Project creation progress has been canceled. Returning to menu...")
            return None
        if choice.lower() == 'y':
            while True:
                id_input = str(input("Create your project ID. (ID must be 5 digits): "))
                if len(id_input) == 5 and id_input not in project_id:
                    break
                print("Your ID must contains 4 digits and must not been taken. Try again.")
                print()

            title = input("Enter your project Title: ")
            self.project_data.update({'ProjectID': id_input, 'Title': title, 'Lead': self.id, 'Member1': None, 'Member2': None, 'Advisor': None, 'Status': 'Pending'})
            self.update_table('project', self.project_data)
            change_role(self.id, 'lead')
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


class Leader:
    def __init__(self, data):
        self.data = data
        self.id = data['ID']
        self.first = data['first']
        self.last = data['last']
        self.type = data['type']

        self.project_data = get_project(self.id)
        self.project_id = self.project_data['ProjectID']
        # print(self.project_id)
        self.pending_request = {}
        self.run()

    def __str__(self):
        return (f"You logged in as {self.first} {self.last}. \n"
                f"You are a {self.type}.")

    def project_status(self):
        pass

    def modify_project(self):
        pass

    def check_inbox(self):
        member_pending_table = alldata.search('member_pending_request')
        find_project_req = member_pending_table.filter(lambda x: x['ProjectID'] == self.project_id)
        print(f"You have sent out {len(find_project_req.table)} invite(s).")
        for i in find_project_req.table:
            data = get_data(i['to_be_member'])
            first = data['first']
            last = data['last']
            print(f"You invited {i['to_be_member']} {first} {last}.")
            print(f"Their response: {i['Response']} , date: {i['Response_date']}")
            print()
        print(f"Choose a student to be member of your project group.")
        while True:
            member_id = str(input("Enter their ID: "))
            find_mem_req = find_project_req.filter(lambda x: x['to_be_member'] == member_id)
            if find_mem_req != []:
                break
            print("Invalid ID. Please try again.")
        data = get_data(member_id)
        first = data['first']
        last = data['last']
        project_table = alldata.search('project')
        find_project = project_table.filter(lambda x: x['ProjectID'] == self.project_id)
        print(f"You're about to add {first} {last} to your group.")
        confirm = str(input("Do you wish to confirm? (Y/N): "))
        if confirm.lower() == 'y':
            if find_project.table[0]['Member1'] == '':
                find_project.update_row('ProjectID', self.project_id, 'Member1', member_id)
                change_role(member_id, 'member')
                print(f"{first} {last} has been added to your group as Member1. Returning to menu...")
            elif find_project.table[0]['Member2'] == '':
                find_project.update_row('ProjectID', self.project_id, 'Member2', member_id)
                change_role(member_id, 'member')
                print(f"{first} {last} has been added to your group as Member2. Returning to menu...")
            else:
                print("Your exceeds the limit of 2 members, you can't add more. Returning to menu...")
        if confirm.lower() == 'n':
            print("Member adding process cancelled. Returning to menu...")

    def invite_members(self):
        request_data = {}
        member_pending_table = alldata.search('member_pending_request')
        persons_table = alldata.search('persons')
        available_students = persons_table.filter(lambda x: x['type'] == 'student')
        while True:
            print("Here is the list of available students.")
            print(available_students.table)
            id_member = str(input("Please Enter the ID of your potential member: "))
            member_data = get_data(id_member)
            print(f"You're about to invite {member_data['first']} {member_data['last']} as a member of your team.")
            confirm = str(input("Do you wish to confirm? (Y/N): "))
            if confirm.lower() == 'y':
                request_data.update({'ProjectID': self.project_id, 'to_be_member': id_member, 'Response': 'HasNotRespond', 'Response_date': 'HasNotRespond'})
                member_pending_table.insert_row(request_data)
                print(f"Invite Has been sent to {member_data['first']} {member_data['last']}. Please re-login to see changes.")
                break
            elif confirm.lower() == 'n':
                continue

    def request_prof(self):
        pass

    def run(self):
        print(self)
        print()
        while True:
            print("You have permission to do the following:")
            print("1. See project status.")
            print("2. See and modify project info.")
            print("3. Check inbox.")
            print("4. Invite members.")
            print("5. Send request to a professor.")
            print("6. Logout")
            choice = int(input("Enter your choice: "))
            if choice == 1:
                print()
                self.project_status()
            elif choice == 2:
                print()
                self.modify_project()
            elif choice == 3:
                print()
                self.check_inbox()
            elif choice == 4:
                print()
                self.invite_members()
            elif choice == 5:
                print()
                self.request_prof()
            elif choice == 6:
                break
            print()


class Project:
    def __init__(self):
        pass


# define a function called exit
def exit():
    print("You have logged out.")
    tables = {
        'login': 'login.csv',
        'persons': 'persons.csv',
        'project': 'project.csv',
        'advisor_pending_request': 'advisor_pending_request.csv',
        'member_pending_request': 'member_pending_request.csv'
    }

    field_names = {
        'login': ['ID', 'username', 'password', 'role'],
        'persons': ['ID', 'first', 'last', 'type'],
        'project': ['ProjectID', "Title", "Lead", 'Member1', 'Member2', 'Advisor', 'Status'],
        'advisor_pending_request': ['ProjectID', 'to_be_advisor', 'Response', 'Response_date'],
        'member_pending_request': ['ProjectID', 'to_be_member', 'Response', 'Response_date']
    }

    for table_name, file_name in tables.items():
        table = alldata.search(table_name)
        file = open(file_name, 'w', newline='')
        writer = csv.DictWriter(file, fieldnames=field_names[table_name])
        writer.writeheader()
        writer.writerows(table.table)
        file.close()

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
    leader1 = Leader(user_data)
    pass
elif val[1] == 'faculty':
    #see and do faculty related activities
    pass
elif val[1] == 'advisor':
    #see and do advisor related activities
    pass



# once everyhthing is done, make a call to the exit function
exit()
