##############
#  19010865  #
#SAYED  UDDIN#
##############
"""Test code
"""
import sankey_Additional 
import sys


TEST_FILES = ["test1.txt", "test2.txt", "test3.txt",
              "test4.txt", "test5.txt", "test6.txt"]

TEST_CASE_1 = ["data1, 14, 12, 124\n", "data2,\n",
               "data3, 123, 744, 456\n"]

TEST_CASE_2 = ["data1, 14, -12, 124\n", "data2, 123, 234, 345\n",
               "data3, 123, 744, 456\n"]

TEST_CASE_3 = ["data1, -14, 124\n", "data2, 123, 234, 345\n",
               "data3, 123, 744, 456\n"]

TEST_CASES = [TEST_CASE_1, TEST_CASE_2, TEST_CASE_3]
#Above are the test cases for testing process_data

TEST_CASE_4 = ["random title, 12, 12, 356\n", "data1, 14, 12, 124\n",
               "data2,\n", "data3, 123, 744, 456\n"]
TEST_CASE_5 = ["random title, -12, 12, 356\n", "data1, 14, -12, 124\n",
               "data2, 123, 234, 345\n", "data3, 123, 744, 456\n"]
TEST_CASE_6 = ["random title, 12, 12, --\n", "data1, -14, 124\n",
               "data2, 123, 234, 345\n", "data3, 123, 744, 456\n"]

TEST_CASES1 = [TEST_CASE_4, TEST_CASE_5, TEST_CASE_6]
#Above are the test cases for testing get_colours


def test_main(file_name):
    """
    Tests main function for additional challenge

    Parameters
    ----------
    file_name : str
        name of file the main function is being run on
    """
    if len(sys.argv) == 1:
        sys.argv.append(file_name)
    else:
        sys.argv[1] = file_name
    sankey_Additional.main()


def test_all_files():
    """
    Tests program on each standard file 
    """
    test_main("netball_2018.txt")
    test_main("Enmax_Bill.txt")
    test_main("California_Electricity.txt")
    test_main("BlueHatGreenHat.txt")


def unittest_process_data(data):
    """
    Tests process_data function

    Parameters
    ----------
    data : list
        list test case 
    """
    try:
        print(sankey_Additional.process_data(data))
        print("Process completed without error")
    except ValueError:
        print("A ValueError has occurred")


def unittest_get_colours(data):
    try:
        print("Colours:", sankey_Additional.get_colours(data))
        print("Process completed without error, ", end = "")
        print("default colours may be assigned")
        #All errors are accounted for by setting a default colour if a colour
        #is not found
    except ValueError:
        print("A ValueError has occurred")
        
    
def main():
    """
    Calls test functions and gives more readable output
    """
    for file in TEST_FILES:
        test_main(file)
        print()

    test_all_files()
    
    print("--process_data TEST CASES--")
    for i, test in enumerate(TEST_CASES):
        print(f"TEST {i + 1}: ")
        unittest_process_data(test)
        print()

    print("--get_colours TEST CASES--")
    for i, test in enumerate(TEST_CASES1):
        print(f"TEST {i + 1}: ")
        unittest_get_colours(test)
        print()
    

if __name__ == "__main__":
    main()
