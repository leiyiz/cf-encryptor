# Primary Vault Class 

'''
Metadata entries
(look at all entries) Given password to vault, returns list of files that are protected locally by that password
get_data_list_by_group(password)
(look at one entry) Given password to vault and the name of a file, returns remote file name and the key to that file
get_data(password, entry_name)  
(make an entry) Given a password, generate and return a random name and a secure random cryptographic key
create_data(password, entry_name)
(delete one entry) Given password to vault and the name of a file, delete the relevant entry
delete_data(password, entry_name)

'''
class Vault:
    def __init__(self):
    
    ''' 
    Gets a list of all data entries accessible by a 
    user passed password in the vault
    
    Inputs:
    password - a string that represents a user password

    Returns:
    a list of all data entries accessible by password
    If password does not allow access to any vault entries, throws an AttributeError.
    '''
    def get_data_list_by_group(self, password):
        return None

    ''' 
    Gets data for a particular entry with the name 
    entry_name and user passed password
    
    Inputs:
    password - a string that represents a user password
    entry_name - a string that represents the name of 
    entry being queried

    Returns: 
    data entry with entry_name name and accessible by password. 
    If data entry with entry_name name does not exist in vault, returns 
    an empty string.
    If password does not allow access to any vault entries, throws an AttributeError.
    '''
    def get_data(self, password, entry_name):
        return None

    '''
    Creates a new data entry with the name entry_name and 
    user passed password.

    Inputs:
    password - a string that represents a user password
    entry_name - a string that represents the name of the 
    entry being created

    Returns:
    True if vault successfully creates a new entry with that password lock
    True if entry with name entry_name already exists under password
    False if error occurs in creation
    '''
    def create_data(password, entry_name):
        return None
    '''
    Deletes a data entry in the vault with name entry_name and 
    user passed password. 

    Inputs:
    password - a string that represents a user password
    entry_name - a string that represents the name of the entry to be deleted

    Returns:
    True if an entry with entry_name under that password is succesfully deleted.
    False otherwise.
    '''
    def delete_data(password, entry_name):
        return None