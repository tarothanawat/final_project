# Final project for 2023's 219114/115 Programming I
### {How to run my project.}
1. Login with username and password
2. After you login you will see a display containing choices you are permitted to do, depending on your roles.
3. You need to logout every time to save changes you made during the run().
4. *Important*
-The login.csv and persons.csv needs to contain "None","None","None","None" basically every key needs to have one row of value ('None')

### {Database(csv files)}
1. persons.csv ; contains data of every person (ID,first,last,type)
2. login.csv ; contain login data of all user (ID,username,password,role)
3. project.csv ; contains Project data of created projects (ProjectID,Title,Lead,Member1,Member2,Advisor,Status)
4. member_pending_request.csv ; contains requests by a leader sent to a student to be a member. (ProjectID,to_be_member,Response,Response_date)
5. advisor_pending_request.csv ; contains request made by a leader to a faculty to be their advisor. (ProjectID,to_be_advisor,Response,Response_date)
6. evaluation.csv ; contains Report of a project and their evaluation made by advisor and a faculty, also contains advisor's advice (ProjectID,Report,Score,Note,Eva1)

### {Classes  and functions in database.py}
- read_csv() ; reads data from csv file can turn it into a dictionary.
- write_csv() ; writes data down from dictionary to csv. (In the end I didn't use this)
- ##### DB class
  - __init__() ; create a list to store a dictionaries as table
  -  insert(table) ; store table in the database object.
  -  search(table_name) ; search for a table.
- ##### Table class
  - __init__() ; takes in dictionary and its name
  - join() ; use to join self with other table
  - filter() ; for finding a specific key and value in a table
  - __is_float ; returns if the element is a float or not as bool
  - aggregate ; for function uses for a key
  - select ; to select some only some attribute from the table
  - insert_row ; append a row in the table
  - update_row ; update a key,value in the table

### {Classes  and functions in project_manage.py}
- initializing() ; reads data from csv then turns it into table classes before putting all of it into the database class
- login() ; takes in username and password then returns the 'ID' and 'role' of that account
- change_role(ID, role) ; takes in 'ID' and 'RoleThatWantToChangeTo' and then change the roles of that ID
- get_data ; return data of a person from the persons table using ID
- get_role ; return the role of that ID
- get_project() ; returns list of project info using leader_id
- get_project_projectID ; returns list of project info using project_id
- exit() ; writes all data of every table in the database back to their csv files
- #### the rest are classes that I already made a table explaining it below.


### {Table containing Roles method explanation}
- https://docs.google.com/spreadsheets/d/1X-sFL7oW2I7UpQNJGZ81lB95ZguudPantS4prVm_Xl8/edit?usp=sharing
- This is a new link because I lost permission on the one I submitted in google classroom.
- If you can't open it please contact me.


### {Missing features and bugs}
- There is no real way for user to go back to the main menu immediately after miss inputting a choice. They need to do the action and then choose deny to confirmation to save changes in the end.
- {class Admin} have alot of missing features such as editing a faculty/advisor evaluation on a project.
- Most known bugs are fixed. But there are probably more not found by me.
- There are  loop-holes and test cases that is program didn't cover (I think).
- There are alot of duplicated codes that could've been made into a global function ,but I just forgets it every time I need to use it.
- Nothing is saved until logout (I don't think it's a bug, just kind of weird.)

### {Things I learned}
- To plan all things before I start coding. Because there are some problems that could easily be fixed with proper planning beforehand.
- Finish projects before its due date.

### {Contact}
- Phone: 065-104-9961
- Discord username : nongtaroyarkginmilo