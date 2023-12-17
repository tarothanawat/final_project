What needs to be done.

Create Tables to store different data types.

    Person(keys): ID, First(name), Last(name), Type(Role)
    Login(keys): ID, Username, Password, Role
    Project(keys): ProjectID, Title, Lead, Member1, Member2, Adviser, Status
    Advisor_pending_request(keys): ProjectID, to_be_advisor, Response, Response_date
    Member_pending_request(keys): ProjectID, to_be_member, Response, Response_date

What should be displayed when we login as each roles?

1.[**Student**]


  - Student: (Normal student)
    - See if there are pending requests to become members of already created projects
    - Accept or deny the requests
      - Member_pending_request table needs to be updated
      - Project table needs to be updated
    - Create a project and become a lead; must deny all member requests first
        - Project table needs to be updated
        - Login table needs to be updated
        - If more members needed, send out requests nd update the member_pending_request table; requests can only go to those whose role is student, i.e., not yet become a member or a lead
  - Lead student: (must not already be a member of any project)
    - Can create a project
    - See project status (pending member, pending advisor, or ready to solicit an advisor)
    - See and modify project information.
      - Project table needs to be updated if modified 
    - See who has responded to the requests sent out
    - Send out requests to potential members
      - update Member_pending_request table
    - Send out requests to a potential advisor; can only do one at a time and after all potential members have accepted or denied the requests
        - Advisor_pending_request table needs to be updated
    
[database.py]
    - needs write csv function.

[project_manage.py]
    - need to implement a way to update data in csv files to table classes.

{Things to do}
- Need to implement denying other request when accepting an invitation or request to be an advisor. :D
- Has a loop-hole where if you deny a prof to be an advisor nothing happens. (Need to make a rule that leaders could only request 1 prof at a time.)
- As a student: when checking inbox user can input any number instead of the one in display.