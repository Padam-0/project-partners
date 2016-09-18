# Import required libraries and returns error message if required.
try:
    import sys
    import smtplib
    import getpass
    import numpy as np
    import os
    import re
except ImportError as import_err:
    print(import_err)
    print("Unable to import required libraries. Please check installation of "
          "sys, smtplib, getpass, numpy, os & re libraries for python 3.5")
    exit(0)

# Define criteria that diversity is measured against
criteria_list = ["CountryOfBirth", "UnderGrad", "IndustryExp", "Industry"]

def openfile(filename):
    # Open a file and extract data
    li = [] # Create empty list called li
    try:
        f = open(filename, 'r') # Try and open file from filename provided
        for line in f:
            li.append((line.rstrip()).split(' ')) # For each line, remove
            # whitepsace and split into single list elements based on ' '
            # character. Append this list to the list li
        f.close() # Close file
        return li
    except:
        o = input("I can't find a file with that name. If you want to quit, "
              "please press Q, if not, please try again:  ").upper()
        if o == 'Q':
            exit(0) # If filename is wrong, allow user option to quit (Q)
        else:
            openfile(getfilename(o.lower())) # If filename is wrong,
            # allow user option to keep trying


def previous_partners():
    # Ask the user if previous partner information is needed
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
            sys.exit() # Give the user an option to quit if input is wrong
    return previous_partners


def getfilename(filename):
    # Takes a filename and reformats it to be in correct input style
    if os.path.join('a','b') == 'a/b': # Checks if OS is Mac/Unix, which uses
        #  the '/' character in directory paths
        #os is unix
        c = filename.count('/') # Counts number of '/' characters in the string
        if c != 0:
            # If '/' characters are present, replaces all but the last of
            # these. Then finds the index of the last '/'
            i = filename.replace('/', '|', c - 1).find('/')
            # Strips all information prior to and including the last '/',
            # leaving only the filename without a path.
            nf = filename[i + 1:]
        else:
            # If no '/' characters are found, filename is left unchanged
            nf = filename
    else:
        #os is windows
        c = filename.count('\\') # Counts number of '\' characters
        if c != 0:
            # If '\' characters are present, replaces all but the last of
            # these. Then finds the index of the last '\'
            i = filename.replace('\\', '|', c - 1).find('\\')
            # Strips all information prior to and including the last '\',
            # leaving only the filename without a path
            nf = filename[i + 1:]
        else:
            # If no '\' characters are found, filename is left unchanged
            nf = filename

    pattern = re.compile(r'\..+$') # Compile a Regular Expression (Regex)
    # pattern to identify the '.' character, followed by one or more other
    # characters at the end of a string
    if re.search(pattern, nf) != None:
        # If the pattern returns a result, find the length of the match
        a = len(re.findall(pattern, nf)[0])
        nf = nf[:-a] # Remove the file extension from the end of the filename
    nf += '.txt' # Replace the file extension with '.txt'
    return os.path.join('..',nf) # Return the extension in the form
    # '../filename.txt'. On windows, will be '..\filename.txt'


def send_email(recipients, subject, message):
    server = smtplib.SMTP('smtp.gmail.com', '587') # Connect to gmail
    server.starttls()  # Starts TLS Encryption
    email_acc = 'peter.adam@ucdconnect.ie' # Set username
    password = getpass.getpass("Enter the password for %s" % (email_acc)) #
    # Enter password
    server.login(email_acc, password) # Login to Server
    content = "Subject: " + subject + "\n" + message # Create message
    server.sendmail(email_acc, recipients, content) # Send email
    server.quit() # Quit from server


def create_criteria_matrix(s, criteria):
    # Creates a matrix with dimensions based on the number of students. Each
    # entry in the matrix represents either a match based on criteria (1) or
    # no match based on a criteria (0)
    ci = criteria_list.index(criteria) + 3 # Find criteria index inside
    # student information
    l = len(s) # Required matrix dimensions
    M = np.zeros((l,l)) # Create a zero matrix of required dimensions
    # create match data
    for i in range(l):
        # For row in the matrix
        for j in range(l):
            # For each column in the matrix
            if s[i][0] == s[j][0]:
                # If the email prefixes match, it means it's the same
                # student, so don't make any adjustment
                M[i][j] += 0
            elif s[i][ci] == s[j][ci]:
                # If there is a match in the criteria
                if ci == 6 and s[i][ci] == 'NA':
                    # Necessary to not double count lack of industry experience
                    M[i][j] += 0
                else:
                    M[i][j] += 1
            else:
                # If no match, do nothing
                pass
    return M

def create_pp_matrix(s, p, M):
    # Adjust a matrix based on a list of prior partners
    l = len(s)
    q = len(p)
    # create match data
    x = 0
    y = 0
    for i in range(q):
        # For each row in the matrix
        for j in range(l):
            # For each column in the matrix
            if p[i][0] == s[j][0]:
                # If partner email prefixes match, remember the row number
                x = j
            if p[i][1] == s[j][0]:
                # If partner email prefixes match, remember the column number
                y = j
        if x > 0 or y > 0:
            # Negate both entries for partners in the matrix
            M[x,y] = abs(M[x,y]) * -1 - 1
            M[y,x] = abs(M[y,x]) * -1 - 1
    return M

def create_neye_matrix(student_information):
    # Create negative identity matrix with dimensions based on the number of
    # students
    l = len(student_information) # Calculate the number of students
    if l > 1:
        M = np.eye(l) # If more than one, create an l x l identity matrix
        M *= -1 # Negate the matrix
        return M
    else:
        # If one or less students, comparison is impossible, so program quits
        print("Cannot calculate diversity with only one student")
        sys.exit(0)


def find_member_name(email_prefix, student_list):
    # Based on an email prefix, find the first and last names of a student in
    # the student list
    for i in student_list:
        # Loop through student entries
        if email_prefix == i[0]: # Check if the email prefix of a given
            # student is equal to the email prefix we are looking for
            first_name = i[1] # If so, return first and last name
            last_name = i[2]
    # What if names can't be found?
    return " ".join([first_name, last_name])


def matching_engine(M):
    li = []
    diT = {}
    di0 = {}
    for i in range(len(M)):
        row = M[i]
        sum_row = (row >= 0).sum()
        count_zeros = np.count_nonzero(row == 0)
        diT[i] = sum_row
        di0[i] = count_zeros
    return diT, di0
    # return li


def main():
    """
    # This will be used when talking to the user. For now, use a default
    input_file = input("What is the name of the .txt file containing student "
                       "information?  ")
    student_info = openfile(getfilename(input_file))
    """

    student_info = openfile(getfilename('sample-input'))

    """
    # This will be used when talking to the user. For now, use a default
    pp = 'N'
    if previous_partners() == 'Y':
        input_file1 = input(
            "What is the name of the .txt file containing previous partner "
            "information?  ")
        prev_partners_info = openfile(getfilename(input_file1))
        pp = 'Y'
    """
    prev_partners_info = openfile(getfilename('sample-pp'))

    # Create diversity matrices for each of our 4 criteria
    cbM = create_criteria_matrix(student_info, "CountryOfBirth")
    ugM = create_criteria_matrix(student_info, "UnderGrad")
    ieM = create_criteria_matrix(student_info, "IndustryExp")
    inM = create_criteria_matrix(student_info, "Industry")

    # Sum diversity matrices
    frM = cbM + ugM + ieM + inM
    # Create negative identity matrix
    neM = create_neye_matrix(student_info)

    """
    if pp == 'Y':
        # Adjust cumulative diversity matrix based on previous partners
        ppM = create_pp_matrix(student_info, prev_partners_info, frM)
        # Add negative identity matrix to remove self-matching
        fM = ppM + neM
    else:
        # Add negative identity matrix to remove self-matching
        fM = frM + neM
    """

    ppM = create_pp_matrix(student_info, prev_partners_info, frM)
    fM = ppM + neM

    print(matching_engine(fM))

    """
    unit_coordinator = input("Please enter the email prefix of the unit "
                              "coordinator: ")

    # Return list of teams here
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
    """


if __name__ == '__main__':
    main()
