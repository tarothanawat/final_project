# Final project for 2023's 219114/115 Programming I
{How to run my project.}
1. Login with username and password
2. After you login you will see a display containing choices you are permitted to do, depending on your roles.
3. You need to logout every time to save changes you made during the run().
4. *Important*
-The login.csv and persons.csv needs to contain "None","None","None","None" basically every key needs to have one row of value ('None')

{Database(csv files)}
1. persons.csv ; contains data of every person (ID,first,last,type)
2. login.csv ; contain login data of all user (ID,username,password,role)
3. project.csv ; contains Project data of created projects (ProjectID,Title,Lead,Member1,Member2,Advisor,Status)
4. member_pending_request.csv ; contains requests by a leader sent to a student to be a member. (ProjectID,to_be_member,Response,Response_date)
5. advisor_pending_request.csv ; contains request made by a leader to a faculty to be their advisor. (ProjectID,to_be_advisor,Response,Response_date)
6. evaluation.csv ; contains Report of a project and their evaluation made by advisor and a faculty, also contains advisor's advice (ProjectID,Report,Score,Note,Eva1)

{Table containing Roles method explanation}
- https://docs.google.com/spreadsheets/d/1MwV1x3g2PI_SKfks3KqMgWudkUkFjfBKzoZ266BrG-o/edit?usp=sharing


{Missing features and bugs}
- There is no real way for user to go back to the main menu immediately after miss inputting a choice. They need to do the action and then choose deny to confirmation to save changes in the end.
- {class Admin} have alot of missing features such as editing a faculty/advisor evaluation on a project.
- Most known bugs are fixed. But there are probably more not found by me.
- There are  loop-holes and test cases that is program didn't cover (I think).
- There are alot of duplicated codes that could've been made into a global function ,but I just forgets it every time I need to use it.
- Nothing is saved until logout (I don't think it's a bug, just kind of weird.)

{Things I learned}
- To plan all things before I start coding. Because there are some problems that could easily be fixed with proper planning beforehand.
- Finish projects before its due date.

{Contact}
- Phone: 065-104-9961
- Discord username : nongtaroyarkginmilo