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

    :param file:
    :return:
    """
    li = []
    f = open(file, 'r')
    for line in f:
        li.append(line)
    f.close()
    return li

def main():

    """
    open file ()
    import student info ()
    close file ()
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

if __name__ == '__main__':
    main()
