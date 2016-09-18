from nose.tools import *
from projpartners import projpartners
import numpy.testing

"""

def test_getfilename():
    assert_equal(getfilename())



def test_openfile(file):
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

"""

def test_create_pp_matrix():
    s = [['peter.adam', 'Peter', 'Adam', 'Australia', 'Engineering', 'Y',
           'OaG'],
          ['andy.mcsweeney', 'Andy', 'McSweeney', 'Ireland', 'Engineering',
           'Y', 'Consulting'],
          ['nicole.mcconville', 'Nicole', 'McConville', 'Ireland', 'Commerce',
           'Y', 'Accounting']]
    p1 = [['peter.adam', 'andy.mcsweeney']]
    p2 = [['peter.adam', 'nicole.mcconville'],['peter.adam', 'andy.mcsweeney']]
    p3 = [['peter.adam', 'andy.mcsweeney'],['peter.adam', 'andy.mcsweeney']]
    M1 = [[1, 2, 3],[1, 2, 3],[1, 2, 3]]
    M2 = [[1, 2, 3],[1, 2, 3],[1, 2, 3]]
    M3 = [[1, 2, 3],[1, 2, 3],[1, 2, 3]]
    res0 = projpartners.create_pp_matrix(s, p1, M1)
    res1 = projpartners.create_pp_matrix(s, p2, M2)
    res2 = projpartners.create_pp_matrix(s, p3, M3)

    #numpy.testing.assert_array_equal(res0, [[1, -3, 3],[-2, 2, 3],[1, 2, 3]])
    #numpy.testing.assert_array_equal(res1, [[1, 2, -4],[1, 2, 3],[-2, 2, 3]])
    #numpy.testing.assert_array_equal(res2, [[1, -4, 3],[-3, 2, 3],[1, 2, 3]])

    print(projpartners.create_pp_matrix(s, p1, M1))

test_create_pp_matrix()

def test_create_neye_matrix():
    res0 = projpartners.create_neye_matrix([])
    res1 = projpartners.create_neye_matrix([1])
    res2 = projpartners.create_neye_matrix([1, 2])
    assert_equal(res0, "Cannot calculate diversity with only one "
                              "student")
    assert_equal(res1, "Cannot calculate diversity with only one "
                              "student")
    numpy.testing.assert_array_equal(res2, [[-1, -0],[-0, -1]])
