"""
Want to:
1. Import a list of information about students
2. Import a list of previous project partners (optional)
3. Create matrices based on matches of predefined criteria
4. Remove all previous project partners from the list
5. Sum matrices to create 'best' fit fo diversity (least matched criteria)
6. Return list of partners
7. Send an email out to each team informing them
8. Send an email out to unit coordinator informing them

"""
try:
    import sys
    import smtplib
    import getpass
except ImportError as import_err:
    print(import_err)


def openfile(file):
    """
    Opens a .txt file containing line with student information. Each line
    should contain in this order:
    Email prefix
    First name
    Last name
    Country of Birth
    Undergraduate Qualification (single word)
    Industry Experience (Y/N)
    (if Y) Industry (single word)

    TO DO:
        test if file exists
        test if file has required .txt extension
        return errors if failure

    :param file:
    :return:
    """
    li = []
    # what if file doesn't exist?
    f = open(file, 'r')
    for line in f:
        li.append((line.rstrip()).split(' '))
    f.close()
    return li


def previous_partners():
    previous_partners = input("Is there relevant information about"
                                  "previous project partners? (Y/N):  ").upper()
    while previous_partners != 'Y' and previous_partners != 'N':
        previous_partners = input("That is not a valid response. "
                                  "Please use Y or N to indicate if "
                                  "you would like to include "
                                  "information about previous project "
                                  "partners.\nAlternatively, "
                                  "enter Q to exit:  ").upper()
        if previous_partners == 'Q':
            sys.exit()
    return previous_partners


def getfilename(filename):
    """
    Takes a filename as input, tests if it is a path (by searching for /) and
    if so, removes all information prior to the filename. Tests if the file
    extension .txt is present, if not, appends it.

    :param filename:
    :return:
    """
    c = filename.count('/')
    if c != 0:
        i = filename.replace('/', '|', c - 1).find('/')
        nf = filename[i+1:]
        print(nf)
    else:
        nf = filename

    if nf.endswith('.txt'):
        li = ['../', nf]
    else:
        li = ['../', nf, '.txt']
    return ''.join(li)


def send_email(recipients, subject, message):
    """
    Takes a list of recipients and emails them with a specific subject and
    message.

    :param recipients:
    :return:
    """


def main():
    """
    # This will be used when talking to the user. For now, use a default
    input_file = input("What is the name of the .txt file containing student "
                       "information?")
    student_info = openfile(getfilename(input_file))
    """

    student_info = openfile(getfilename('sample-input'))

    """
    # This will be used when talking to the user. For now, use a default
    if previous_partners() == 'Y':
        input_file1 = input(
            "What is the name of the .txt file containing previous partner "
            "information?")
        prev_partners_info = openfile(getfilename(input_file1))
    """

    prev_partners_info = openfile(getfilename('sample-pp'))

    print(student_info)
    print(prev_partners_info)

    """
    if previous partners == required:
        open file ()
        import previous partners info ()
        close file ()
    for i in criteria:
        create matching matrix of i
    create -1 identity matrix to remove self-matches
    create -1 matrix for previous partners
    combine previous partners matrix ((i * -1) - 1)
    disregard all negative results
    create optimal list ()
    for i in teams:
        email (i)
    email (unit-coord)
    """

    unit_coordinator = [input("Please enter the email prefix of the unit "
                              "coordinator: ")]

    # let teams output be a list of lists,
    # [[team_1_member_1,team_1_member_2],[team_2_member_1,...],...]

    teams = [['peter.adam', 'andy.mcsweeney']]

    for i in teams:
        team_subject = "Your team for ___ assignment"
        team_message = "Hi tm1.name & tm2.name,\n\nYou have been grouped " \
                       "together for this assignment by #autodiverse, " \
                       "the robot that loves creating new, diverse project " \
                       "teams!\n\nThe unit coordinator has been informed " \
                       "that you will be working together for this task, " \
                       "so if you have any issues, please email them at " \
                       + unit_coordinator + "@ucdconnect.ie\n\n#autodiverse " \
                       "wishes you a productive and diverse project experience!"
        send_email(i, team_subject, team_message)

    uc_subject = "Teams for __ assignment"
    uc_message = "Hi uc_name, ..."
    send_email(unit_coordinator, uc_subject, uc_message)


if __name__ == '__main__':
    main()
