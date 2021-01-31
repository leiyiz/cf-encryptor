from crypto import *
import os
import hashlib

# Data structure for an entry in the vault
class VaultEntry:
    def __init__(self, entryname="", key="", salt=""):
        self.name = entryname
        self.key = key
        self.salt = salt
    def get_key(self):
        return self.key
    def get_name(self):
        return self.name
    def generate_key(self, password):
        # When generating key during init of a key, automatically hash
        self.salt = os.urandom(16)
        self.key = generate_password_key(password, self.salt)
    def hash_entry(self):
        entry_hash = hashlib.sha256()
        entry_hash.update("{},{},{}".format(self.name, self.key, self.salt))
        return entry_hash.digest()
    
# Primary Vault Class 
class Vault:
    def __init__(self):
        # Dictionary with hash of password: entries
        self.entries = {}
        self.on_init()

    def __del__(self):
        self.save_data()
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
    def create_data(self, password, entry_name):
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
    def delete_data(self, password, entry_name):
        return None
    
    ''' Called when program exits.
        Performs the following functionalities:
            - Hash all entries
            - Save new password hash to entry dictionary to local file
    '''
    def save_data(self):

    ''' Loaded when vault is initiatlized
        Performs the following functionalities:
            - Load password hash to entry dictionary from local file
            - Unhash all entries
            - Load internal data structures
    ''' 
    def on_init(self):

    
