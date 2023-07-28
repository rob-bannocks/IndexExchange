import utility
from urllib.parse import quote

def list_int_to_urlstring(int_list):
    """
    Function takes a list, uses list_int_to_string from utility to create a comma
    sepperated list and encodes this for use in a URL with the quote function
    usong quote from urllib

    Args:
        int_list (_type_): list of integers

    Returns:
        string: string in a format suitable for using in a rul
    """
    return quote(utility.list_ints_to_string(int_list))

def string_to_urlstring(string):
    return quote(string)

def int_to_urlstring(number):
    return quote(str(number))
if __name__ == "__main__":
    list_ints=[1,2,3,5,7,11,13]
    print("testing conversion of "+str(list_ints)+" to URL String "+list_int_to_urlstring(list_ints))
