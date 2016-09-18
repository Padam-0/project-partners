## README

projpartners.py

Project Partners aims to create groups of students based on diversity among
people.

## Program Structure:

In simplest terms, the program follows the steps below:

1. Import a list of information about students
2. Import a list of previous project partners (optional)
3. Create matrices based on matches of predefined criteria
4. Remove all previous project partners from the list
5. Sum matrices to create 'best' fit fo diversity (least matched criteria)
6. Return list of partners
7. Send an email out to each team informing them
8. Send an email out to unit coordinator informing them

Inputs:

Module Information:

openfile(file):
openfile() takes a text file as an input, with each line containing the
following information in order:
    Email prefix
    First name
    Last name
    Country of Birth
    Undergraduate Qualification (single word)
    Industry Experience (Y/N)
    (if Y) Industry (single word)