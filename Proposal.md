{How to submit a project.}
- Lead needs to be the one that submits the project. 
  - Project must have an advisor
  - Project must have 2 members; excluding the leader
- The project status will be changed to 'WaitingForApproval' in the mean time that advisor has not graded the project.
- Any faculty can evaluate the project giving "Passed" or "failed".
- Advisor can only grade the project when the evaluation from other faculty is "Passed".
- Advisor grades the project. Score of 100
  - if score >= 70: 
    - the project's status gets changed to 'Approved'
  - if score < 70:
    - The project's status gets changed to 'Disapproved'

{Advisor class}
- Advisor class is a former faculty class that is advising a project.
  - An advisor can only advise 1 project.
- Advisor can check their inbox for request to evaluate sent by leader of the project.
- Project grading.
  - The project will change status to 'Approved' if score >=70 else: 'Disapproved'
  - If a project is disapproved advisor need to sent them a note on how to improve their project.

{Bugs (there are more, maybe not founded.)}
- {Leader Class}
  - You can not view your project if your project doesn't have 2 members and an advisor already.(It will result in Error.) 
    - - (Fixed); now when get_data can't find a person data it will display as 'None'

- {Member Class}
  - You can not view your project if your project doesn't have 2 members and an advisor already.(It will result in Error.)
    - (Fixed); now when get_data can't find a person data it will display as 'None'

{Modifying a project; class Member and Leader}
- Modifying a project means actions such as....
  - editing project title
  - editing the Report in evaluation.csv

{Admin Class}
- Admin class can do 2 main actions
  - 1. Remove a person from a project.
     - if that person is a {Leader} The project will be disbanded and all data that ties to the project will be "nuked". The Leader's role will be reverted to student.
     - if that person is a {Member} They will be removed from the project all information that ties to them being in the project will be "nuked". Their role will be reverted to student.
     - if that person is an {Advisor} They will be removed from the project all information that ties to them being in the project will be "nuked". Their role will be reverted to faculty.
  - 2. Change login data.
     - The Admin  needs to enter thr first name and last name of the target.
     - Then they choose which to change username or password.
     - Then they enter the new data.
     - The login database gets updated.