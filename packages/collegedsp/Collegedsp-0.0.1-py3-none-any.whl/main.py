# importing all packages
import numpy as np

def matrix_add(matrix1, matrix2):
    """
    This function takes two matrix and finds the sum of the two matrix.
    It displays the added matrix as a result
    """

    # Matrix1: First matrix
    # Matrix2: Second Matrix
    result = [map(sum, zip(*z)) for z in zip(matrix1, matrix2)]  # To add two matrix

    # To print the added matrix in actual matrix form
    for i in result:
        print(list(i))

def matrix_sub(matrix1, matrix2):
    """
    This function takes two matrix and finds the subtraction of the two matrix.
    It displays the subtracted matrix as a result.
    """

    # Matrix1: First matrix
    # Matrix2: Second Matrix
    matrix1 = np.array(matrix1)
    matrix2 = np.array(matrix2)
    result = np.subtract(matrix1, matrix2)  # To subtract two matrix

    # To print the subtracted matrix in actual matrix form
    for i in result:
        print(list(i))


def matrix_multiply(matrix1, matrix2):
    """
    This function takes two matrix and finds the multiplication of the two matrix.
    It displays the multiplication matrix as a result
    """

    # Matrix1: First matrix
    # Matrix2: Second Matrix
    matrix1 = np.array(matrix1)
    matrix2 = np.array(matrix2)
    result = np.dot(matrix1, matrix2)  # To multiply two matrix

    # To print the multiplicated matrix in actual matrix form
    for i in result:
        print(list(i))

def matrix_elemultiply(matrix1, matrix2):
    """
    This function takes two matrix and finds the element-wise multiplication of the two matrix.
    It displays the element-wise multiplication matrix as a result
    """

    # Matrix1: First matrix
    # Matrix2: Second Matrix
    matrix1 = np.array(matrix1)
    matrix2 = np.array(matrix2)
    result = np.multiply(matrix1, matrix2)  # To multiply element wise the two matrix

    # To print the element-wise multiplicated matrix in actual matrix form
    for i in result:
        print(list(i))
def matrix_inverse(matrix):
    """
    This function takes one matrix and finds the inverse of the matrix.
    It displays the inversed matrix as a result
    """

    matrix = np.array(matrix)
    result = np.linalg.inv(matrix)  # To inverse the matrix

    # To print the inversed matrix in actual matrix form
    for i in result:
        print(list(i))

def matrix_transpose(matrix):
    """
    This function takes one matrix and finds the transpose of the matrix.
    It displays the transposed matrix as a result
    """

    matrix = np.array(matrix)
    result = np.transpose(matrix)  # To transpose the matrix

    # To print the transposed matrix in actual matrix form
    for i in result:
        print(list(i))