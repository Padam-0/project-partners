try:
    import sys
    import smtplib
    import getpass
    import numpy as np
    import os
    import re
except ImportError as import_err:
    print(import_err)

criteria_list = ["CountryOfBirth", "UnderGrad", "IndustryExp", "Industry"]

def openfile(file):
    li = []
    try:
        f = open(file, 'r')
        for line in f:
            li.append((line.rstrip()).split(' '))
        f.close()
        return li
    except:
        o = input("I can't find a file with that name. If you want to quit, "
              "please press Q, if not, please try again:  ").upper()
        if o == 'Q':
            exit(0)
        else:
            openfile(getfilename(o.lower()))


def previous_partners():
    previous_partners = input("Is there relevant information about "
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
    if os.path.join('a','b') == 'a/b':
        #os is unix
        c = filename.count('/')
        if c != 0:
            i = filename.replace('/', '|', c - 1).find('/')
            nf = filename[i + 1:]
        else:
            nf = filename
    else:
        #os is windows
        c = filename.count('\\')
        if c != 0:
            i = filename.replace('\\', '|', c - 1).find('\\')
            nf = filename[i + 1:]
        else:
            nf = filename

    pattern = re.compile(r'\..+$')
    if re.search(pattern, nf) != None:
        a = len(re.findall(pattern, nf)[0])
        nf = nf[:-a]
    nf += '.txt'
    return os.path.join('..',nf)


def send_email(recipients, subject, message):
    """
    Takes a list of recipients and emails them with a specific subject and
    message.

    :param recipients:
    :return:
    """
    server = smtplib.SMTP('smtp.gmail.com', '587') # Connect to gmail
    server.starttls()  # Starts TLS Encryption
    email_acc = 'peter.adam@ucdconnect.ie'
    password = getpass.getpass("Enter the password for %s" % (email_acc))
    server.login(email_acc, password)
    content = "Subject: " + subject + "\n" + message
    server.sendmail(email_acc, recipients, content)
    server.quit()


def create_criteria_matrix(s, criteria):
    ci = criteria_list.index(criteria) + 3
    l = len(s)
    M = np.zeros((l,l))
    # create match data
    for i in range(l):
        for j in range(l):
            if s[i][0] == s[j][0]:
                M[i][j] += 0
            elif s[i][ci] == s[j][ci]:
                if ci == 6 and s[i][ci] == 'NA':
                    # Necessary to not double count lack of industry experience
                    M[i][j] += 0
                else:
                    M[i][j] += 1
            else:
                pass
    return M

def create_pp_matrix(s, p, M):
    l = len(s)
    q = len(p)
    # create match data
    x = 0
    y = 0
    for i in range(q):
        for j in range(l):
            if p[i][0] == s[j][0]:
                x = j
            if p[i][1] == s[j][0]:
                y = j
        if x > 0 or y > 0:
            M[x,y] = abs(M[x,y]) * -1 - 1
            M[y,x] = abs(M[y,x]) * -1 - 1
    return M

def create_neye_matrix(student_information):
    l = len(student_information)
    if l > 1:
        M = np.eye(l)
        M *= -1
        return M
    else:
        print("Cannot calculate diversity with only one student")
        sys.exit(0)


def find_member_name(name, student_list):
    for i in student_list:
        if name == i[0]:
            first_name = i[1]
            last_name = i[2]
    # What if names can't be found?
    return " ".join([first_name, last_name])

def main():

    # This will be used when talking to the user. For now, use a default
    input_file = input("What is the name of the .txt file containing student "
                       "information?  ")
    student_info = openfile(getfilename(input_file))

    #student_info = openfile(getfilename('sample-input'))

    # This will be used when talking to the user. For now, use a default
    pp = 'N'
    if previous_partners() == 'Y':
        input_file1 = input(
            "What is the name of the .txt file containing previous partner "
            "information?  ")
        prev_partners_info = openfile(getfilename(input_file1))
        pp = 'Y'

    #prev_partners_info = openfile(getfilename('sample-pp'))

    cbM = create_criteria_matrix(student_info, "CountryOfBirth")
    ugM = create_criteria_matrix(student_info, "UnderGrad")
    ieM = create_criteria_matrix(student_info, "IndustryExp")
    inM = create_criteria_matrix(student_info, "Industry")

    frM = cbM + ugM + ieM + inM
    neM = create_neye_matrix(student_info)
    if pp == 'Y':
        ppM = create_pp_matrix(student_info, prev_partners_info, frM)
        fM = ppM + neM
    else:
        fM = frM + neM
    print(fM)

    """
    Matching Engine to go here

    """

    unit_coordinator = input("Please enter the email prefix of the unit "
                              "coordinator: ")

    teams = [['peter.adam', 'peter.adam']]

    for i in teams:
        tm1 = find_member_name(i[0], student_info)
        tm2 = find_member_name(i[1], student_info)

        team_subject = "Your team for ___ assignment"
        team_message = "Hi " + tm1 + " & " + tm2 + ",\n\n" \
                       "You have been grouped together for this assignment by " \
                       "#autodiverse, the robot that loves creating new, " \
                       "diverse project teams!\n\nThe unit coordinator has " \
                       "been informed that you will be working together for " \
                       "this task, so if you have any issues, please email " \
                       "them at "+ unit_coordinator + "@ucdconnect.ie\n\n" \
                       "#autodiverse wishes you a productive and diverse " \
                       "project experience!"

        recipients = []
        for recipient in i:
            recipients.append(recipient + "@ucdconnect.ie")
        #send_email(recipients, team_subject, team_message)
        print(team_message)

    uc_subject = "Teams for __ assignment"
    uc_message = "Hi uc_name, ..."

    #send_email(unit_coordinator, uc_subject, uc_message)

if __name__ == '__main__':
    main()
