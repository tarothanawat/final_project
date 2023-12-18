# import database module
import database
from database import read_csv, DB, Table, write_csv
import csv
import datetime
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
    evaluation = read_csv('evaluation.csv')

    persons_table = Table("persons", persons)
    login_table = Table("login", login)
    project_table = Table('project', project)
    advisor_pending_table = Table('advisor_pending_request', advisor_pending)
    member_pending_table = Table('member_pending_request', member_pending)
    evaluation_table = Table('evaluation', evaluation)

    alldata.insert(persons_table)
    alldata.insert(login_table)
    alldata.insert(project_table)
    alldata.insert(advisor_pending_table)
    alldata.insert(member_pending_table)
    alldata.insert(evaluation_table)


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
    if user_data == []:
        return None
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


def get_project_projectID(projectID):
    project_table = alldata.search('project')
    find_project = project_table.filter(lambda x: x['ProjectID'] == projectID)
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
                find_req.update_row('to_be_member', self.id, 'Response_date', datetime.date.today())
                member_req_table = alldata.search('member_pending_request')
                find_other_req = member_req_table.filter(lambda x: x['Response'] == 'HasNotRespond')
                find_other_req.update_row('to_be_member', self.id, 'Response', 'Deny')
                find_other_req.update_row('to_be_member', self.id, 'Response_date', datetime.date.today())
                print(f"You have accepted the request to projectID({project_res}).")
                print("Returning to menu...")
                break
            elif response.lower() == 'deny':
                find_req.update_row('to_be_member', self.id, 'Response', 'Deny')
                find_req.update_row('to_be_member', self.id, 'Response_date', datetime.date.today())
                print(f"You have denied the request to projectID({project_res}).")
                print("Returning to menu...")
                break
            elif response.lower() != 'accept' or response.lower() != 'deny':
                print("Your response is invalid. Tryagain.")
                continue
        exit()

    def create_project(self):
        project_table = alldata.search('project')
        eval_table = alldata.search('evaluation')
        member_req_table = alldata.search('member_pending_request')
        project_id = project_table.aggregate(lambda x: str(x), 'ProjectID')
        # print(project_id)
        print("To create a project you will be promoted to be a leader and you must deny all pending invites.")
        while True:
            choice = str(input("Accept condition? (Y/N): "))
            if choice.lower() in 'ny':
                break
        if choice.lower() == 'n':
            print("Project creation progress has been canceled. Returning to menu...")
            return None
        if choice.lower() == 'y':
            while True:
                id_input = str(input("Create your project ID. (ID must be 5 digits): "))
                if len(id_input) == 5 and id_input not in project_id:
                    break
                print("Your ID must contains 5 digits and must not been taken. Try again.")
                print()

            title = input("Enter your project Title: ")
            self.project_data.update({'ProjectID': id_input, 'Title': title, 'Lead': self.id, 'Member1': 'None', 'Member2': 'None', 'Advisor': 'None', 'Status': 'Pending'})
            eval_table.insert_row({'ProjectID': id_input, 'Report': 'None', 'Score': 0, 'Note': 'None', 'Eva1': 'None'})
            self.update_table('project', self.project_data)
            member_req_table.update_row('to_be_member', self.id, 'Response', 'Deny')
            member_req_table.update_row('to_be_member', self.id, 'Response_date', datetime.date.today())
            change_role(self.id, 'lead')
            print("Project has been initialized, returning to menu...")
        exit()

    def run(self):
        print(self)
        print()
        while True:
            print("You have permission to do the following:")
            print("1. Check inbox.")
            print("2. Create a project.")
            print("3. Logout.")
            choice = str(input("Enter your choice: "))
            if choice == '1':
                print()
                self.check_inbox()
            elif choice == '2':
                print()
                self.create_project()
            elif choice == '3':
                print("You have logged out.")
                break
            else:
                print("Choice Invalid. Try again.")
                print()
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
        self.project_title = self.project_data['Title']
        self.project_lead = self.project_data['Lead']
        self.project_mem1 = self.project_data['Member1']
        self.project_mem2 = self.project_data['Member2']
        self.project_advisor = self.project_data['Advisor']
        self.project_status = self.project_data['Status']
        self.pending_request = {}
        self.run()

    def __str__(self):
        return (f"You logged in as {self.first} {self.last}. \n"
                f"You are a {self.type}.")

    def check_status(self):
        get_lead_data = get_data(self.project_lead)
        get_mem1_data = get_data(self.project_mem1)
        get_mem2_data = get_data(self.project_mem2)
        get_advisor_data = get_data(self.project_advisor)
        eval_table = alldata.search('evaluation')
        find_eval = eval_table.filter(lambda x: x['ProjectID'] == self.project_id)
        eval_data = find_eval.table[0]
        print("You are now viewing your project status.")
        print()
        print(f"ProjectID : {self.project_id}")
        print(f"Title : {self.project_title}")
        print(f"Leader : {get_lead_data['first']} {get_lead_data['last']} ({self.project_lead})")
        print(f"Member1 : {get_mem1_data['first']} {get_mem1_data['last']} ({self.project_mem1})")
        print(f"Member2 : {get_mem2_data['first']} {get_mem2_data['last']} ({self.project_mem2})")
        print(f"Advisor : {get_advisor_data['first']} {get_advisor_data['last']} ({self.project_advisor})")
        print(f"Project Report: {eval_data['Report']}")
        print(f"Project Score: {eval_data['Score']}")
        print(f"Note from advisor: {eval_data['Note']}")
        print(f"Project Status : {self.project_status}")

    def check_inbox(self):
        member_pending_table = alldata.search('member_pending_request')

        print("Which message do you want to see?")
        print("1. See invites to potential group member(s).")
        print("2. See request to potential advisor.")
        choose = str(input("Enter your choice: "))
        if choose == "1":
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
                if find_mem_req.table[0]['Response'] != 'Accept':
                    print("Invalid ID(the student didn't accept your invitation or is already in a group). Please try again.")
                    continue

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
                if find_project.table[0]['Member1'] == 'None':
                    find_project.update_row('ProjectID', self.project_id, 'Member1', member_id)
                    change_role(member_id, 'member')
                    # find_project_req.delete_row('ProjectID', self.project_id, 'to_be_member', member_id)
                    find_project_req.update_row('to_be_member', member_id, 'Response', 'JoinedGroup')
                    print(f"{first} {last} has been added to your group as Member1. Returning to menu...")
                elif find_project.table[0]['Member2'] == 'None':
                    find_project.update_row('ProjectID', self.project_id, 'Member2', member_id)
                    change_role(member_id, 'member')
                    # find_project_req.delete_row('ProjectID', self.project_id, 'to_be_member', member_id)
                    find_project_req.update_row('to_be_member', member_id, 'Response', 'JoinedGroup')
                    print(f"{first} {last} has been added to your group as Member2. Returning to menu...")
                else:
                    print("Your group exceeds the limit of 2 members, you can't add more. Returning to menu...")
            if confirm.lower() == 'n':
                print("Member adding process cancelled. Returning to menu...")
        ##############################################################################
        if choose == '2':
            advisor_pending_table = alldata.search('advisor_pending_request')
            find_project_req = advisor_pending_table.filter(lambda x: x['ProjectID'] == self.project_id)
            print(f"You have sent out {len(find_project_req.table)} request(s).")
            for i in find_project_req.table:
                data = get_data(i['to_be_advisor'])
                first = data['first']
                last = data['last']
                print(f"You invited {i['to_be_advisor']} {first} {last}.")
                print(f"Their response: {i['Response']} , date: {i['Response_date']}")
                print()
            print(f"Choose a Professor to be advisor of your project.")
            while True:
                prof_id = str(input("Enter their ID: "))
                find_prof_req = find_project_req.filter(lambda x: x['to_be_advisor'] == prof_id)
                if find_prof_req.table[0]['Response'] != 'Accept':
                    print(
                        "Invalid ID(the professor didn't accept your request or is already an advisor of a group). Please try again.")
                    continue

                if find_prof_req != []:
                    break
                print("Invalid ID. Please try again.")
            data = get_data(prof_id)
            first = data['first']
            last = data['last']
            project_table = alldata.search('project')
            find_project = project_table.filter(lambda x: x['ProjectID'] == self.project_id)
            print(f"You're about to let {first} {last} to be the advisor your group.")
            confirm = str(input("Do you wish to confirm? (Y/N): "))
            if confirm.lower() == 'y':
                if find_project.table[0]['Advisor'] == 'None':
                    find_project.update_row('ProjectID', self.project_id, 'Advisor', prof_id)
                    change_role(prof_id, 'advisor')
                    # find_project_req.delete_row('ProjectID', self.project_id, 'to_be_member', member_id)
                    find_project_req.update_row('to_be_advisor', prof_id, 'Response', 'IsAnAdvisor')
                    print(f"{first} {last} is now your project advisor. Returning to menu...")
                else:
                    print("Your group already has an advisor. Returning to menu...")
            if confirm.lower() == 'n':
                print("Advisor confirmation process cancelled. Returning to menu...")
        exit()

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
                print(f"Invite Has been sent to {member_data['first']} {member_data['last']}.")
                break
            elif confirm.lower() == 'n':
                continue
        exit()

    def request_prof(self):
        request_data = {}
        advisor_req_table = alldata.search('advisor_pending_request')
        persons_table = alldata.search('persons')
        available_prof = persons_table.filter(lambda x: x['type'] == 'faculty')
        while True:
            print("Here is the list of available professors.")
            print(available_prof.table)
            id_advisor = str(input("Please Enter the ID of your potential advisor: "))
            advisor_data = get_data(id_advisor)
            print(f"You're about to invite {advisor_data['first']} {advisor_data['last']} as a advisor of your project.")
            confirm = str(input("Do you wish to confirm? (Y/N): "))
            if confirm.lower() == 'y':
                request_data.update({'ProjectID': self.project_id, 'to_be_advisor': id_advisor, 'Response': 'HasNotRespond', 'Response_date': 'HasNotRespond'})
                advisor_req_table.insert_row(request_data)
                print(f"Invite Has been sent to {advisor_data['first']} {advisor_data['last']}.")
                break
            elif confirm.lower() == 'n':
                continue
        exit()

    def submit_project(self):
        if self.project_mem2 == 'None' or self.project_mem1 == 'None':
            print(f"To submit, your project must have 2 members.")
            return None
        elif self.project_advisor == 'None':
            print("You need an advisor to submit a project.")
            return None
        eval_table = alldata.search('evaluation')
        find_eval = eval_table.filter(lambda x: x['ProjectID'] == self.project_id)
        eval_data = find_eval.table[0]
        project_table = alldata.search('project')
        print("You're now submitting your project.")
        print("This report will get evaluated by your advisor")
        print(f"Report: {eval_data['Report']}")
        while True:
            confirm = str(input("Do you wish to submit your project? (Y/N): "))
            if confirm.lower() == 'y':
                project_table.update_row("ProjectID", self.project_id, "Status", 'WaitingForApproval')
                print(f"Your report has been sent to your advisor.")
                break
            elif confirm.lower() == 'n':
                print("Returning to menu...")
                break

    def modify_project(self):
        project_table = alldata.search('project')
        find_project = project_table.filter(lambda x: x['ProjectID'] == self.project_id)
        eval_table = alldata.search('evaluation')

        while True:
            print("What do you want to do?")
            print("1. Change the project title.")
            print("2. Write a report. (replacing the old one)")
            print("3. Return to menu.")
            choice = str(input("Enter your choice: "))
            if choice == '1':
                print()
                new_title = str(input("Enter your new project title: "))
                print(f"You're changing the project title from {self.project_title} to {new_title}")
                while True:
                    confirm = str(input("Are you sure? (Y/N): "))
                    if confirm.lower() == 'y':
                        project_table.update_row('ProjectID', self.project_id, 'Title', new_title)
                        print(f"Your new project title is {find_project.table[0]['Title']}")
                        break
                    elif confirm.lower() == 'n':
                        print("Project title changing process has been cancelled. Returning to menu...")
                        break
                    else:
                        print("Invalid input. Try again.")
                break
            elif choice == '2':
                print()
                print("You're now writing a new report.")
                new_report = str(input("Write down your report: "))
                print(f"This is your new report: {new_report}")
                while True:
                    confirm = str(input("Are you sure? (Y/N): "))
                    if confirm.lower() == 'y':
                        eval_table.update_row('ProjectID', self.project_id, 'Report', new_report)
                        print(f"Your new project report has been updated. Returning to menu...")
                        break
                    elif confirm.lower() == 'n':
                        print("Project title changing process has been cancelled. Returning to menu...")
                        break
                    else:
                        print("Invalid input. Try again.")
                break
            elif choice == '3':
                print()
                print("Returning to menu...")
                break
            else:
                print("Choice Invalid. Try again.")
                print()

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
            print("6. Submit your project.")
            print("7. Logout")
            choice = str(input("Enter your choice: "))
            if choice == '1':
                print()
                self.check_status()
            elif choice == '2':
                print()
                self.modify_project()
            elif choice == '3':
                print()
                self.check_inbox()
            elif choice == '4':
                print()
                self.invite_members()
            elif choice == '5':
                print()
                self.request_prof()
            elif choice == '6':
                print()
                self.submit_project()
            elif choice == '7':
                print("You have logged out.")
                break
            else:
                print("Choice Invalid. Try again.")
                print()
            print()


class Member:
    def __init__(self, data):
        self.data = data
        self.id = data['ID']
        self.first = data['first']
        self.last = data['last']
        self.type = data['type']
        project_table = alldata.search('project')
        find_project = project_table.filter(lambda x: x['Member1'] == self.id or x['Member2'] == self.id)
        self.lead_id = find_project.table[0]['Lead']
        self.project_data = get_project(self.lead_id)
        self.project_id = self.project_data['ProjectID']
        self.project_title = self.project_data['Title']
        self.project_lead = self.project_data['Lead']
        self.project_mem1 = self.project_data['Member1']
        self.project_mem2 = self.project_data['Member2']
        self.project_advisor = self.project_data['Advisor']
        self.project_status = self.project_data['Status']
        self.pending_request = {}
        self.run()

    def __str__(self):
        return (f"You logged in as {self.first} {self.last}. \n"
                f"You are a {self.type}.")

    def modify_project(self):
        project_table = alldata.search('project')
        find_project = project_table.filter(lambda x: x['ProjectID'] == self.project_id)
        eval_table = alldata.search('evaluation')

        while True:
            print("What do you want to do?")
            print("1. Change the project title.")
            print("2. Write a report. (replacing the old one)")
            print("3. Return to menu.")
            choice = str(input("Enter your choice: "))
            if choice == '1':
                print()
                new_title = str(input("Enter your new project title: "))
                print(f"You're changing the project title from {self.project_title} to {new_title}")
                while True:
                    confirm = str(input("Are you sure? (Y/N): "))
                    if confirm.lower() == 'y':
                        project_table.update_row('ProjectID', self.project_id, 'Title', new_title)
                        print(f"Your new project title is {find_project.table[0]['Title']}")
                        break
                    elif confirm.lower() == 'n':
                        print("Project title changing process has been cancelled. Returning to menu...")
                        break
                    else:
                        print("Invalid input. Try again.")
                break
            elif choice == '2':
                print()
                print("You're now writing a new report.")
                new_report = str(input("Write down your report: "))
                print(f"This is your new report: {new_report}")
                while True:
                    confirm = str(input("Are you sure? (Y/N): "))
                    if confirm.lower() == 'y':
                        eval_table.update_row('ProjectID', self.project_id, 'Report', new_report)
                        print(f"Your new project report has been updated. Returning to menu...")
                        break
                    elif confirm.lower() == 'n':
                        print("Project title changing process has been cancelled. Returning to menu...")
                        break
                    else:
                        print("Invalid input. Try again.")
                break
            elif choice == '3':
                print()
                print("Returning to menu...")
                break
            else:
                print("Choice Invalid. Try again.")
                print()

    def check_status(self):
        get_lead_data = get_data(self.project_lead)
        get_mem1_data = get_data(self.project_mem1)
        get_mem2_data = get_data(self.project_mem2)
        get_advisor_data = get_data(self.project_advisor)
        eval_table = alldata.search('evaluation')
        find_eval = eval_table.filter(lambda x: x['ProjectID'] == self.project_id)
        eval_data = find_eval.table[0]
        print("You are now viewing your project status.")
        print()
        print(f"ProjectID : {self.project_id}")
        print(f"Title : {self.project_title}")
        print(f"Leader : {get_lead_data['first']} {get_lead_data['last']} ({self.project_lead})")
        print(f"Member1 : {get_mem1_data['first']} {get_mem1_data['last']} ({self.project_mem1})")
        print(f"Member2 : {get_mem2_data['first']} {get_mem2_data['last']} ({self.project_mem2})")
        print(f"Advisor : {get_advisor_data['first']} {get_advisor_data['last']} ({self.project_advisor})")
        print(f"Project Report: {eval_data['Report']}")
        print(f"Project Score: {eval_data['Score']}")
        print(f"Note from advisor: {eval_data['Note']}")
        print(f"Project Status : {self.project_status}")

    def run(self):
        print(self)
        print()
        while True:
            print("You have permission to do the following:")
            print("1. See project status.")
            print("2. Modify project.")
            print("3. Logout.")
            choice = str(input("Enter your choice: "))
            if choice == '1':
                print()
                self.check_status()
            elif choice == '2':
                print()
                self.modify_project()
            elif choice == '3':
                print()
                print("You have logged out.")
                break
            else:
                print("Choice Invalid. Try again.")
                print()
            print()


class Faculty:
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

    def eva_project(self):
        print("You're now evaluating a project.")
        project_table = alldata.search('project')
        find_ready = project_table.filter(lambda x: x['Advisor'] != self.id).filter(lambda x: x['Status'] == 'WaitingForApproval')
        while True:
            print("Here is a list of projects that are ready for evaluation.")
            print(find_ready.select(["ProjectID", "Title"]))
            enter_id = str(input("Enter a ProjectID: "))
            find_project = project_table.filter(lambda x: x['ProjectID'] == enter_id)
            print(find_project)
            if find_project != []:
                print()
                break
            print('Invalid ID.')

        project_data = get_project_projectID(enter_id)
        project_id = project_data['ProjectID']
        project_title = project_data['Title']
        project_lead = project_data['Lead']
        project_mem1 = project_data['Member1']
        project_mem2 = project_data['Member2']
        project_advisor = project_data['Advisor']

        eval_table = alldata.search('evaluation')
        find_eval = eval_table.filter(lambda x: x['ProjectID'] == project_id)
        eval_data = find_eval.table[0]
        print()
        print(f"Title: {project_title}")
        print(f"Project Leader: {project_lead}")
        print(f"Member 1: {project_mem1}")
        print(f"Member 2: {project_mem2}")
        print(f"Advisor: {project_advisor}")
        print(f"Report: {eval_data['Report']}")
        print()
        while True:
            eval_choose = str(input("What is your evaluation for this project? (fail/pass): "))
            if eval_choose.lower() == 'fail' or eval_choose.lower() == 'pass':
                break
            else:
                print("Invalid choice.")
                continue
        if eval_choose.lower() == 'fail':
            result = 'Failed'
        else:
            result = 'Passed'
        print(f"Your evaluation for project({project_title}) is {result}.")
        while True:
            confirm = str(input("Do you wish to confirm your evaluation? (Y/N): "))
            if confirm.lower() == 'y':
                eval_table.update_row('ProjectID', project_id, 'Eva1', result)
                print(f"Your evaluation has been confirmed. Returning to menu...")
                break
            elif confirm.lower() == 'n':
                print("Project evaluation process has been cancelled. Returning to menu...")
                break
            else:
                print("Invalid input. Try again.")

    def check_any_status(self):
        print("You're now checking status of a project.")
        project_table = alldata.search('project')
        while True:
            print("Here is a list of projects.")
            print(project_table.select(["ProjectID", "Title"]))
            enter_id = str(input("Enter a ProjectID: "))
            find_project = project_table.filter(lambda x: x['ProjectID'] == enter_id)
            print(find_project)
            if find_project != []:
                print()
                break
            print('Invalid ID.')

        project_data = get_project_projectID(enter_id)
        project_id = project_data['ProjectID']
        project_title = project_data['Title']
        project_lead = project_data['Lead']
        project_mem1 = project_data['Member1']
        project_mem2 = project_data['Member2']
        project_advisor = project_data['Advisor']
        project_status = project_data['Status']

        get_lead_data = get_data(project_lead)
        get_mem1_data = get_data(project_mem1)
        get_mem2_data = get_data(project_mem2)
        get_advisor_data = get_data(project_advisor)
        eval_table = alldata.search('evaluation')
        find_eval = eval_table.filter(lambda x: x['ProjectID'] == project_id)
        eval_data = find_eval.table[0]
        print("You are now viewing the project status.")
        print()
        print(f"ProjectID : {project_id}")
        print(f"Title : {project_title}")
        print(f"Leader : {get_lead_data['first']} {get_lead_data['last']} ({project_lead})")
        print(f"Member1 : {get_mem1_data['first']} {get_mem1_data['last']} ({project_mem1})")
        print(f"Member2 : {get_mem2_data['first']} {get_mem2_data['last']} ({project_mem2})")
        print(f"Advisor : {get_advisor_data['first']} {get_advisor_data['last']} ({project_advisor})")
        print(f"Project Report: {eval_data['Report']}")
        print(f"Project Score: {eval_data['Score']}")
        print(f"Note from advisor: {eval_data['Note']}")
        print(f"Project Status : {project_status}")

    def check_inbox(self):
        project_table = alldata.search('project')
        pending_req_table = alldata.search('advisor_pending_request')
        find_req = pending_req_table.filter(lambda x: x['to_be_advisor'] == self.id)
        print(f"You have {len(find_req.table)} pending request(s).")
        for data in find_req.table:
            find_project = project_table.filter(lambda x: x['ProjectID'] == data['ProjectID'])
            project_data = find_project.table[0]
            get_leader = get_data(project_data['Lead'])
            print(f"{get_leader['first']} {get_leader['last']} has requested you to be an advisor for their project group.")
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
                find_req.update_row('to_be_advisor', self.id, 'Response', 'Accept')
                find_req.update_row('to_be_advisor', self.id, 'Response_date', datetime.date.today())
                adv_req_table = alldata.search('advisor_pending_request')
                find_other_req = adv_req_table.filter(lambda x: x['Response'] == 'HasNotRespond')
                find_other_req.update_row('to_be_advisor', self.id, 'Response', 'Deny')
                find_other_req.update_row('to_be_advisor', self.id, 'Response_date', datetime.date.today())
                print(f"You have accepted the request to projectID({project_res}).")
                print("Returning to menu...")
                break
            elif response.lower() == 'deny':
                find_req.update_row('to_be_advisor', self.id, 'Response', 'Deny')
                find_req.update_row('to_be_advisor', self.id, 'Response_date', datetime.date.today())
                print(find_req.table)
                print(f"You have denied the request to projectID({project_res}).")
                print("Returning to menu...")
                break
            elif response.lower() != 'accept' or response.lower() != 'deny':
                print("Your response is invalid. Tryagain.")
                continue
        exit()

    def run(self):
        print(self)
        print()
        while True:
            print("You have permission to do the following:")
            print("1. Check inbox.")
            print("2. Evaluate a project.")
            print("3. View any project status.")
            print("4. Logout.")

            choice = str(input("Enter your choice: "))
            if choice == '1':
                print()
                self.check_inbox()
            elif choice == '2':
                print()
                self.eva_project()
            elif choice == '3':
                print()
                self.check_any_status()
            elif choice == '4':
                print()
                print("You have logged out.")
                break
            else:
                print("Choice Invalid. Try again.")
                print()
            print()


class Advisor:
    def __init__(self, data):
        self.data = data
        self.id = data['ID']
        self.first = data['first']
        self.last = data['last']
        self.type = data['type']
        project_table = alldata.search('project')
        find_project = project_table.filter(lambda x: x['Advisor'] == self.id)
        self.lead_id = find_project.table[0]['Lead']
        self.project_data = get_project(self.lead_id)
        self.project_id = self.project_data['ProjectID']
        self.project_title = self.project_data['Title']
        self.project_lead = self.project_data['Lead']
        self.project_mem1 = self.project_data['Member1']
        self.project_mem2 = self.project_data['Member2']
        self.project_advisor = self.project_data['Advisor']
        self.project_status = self.project_data['Status']
        self.pending_request = {}
        self.run()

    def __str__(self):
        return (f"You logged in as {self.first} {self.last}. \n"
                f"You are a {self.type}.")

    def eva_project(self):
        print("You're now evaluating a project.")
        project_table = alldata.search('project')
        find_ready = project_table.filter(lambda x: x['Advisor'] != self.id).filter(
            lambda x: x['Status'] == 'WaitingForApproval')
        while True:
            print("Here is a list of projects that are ready for evaluation.")
            print(find_ready.select(["ProjectID", "Title"]))
            enter_id = str(input("Enter a ProjectID: "))
            find_project = project_table.filter(lambda x: x['ProjectID'] == enter_id)
            print(find_project)
            if find_project != []:
                print()
                break
            print('Invalid ID.')

        project_data = get_project_projectID(enter_id)
        project_id = project_data['ProjectID']
        project_title = project_data['Title']
        project_lead = project_data['Lead']
        project_mem1 = project_data['Member1']
        project_mem2 = project_data['Member2']
        project_advisor = project_data['Advisor']

        eval_table = alldata.search('evaluation')
        find_eval = eval_table.filter(lambda x: x['ProjectID'] == project_id)
        eval_data = find_eval.table[0]
        print()
        print(f"Title: {project_title}")
        print(f"Project Leader: {project_lead}")
        print(f"Member 1: {project_mem1}")
        print(f"Member 2: {project_mem2}")
        print(f"Advisor: {project_advisor}")
        print(f"Report: {eval_data['Report']}")
        print()
        while True:
            eval_choose = str(input("What is your evaluation for this project? (fail/pass): "))
            if eval_choose.lower() == 'fail' or eval_choose.lower() == 'pass':
                break
            else:
                print("Invalid choice.")
                continue
        if eval_choose.lower() == 'fail':
            result = 'Failed'
        else:
            result = 'Passed'
        print(f"Your evaluation for project({project_title}) is {result}.")
        while True:
            confirm = str(input("Do you wish to confirm your evaluation? (Y/N): "))
            if confirm.lower() == 'y':
                eval_table.update_row('ProjectID', project_id, 'Eva1', result)
                print(f"Your evaluation has been confirmed. Returning to menu...")
                break
            elif confirm.lower() == 'n':
                print("Project evaluation process has been cancelled. Returning to menu...")
                break
            else:
                print("Invalid input. Try again.")

    def check_any_status(self):
        print("You're now evaluating a project.")
        project_table = alldata.search('project')
        while True:
            print("Here is a list of projects.")
            print(project_table.select(["ProjectID", "Title"]))
            enter_id = str(input("Enter a ProjectID: "))
            find_project = project_table.filter(lambda x: x['ProjectID'] == enter_id)
            print(find_project)
            if find_project != []:
                print()
                break
            print('Invalid ID.')

        project_data = get_project_projectID(enter_id)
        project_id = project_data['ProjectID']
        project_title = project_data['Title']
        project_lead = project_data['Lead']
        project_mem1 = project_data['Member1']
        project_mem2 = project_data['Member2']
        project_advisor = project_data['Advisor']
        project_status = project_data['Status']

        get_lead_data = get_data(project_lead)
        get_mem1_data = get_data(project_mem1)
        get_mem2_data = get_data(project_mem2)
        get_advisor_data = get_data(project_advisor)
        eval_table = alldata.search('evaluation')
        find_eval = eval_table.filter(lambda x: x['ProjectID'] == project_id)
        eval_data = find_eval.table[0]
        print("You are now viewing the project status.")
        print()
        print(f"ProjectID : {project_id}")
        print(f"Title : {project_title}")
        print(f"Leader : {get_lead_data['first']} {get_lead_data['last']} ({project_lead})")
        print(f"Member1 : {get_mem1_data['first']} {get_mem1_data['last']} ({project_mem1})")
        print(f"Member2 : {get_mem2_data['first']} {get_mem2_data['last']} ({project_mem2})")
        print(f"Advisor : {get_advisor_data['first']} {get_advisor_data['last']} ({project_advisor})")
        print(f"Project Report: {eval_data['Report']}")
        print(f"Project Score: {eval_data['Score']}")
        print(f"Note from advisor: {eval_data['Note']}")
        print(f"Project Status : {project_status}")

    def check_inbox(self):
        project_table = alldata.search('project')
        find_req = project_table.filter(lambda x: x['Status'] == 'WaitingForApproval')
        eval_table = alldata.search('evaluation')
        find_eval = eval_table.filter(lambda x: x['ProjectID'] == self.project_id).filter(lambda x: x['Eva1'] == 'Passed')
        eval_data = find_eval.table[0]
        print(f"You have {len(find_eval.table)} pending request for approval.")
        if len(find_eval.table) == 0:
            print("Returning to menu...")
            return None
        print()
        print(f"Title: {self.project_title}")
        print(f"Project Leader: {self.project_lead}")
        print(f"Member 1: {self.project_mem1}")
        print(f"Member 2: {self.project_mem2}")
        print(f"Report: {eval_data['Report']}")
        print()
        while True:
            score = int(input("Please grade this project report out of 100 (use integers): "))
            if 0 <= score <=100:
                break
            print(f"Score must be within 0-100")
        if score >= 70:
            result = 'Approved'
        else:
            result = 'Disapproved'
        print(f"You graded the project {score} out of 100. The project will be {result}.")
        note = str(input("Please enter your comment/advise on the project: "))
        while True:
            confirm = str(input("Do you wish to confirm your evaluation? (Y/N): "))
            if confirm.lower() == 'y':
                eval_table.update_row('ProjectID', self.project_id, 'Score', score)
                eval_table.update_row('ProjectID', self.project_id, 'Note', note)
                project_table.update_row('ProjectID', self.project_id, 'Status', result)
                print(f"Your evaluation has been confirmed. Returning to menu...")
                break
            elif confirm.lower() == 'n':
                print("Project evaluation process has been cancelled. Returning to menu...")
                break
            else:
                print("Invalid input. Try again.")

    def check_status(self):
        get_lead_data = get_data(self.project_lead)
        get_mem1_data = get_data(self.project_mem1)
        get_mem2_data = get_data(self.project_mem2)
        get_advisor_data = get_data(self.project_advisor)
        eval_table = alldata.search('evaluation')
        find_eval = eval_table.filter(lambda x: x['ProjectID'] == self.project_id)
        eval_data = find_eval.table[0]
        print("You are now viewing your project status.")
        print()
        print(f"ProjectID : {self.project_id}")
        print(f"Title : {self.project_title}")
        print(f"Leader : {get_lead_data['first']} {get_lead_data['last']} ({self.project_lead})")
        print(f"Member1 : {get_mem1_data['first']} {get_mem1_data['last']} ({self.project_mem1})")
        print(f"Member2 : {get_mem2_data['first']} {get_mem2_data['last']} ({self.project_mem2})")
        print(f"Advisor : {get_advisor_data['first']} {get_advisor_data['last']} ({self.project_advisor})")
        print(f"Project Report: {eval_data['Report']}")
        print(f"Project Score: {eval_data['Score']}")
        print(f"Note from advisor: {eval_data['Note']}")
        print(f"Project Status : {self.project_status}")

    def run(self):
        print(self)
        print()
        while True:
            print("You have permission to do the following:")
            print("1. Check inbox (for project approval).")
            print("2. See project status.")
            print("3. Check any project status.")
            print("4. Evaluate a project (that is not advised by you): ")
            print("5. Logout.")
            choice = str(input("Enter your choice: "))
            if choice == '1':
                print()
                self.check_inbox()
            elif choice == '2':
                print()
                self.check_status()
            elif choice == '3':
                print()
                self.check_any_status()
            elif choice == '4':
                print()
                self.eva_project()
            elif choice == '5':
                print()
                print("You have logged out.")
                break
            else:
                print("Choice Invalid. Try again.")
                print()
            print()


class Admin:
    def __init__(self, data):
        self.data = data
        self.id = data['ID']
        self.first = data['first']
        self.last = data['last']
        self.type = data['type']

        self.run()

    def __str__(self):
        return (f"You logged in as {self.first} {self.last}. \n"
                f"You are a {self.type}.")

    def remove_person(self):
        print("You're now removing a person from a project.")
        project_table = alldata.search('project')
        print("List of projects.")
        print(project_table.table)
        project_allID = project_table.select('ProjectID')
        while True:
            project_choose = str(input("Please enter the projectID you want to remove a person from: "))
            project_exists = False
            for project in project_allID:
                if project['ProjectID'] == project_choose:
                    project_exists = True
                    break
            if project_exists:
                break
            else:
                print(f"Invalid ProjectID.")
        project_find = project_table.filter(lambda x: x['ProjectID'] == project_choose)
        project_data = get_project_projectID(project_choose)
        project_id = project_data['ProjectID']
        project_title = project_data['Title']
        project_lead = project_data['Lead']
        project_mem1 = project_data['Member1']
        project_mem2 = project_data['Member2']
        project_advisor = project_data['Advisor']
        project_status = project_data['Status']

        get_lead_data = get_data(project_lead)
        get_mem1_data = get_data(project_mem1)
        get_mem2_data = get_data(project_mem2)
        get_advisor_data = get_data(project_advisor)
        eval_table = alldata.search('evaluation')
        find_eval = eval_table.filter(lambda x: x['ProjectID'] == project_id)
        eval_data = find_eval.table[0]
        while True:
            person_to_remove = str(input("Which person do you want to remove from this project (Leader, Member1, Member2, Advisor): "))
            if person_to_remove.lower() == 'leader':
                print()
                print("You're removing the project Leader the project will be disbanded. Are you sure?")
                while True:
                    confirm = str(input("Do you wish to confirm your action? (Y/N): "))
                    if confirm.lower() == 'y':
                        self.nuke_project(project_id)
                        print()
                        print(f"You nuked project({project_choose}) all associate roles are reverted and data are all gone.")
                        print(f"Your action has consequences. Returning to menu...")
                        break
                    elif confirm.lower() == 'n':
                        print("Your action has been cancelled. Returning to menu...")
                        break
                    else:
                        print("Invalid input. Try again.")

            elif person_to_remove.lower() == 'member1':
                print()
                print(f"You're removing {get_mem1_data['first']} {get_mem1_data['last']} from the project. Are you sure?")
                while True:
                    confirm = str(input("Do you wish to confirm your action? (Y/N): "))
                    if confirm.lower() == 'y':
                        self.remove_a_member(project_choose, get_mem1_data['ID'], 'student')
                        print()
                        print(
                            f"You removed {get_mem1_data['first']} {get_mem1_data['last']} from project({project_choose}).")
                        print(f"Your action has consequences. Returning to menu...")
                        break
                    elif confirm.lower() == 'n':
                        print("Your action has been cancelled. Returning to menu...")
                        break
                    else:
                        print("Invalid input. Try again.")

            elif person_to_remove.lower() == 'member2':
                print()
                print(f"You're removing {get_mem2_data['first']} {get_mem2_data['last']} from the project. Are you sure")
                while True:
                    confirm = str(input("Do you wish to confirm your action? (Y/N): "))
                    if confirm.lower() == 'y':
                        self.remove_a_member(project_choose, get_mem2_data['ID'], 'student')
                        print()
                        print(
                            f"You removed {get_mem2_data['first']} {get_mem2_data['last']} from project({project_choose}).")
                        print(f"Your action has consequences. Returning to menu...")
                        break
                    elif confirm.lower() == 'n':
                        print("Your action has been cancelled. Returning to menu...")
                        break
                    else:
                        print("Invalid input. Try again.")

            elif person_to_remove.lower() == 'advisor':
                print()
                print(f"You're removing {get_advisor_data['first']} {get_advisor_data['last']} from the project. Are you sure? ")
                while True:
                    confirm = str(input("Do you wish to confirm your action? (Y/N): "))
                    if confirm.lower() == 'y':
                        self.remove_a_member(project_choose, get_advisor_data['ID'], 'faculty')
                        print()
                        print(
                            f"You removed {get_advisor_data['first']} {get_advisor_data['last']} from project({project_choose}).")
                        print(f"Your action has consequences. Returning to menu...")
                        break
                    elif confirm.lower() == 'n':
                        print("Your action has been cancelled. Returning to menu...")
                        break
                    else:
                        print("Invalid input. Try again.")
            else:
                print("Invalid Input.")
            break

    def remove_a_member(self, projectID ,memberID, newrole):

        project_data = get_project_projectID(projectID)
        project_title = project_data['Title']
        project_lead = project_data['Lead']
        project_mem1 = project_data['Member1']
        project_mem2 = project_data['Member2']
        project_advisor = project_data['Advisor']
        project_status = project_data['Status']

        get_mem1_data = get_data(project_mem1)
        get_mem2_data = get_data(project_mem2)
        get_advisor_data = get_data(project_advisor)

        eval_table = alldata.search('evaluation')
        find_eval = eval_table.filter(lambda x: x['ProjectID'] == projectID)
        eval_data = find_eval.table[0]

        project_table = alldata.search('project')
        project_find = project_table.filter(lambda x: x['ProjectID'] == projectID)
        get_target_data = get_data(memberID)

        if get_target_data['type'] == 'member':
            member_pending = alldata.search('member_pending_request')
            member_pending_find = member_pending.filter(lambda x: x['ProjectID'] == projectID)
            if memberID == get_mem1_data['ID']:
                project_find.update_row("ProjectID", projectID, "Member1", 'None')
                member_pending_find.update_row('to_be_member', memberID, 'Response', 'None')
                member_pending_find.update_row('to_be_member', memberID, 'Response_date', 'None')
                member_pending_find.update_row('to_be_member', memberID, 'ProjectID', 'None')
                member_pending_find.update_row('to_be_member', memberID, 'to_be_member', 'None')
            elif memberID == get_mem2_data['ID']:
                project_find.update_row("ProjectID", projectID, "Member2", 'None')
                member_pending_find.update_row('to_be_member', memberID, 'Response', 'None')
                member_pending_find.update_row('to_be_member', memberID, 'Response_date', 'None')
                member_pending_find.update_row('to_be_member', memberID, 'ProjectID', 'None')
                member_pending_find.update_row('to_be_member', memberID, 'to_be_member', 'None')

        if get_target_data['type'] == 'advisor':
            advisor_pending = alldata.search('advisor_pending_request')
            advisor_find = advisor_pending.filter(lambda x: x['ProjectID'] == projectID)
            advisor_find.update_row('ProjectID', projectID, 'to_be_advisor', 'None')
            advisor_find.update_row('ProjectID', projectID, 'Response', 'None')
            advisor_find.update_row('ProjectID', projectID, 'Response_date', 'None')
            advisor_find.update_row('ProjectID', projectID, 'ProjectID', 'None')
            project_find.update_row("ProjectID", projectID, "Advisor", 'None')
        change_role(memberID, newrole)

    def nuke_project(self, projectID):
        project_data = get_project_projectID(projectID)
        project_id = project_data['ProjectID']
        project_lead = project_data['Lead']
        project_mem1 = project_data['Member1']
        project_mem2 = project_data['Member2']
        project_advisor = project_data['Advisor']

        eval_table = alldata.search('evaluation')
        find_eval = eval_table.filter(lambda x: x['ProjectID'] == project_id)


        member_pending = alldata.search('member_pending_request')
        member_pending_find = member_pending.filter(lambda x: x['ProjectID'] == projectID)
        member_pending_find.update_row('ProjectID', projectID, 'to_be_member', 'Nuked')
        member_pending_find.update_row('ProjectID', projectID, 'Response', 'Nuked')
        member_pending_find.update_row('ProjectID', projectID, 'Response_date', 'Nuked')
        member_pending_find.update_row('ProjectID', projectID, 'ProjectID', 'Nuked')

        advisor_pending = alldata.search('advisor_pending_request')
        advisor_find = advisor_pending.filter(lambda x: x['ProjectID'] == projectID)
        advisor_find.update_row('ProjectID', projectID, 'to_be_advisor', 'Nuked')
        advisor_find.update_row('ProjectID', projectID, 'Response', 'Nuked')
        advisor_find.update_row('ProjectID', projectID, 'Response_date', 'Nuked')
        advisor_find.update_row('ProjectID', projectID, 'ProjectID', 'Nuked')

        find_eval.update_row("ProjectID", projectID, "Report", "Project Nuked")
        find_eval.update_row("ProjectID", projectID, "Score", "Project Nuked")
        find_eval.update_row("ProjectID", projectID, "Eva1", "Project Nuked")
        find_eval.update_row("ProjectID", projectID, "Note", "Project Nuked")
        find_eval.update_row("ProjectID", projectID, "ProjectID", "Project Nuked")

        project_table = alldata.search('project')
        project_find = project_table.filter(lambda x: x['ProjectID'] == projectID)

        change_role(project_lead, 'student')
        change_role(project_mem1, 'student')
        change_role(project_mem2, 'student')
        change_role(project_advisor, 'faculty')
        project_find.update_row("ProjectID", projectID, "Lead", "Nuked")
        project_find.update_row("ProjectID", projectID, "Member1", "Nuked")
        project_find.update_row("ProjectID", projectID, "Member2", "Nuked")
        project_find.update_row("ProjectID", projectID, "Advisor", "Nuked")
        project_find.update_row("ProjectID", projectID, "Title", "Nuked")
        project_find.update_row("ProjectID", projectID, "Status", "Nuked")
        project_find.update_row("ProjectID", projectID, "ProjectID", "Nuked")


    def change_login_data(self):
        print("You're now changing login data.")
        persons_table = alldata.search('persons')
        while True:
            first = str(input("Enter the first name of your target: "))
            last = str(input("Enter the last name of your target: "))
            find_person = persons_table.filter(lambda x: x['first'] == first).filter(lambda x: x['last'] ==last)
            if find_person != []:
                break
            print("Error: person not found. Try again.")
            print()
        person_data = find_person.table[0]
        person_id = person_data['ID']
        person_first = person_data['first']
        person_last = person_data['last']
        person_role = person_data['type']

        login_table = alldata.search('login')
        login_find = login_table.filter(lambda x: x['ID'] == person_id)
        print()
        while True:
            print(f"Which data of {person_first} {person_last} do you want to change?:")
            print(f"Note: If you want to revert their roles you can do so by removing them from a project.")
            print("1. Change their username.")
            print("2. Change their password.")
            print("3. Return to main menu.")
            choice = str(input("Enter your choice: "))
            if choice == '1':
                while True:
                    print()
                    new_user_name = str(input("Enter their new user name: "))
                    if new_user_name != '' and not new_user_name.isspace() and len(new_user_name) <= 16:
                        break
                    print("Username must not be an empty string and not longer than 16 characters!")
                while True:
                    print()
                    print(f"You're about to change {person_first} {person_last}'s username to {new_user_name}")
                    while True:
                        confirm = str(input("Do you wish to confirm your action? (Y/N): "))
                        if confirm.lower() == 'y':
                            login_table.update_row("ID", person_id, "username", new_user_name)
                            print(f"Successfully change their username to {new_user_name}")
                            print(f"Your action has consequences. Returning to menu...")
                            break
                        elif confirm.lower() == 'n':
                            print("Your action has been cancelled. Returning to menu...")
                            break
                        else:
                            print("Invalid input. Try again.")
                    break

            elif choice == '2':
                print()
                while True:
                    print()
                    new_pass = str(input("Enter their new password: "))
                    if new_pass != '' and not new_pass.isspace() and len(new_pass) == 4:
                        break
                    print("Password must not be an empty string and must be 4 digits!")
                while True:
                    print()
                    print(f"You're about to change {person_first} {person_last}'s password to {new_pass}")
                    while True:
                        confirm = str(input("Do you wish to confirm your action? (Y/N): "))
                        if confirm.lower() == 'y':
                            login_table.update_row("ID", person_id, "password", new_pass)
                            print(f"Successfully change their password to {new_pass}")
                            print(f"Your action has consequences. Returning to menu...")
                            break
                        elif confirm.lower() == 'n':
                            print("Your action has been cancelled. Returning to menu...")
                            break
                        else:
                            print("Invalid input. Try again.")
                    break

            elif choice == '3':
                print()
                print("Returning to main menu....")
                break
            else:
                print("Choice Invalid. Try again.")
                print()
            print()

    def run(self):
        print(self)
        print()
        while True:
            print("You have permission to do the following:")
            print("1. Remove a person from a project.")
            print("2. Change login data.")
            print("3. Logout.")
            choice = str(input("Enter your choice: "))
            if choice == '1':
                print()
                self.remove_person()
            elif choice == '2':
                print()
                self.change_login_data()
            elif choice == '3':
                print()
                print("You have logged out.")
                break
            else:
                print("Choice Invalid. Try again.")
                print()
            print()


# define a function called exit
def exit():
    tables = {
        'login': 'login.csv',
        'persons': 'persons.csv',
        'project': 'project.csv',
        'advisor_pending_request': 'advisor_pending_request.csv',
        'member_pending_request': 'member_pending_request.csv',
        'evaluation': 'evaluation.csv'
    }

    field_names = {
        'login': ['ID', 'username', 'password', 'role'],
        'persons': ['ID', 'first', 'last', 'type'],
        'project': ['ProjectID', "Title", "Lead", 'Member1', 'Member2', 'Advisor', 'Status'],
        'advisor_pending_request': ['ProjectID', 'to_be_advisor', 'Response', 'Response_date'],
        'member_pending_request': ['ProjectID', 'to_be_member', 'Response', 'Response_date'],
        'evaluation': ['ProjectID', 'Report', 'Score', 'Note', 'Eva1']
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
    admin1 = Admin(user_data)
elif val[1] == 'student':
    #see and do student related activities
    student1 = Student(user_data)
elif val[1] == 'member':
    #see and do member related activities
    member1 = Member(user_data)
elif val[1] == 'lead':
    leader1 = Leader(user_data)
elif val[1] == 'faculty':
    #see and do faculty related activities
    faculty1 = Faculty(user_data)
elif val[1] == 'advisor':
    #see and do advisor related activities
    advisor1 = Advisor(user_data)



# once everyhthing is done, make a call to the exit function
exit()
