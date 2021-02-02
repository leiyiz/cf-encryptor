from crypto import *
import os
import hashlib

# Data structure for an entry in the vault
class VaultEntry:
    def __init__(self, entryname="", key="", salt=""):
        self.name = entryname
        self.entry_key = key
        self.salt = salt
    def get_key(self):
        return self.key
    def get_name(self):
        return self.name
    def generate_key(self, password):
        # When generating key during init of a key, automatically hash
        if (self.salt == ""):
            self.salt = os.urandom(16)
        self.key = generate_password_key(password, self.salt)
    def encrypt_entry(self, key):
        entry = ("{},{},{}".format(self.name, self.entry_key, self.salt))
        return encrypt(key, entry)
    def decrypt_and_store_entry(self, key, entry_cipher):
        self.name, self.entry_key, self.salt = decrypt(key, entry_cipher).split(",")
    
# Primary Vault Class 
class Vault:
    def __init__(self, entry_keys):
        # Dictionary with hash of password: entries
        self.entries = {}
        self.entry_cipher_keys = entry_keys
        self.on_init(self.entry_cipher_keys)

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
        hash_fn = hashlib.sha256()
        hash_fn.update("{}".format(password).encode())
        pass_hash = hash_fn.digest()
        if pass_hash in self.entries:
            return self.entries[pass_hash]
        else:
            return AttributeError()
    
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
    Null.
    If password does not allow access to any vault entries, throws an AttributeError.
    '''
    def get_data(self, password, entry_name):
        hash_fn = hashlib.sha256()
        hash_fn.update("{}".format(password).encode())
        pass_hash = hash_fn.digest()
        if pass_hash in self.entries:
            for entry in self.entries[pass_hash]:
                if entry.get_name() == entry_name:
                    return entry
            return None
        else:
            return AttributeError()

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
        hash_fn = hashlib.sha256()
        hash_fn.update("{}".format(password).encode())
        pass_hash = hash_fn.digest()
        if pass_hash not in self.entries.keys():
            new_entry = VaultEntry(entry_name)
            new_entry.generate_key(password)
            self.entries[pass_hash] = []
            self.entries[pass_hash].append(new_entry)
        else:
            exists = False
            for entry in self.entries[pass_hash]:
                if entry.get_name() == entry_name:
                    exists = True
                    break
            if not exists:
                new_entry = VaultEntry(entry_name)
                new_entry.generate_key(password)
                self.entries[pass_hash].append(new_entry)
        return True
    
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
        hash_fn = hashlib.sha256()
        hash_fn.update("{}".format(password).encode())
        pass_hash = hash_fn.digest()
        index = 0
        if pass_hash in self.entries.keys():
            for entry in self.entries[pass_hash]:
                if entry.get_name() == entry_name:
                    break
                else:
                    index += 1
            if index < len(self.entries[pass_hash]):
                self.entries[pass_hash].pop(index)
                return True
        return False
        
    ''' Called when program exits.
        Performs the following functionalities:
            - Encrypt entries
            - Save new password hash to entry dictionary to local file
    '''
    def on_exit(self):
        all_entries = []
        i = 0
        for p in self.entries.keys():
            for entry in self.entries[p]:
                entry_cipher = entry.encrypt_entry(self.entry_cipher_keys[i])
                all_entries.append("{}:{}".format(p, entry_cipher))
                i += 1
        with open("cfe_vault.dat", "w+") as f:
            for entry in all_entries:
                f.write(entry + "\n")
        
    ''' Loaded when vault is initiatlized
        Performs the following functionalities:
            - Load password hash to entry dictionary from local file
            - Unhash all entries
            - Load internal data structures
    ''' 
    def on_init(self, keys):
        all_entries = []
        with open("cfe_vault.dat", "r+") as f:
            all_entries = f.readlines()
        for i in range(len(all_entries)):
            pass_hash, entry_cipher = all_entries[i].split(":")
            entry = VaultEntry()
            entry.decrypt_and_store_entry(keys[i], entry_cipher)
            if pass_hash not in self.entries.keys():
                self.entries[pass_hash] = []
            self.entries[pass_hash].append(entry)
        

if __name__ == "__main__":
    print("Toy Example")
    entry_keys = []
    entry_keys.append(generate_random_key())
    sample_vault = Vault(entry_keys)
    sample_vault.create_data("password123", "arkasfile.txt")
    sample_entry = sample_vault.get_data("password123", "arkasfile.txt")
    print(sample_entry.get_key())
    