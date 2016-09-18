from nose.tools import *
from projpartners import projpartners
import numpy.testing
import numpy as np
import os

def test_openfile():
    a = 'sample-pp-test.txt'
    b = 'sample-pp-test'
    c = '/sample-pp-test.txt'
    d = '../sample-pp-test.txt'

    res1 = projpartners.openfile(projpartners.getfilename(a)[3:])
    res2 = projpartners.openfile(projpartners.getfilename(b)[3:])
    res3 = projpartners.openfile(projpartners.getfilename(c)[3:])
    res4 = projpartners.openfile(projpartners.getfilename(d)[3:])

    assert_equal(res1, [['peter.adam', 'andy.mcsweeney']])
    assert_equal(res2, [['peter.adam', 'andy.mcsweeney']])
    assert_equal(res3, [['peter.adam', 'andy.mcsweeney']])
    assert_equal(res4, [['peter.adam', 'andy.mcsweeney']])

def test_getfilename():
    a = '../test.txt'
    b = '/Users/Padams/Documents/Programming/Python/projects/projpartners/test'
    c = 'test.ext'

    res0 = projpartners.getfilename(a)
    res1 = projpartners.getfilename(b)
    res2 = projpartners.getfilename(c)

    assert_equal(res0, os.path.join('..','test.txt'))
    assert_equal(res1, os.path.join('..','test.txt'))
    assert_equal(res2, os.path.join('..','test.txt'))

def test_create_criteria_matrix():
    s = [['peter.adam', 'Peter', 'Adam', 'Australia', 'Engineering', 'Y',
          'OaG'],
         ['andy.mcsweeney', 'Andy', 'McSweeney', 'Ireland', 'Engineering',
          'N', 'NA'],
         ['nicole.mcconville', 'Nicole', 'McConville', 'Ireland', 'Commerce',
          'N', 'NA']]
    res0 = projpartners.create_criteria_matrix(s, "CountryOfBirth")
    res1 = projpartners.create_criteria_matrix(s, "Industry")
    res2 = projpartners.create_criteria_matrix(s, "UnderGrad")

    numpy.testing.assert_array_equal(res0, [[0, 0, 0],[0, 0, 1],[0, 1, 0]])
    numpy.testing.assert_array_equal(res1, [[0, 0, 0],[0, 0, 0],[0, 0, 0]])
    numpy.testing.assert_array_equal(res2, [[0, 1, 0],[1, 0, 0],[0, 0, 0]])


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
    M = np.array([[1, 2, 3],[1, 2, 3],[1, 2, 3]])
    N = np.array([[1, 2, 3],[1, 2, 3],[1, 2, 3]])
    O = np.array([[1, 2, 3],[1, 2, 3],[1, 2, 3]])
    res0 = projpartners.create_pp_matrix(s, p1, M)
    res1 = projpartners.create_pp_matrix(s, p2, N)
    res2 = projpartners.create_pp_matrix(s, p3, O)

    numpy.testing.assert_array_equal(res0, [[1, -3, 3],[-2, 2, 3],[1, 2, 3]])
    numpy.testing.assert_array_equal(res1, [[1, -3, -4],[-2, 2, 3],[-2, 2, 3]])
    numpy.testing.assert_array_equal(res2, [[1, -4, 3],[-3, 2, 3],[1, 2, 3]])

def test_create_neye_matrix():
    res0 = projpartners.create_neye_matrix([])
    res1 = projpartners.create_neye_matrix([1])
    res2 = projpartners.create_neye_matrix([1, 2])
    assert_equal(res0, "Cannot calculate diversity with only one "
                              "student")
    assert_equal(res1, "Cannot calculate diversity with only one "
                              "student")
    numpy.testing.assert_array_equal(res2, [[-1, -0],[-0, -1]])
