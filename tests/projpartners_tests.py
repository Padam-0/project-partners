from nose.tools import *
from projpartners import *

def test_getfilename():
    assert_equal(getfilename())



def test_openfile(file):
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


def test_previous_partners():
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


def test_getfilename(filename):
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


def test_send_email(recipients, subject, message):
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


def test_create_criteria_matrix(s, criteria):
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

def test_create_pp_matrix(s, p, M):
    l = len(s)
    q = len(p)
    # create match data
    for i in range(q):
        for j in range(l):
            if p[i][0] == s[j][0]:
                x = j
            if p[i][1] == s[j][0]:
                y = j
    M[x,y] = M[x,y] * -1 - 1
    M[y,x] = M[y,x] * -1 - 1
    return M

def test_create_neye_matrix(student_information):

    l = len(student_information)
    M = np.eye(l)
    M *= -1
    return M