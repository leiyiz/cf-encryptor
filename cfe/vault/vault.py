from crypto import *
import os
import hashlib

# Data structure for an entry in the vault
class VaultEntry:
    def __init__(self, entryname="", key=""):
        self.name = entryname
        self.entry_key = key
        self.salt = os.urandom(16)
    def get_key(self):
        return self.entry_key
    def get_name(self):
        return self.name
    def generate_key(self):
        self.entry_key = generate_random_key()
    
    def encrypt_entry(self, password):
        entry = ("{},{},{}".format("cfe_check", self.name, self.entry_key))
        key = generate_password_key(password, self.salt)
        ciphertext = encrypt(key,entry)
        return self.salt + ciphertext
    
    ''' Returns true if successfully decrypted and stored, and false otherwise '''
    def decrypt_and_store_entry(self, password, entry_ciphertext):
        #print(entry_ciphertext)
        salt, ciphertext = entry_ciphertext[:16], entry_ciphertext[16:]
        key = generate_password_key(password, salt)
        entry_data = decrypt(key, ciphertext).decode()
        if "cfe_check" in entry_data:
            # Decrypted succesfully, store
            _ ,self.name, self.entry_key = entry_data.split(",")
            self.entry_key = bytes(self.entry_key[2:-2], encoding="ascii")
            self.salt = salt
            return True
        else:
            return False

    
# Primary Vault Class 
class Vault:
    def __init__(self, password):
        # Dictionary with hash of password: entries
        self.entries = []
        self.password =  password
        self.on_init()

    ''' 
    Gets a list of all data entries accessible by a 
    user passed password in the vault
    
    Inputs:
    password - a string that represents a user password

    Returns:
    a list of all data entries accessible by password
<<<<<<< HEAD
    If password does not allow access to any vault entries, returns None.
    '''
    def get_data_list_by_group(self, password):
        if (password == self.password):
            return self.entries
        else:
            return []
=======
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
>>>>>>> 49a64ff7914fad6b304123329126d3b9187c4dce
    
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
<<<<<<< HEAD
    None.
    If password does not allow access to any vault entries, None.
    '''
    def get_data(self, password, entry_name):
        if (password == self.password):
            for entry in self.entries:
                if entry.get_name() == entry_name:
                    return entry    
        return None
=======
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
>>>>>>> 49a64ff7914fad6b304123329126d3b9187c4dce

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
<<<<<<< HEAD
    False if error occurs in creation or cannot authenticate query
    '''
    def create_data(self, password, entry_name):
        if (password == self.password):
            for entry in self.entries:
                if entry.get_name() == entry_name:
                    return True
            new_entry = VaultEntry(entry_name)
            new_entry.generate_key()
            self.entries.append(new_entry)
            self.on_save()
            return True
        return False

=======
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
>>>>>>> 49a64ff7914fad6b304123329126d3b9187c4dce
    
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
<<<<<<< HEAD
        if (password == self.password):
            i = 0
            for entry in self.entries:
                if entry.get_name() == entry_name:
                    break
                else:
                    i += 1
            if i < len(self.entries):
                self.entries.pop(i)
                return True

        return False

=======
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
>>>>>>> 49a64ff7914fad6b304123329126d3b9187c4dce
        
    ''' Called when program exits.
        Performs the following functionalities:
            - Encrypt entries
            - Save new password hash to entry dictionary to local file
    '''
<<<<<<< HEAD
    def on_save(self):
        with open("cfe_vault.dat", "wb+") as f:
            for entry in self.entries:
                entry_ct = entry.encrypt_entry(self.password)
                f.write(entry_ct)
            
=======
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
>>>>>>> 49a64ff7914fad6b304123329126d3b9187c4dce
        
    ''' Loaded when vault is initiatlized
        Performs the following functionalities:
            - Load password hash to entry dictionary from local file
            - Unhash all entries
            - Load internal data structures
    ''' 
<<<<<<< HEAD
    def on_init(self):
        all_entries = []
        with open("cfe_vault.dat", "rb") as f:
            all_entries = f.readlines()
        if len(all_entries) != 0:    
            for entry_ct in all_entries:
                potential_entry = VaultEntry()
                if potential_entry.decrypt_and_store_entry(self.password, entry_ct):
                    self.entries.append(potential_entry)
        

=======
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
>>>>>>> 49a64ff7914fad6b304123329126d3b9187c4dce
        

if __name__ == "__main__":
    print("Toy Example")
    entry_keys = []
    entry_keys.append(generate_random_key())
<<<<<<< HEAD
    sample_vault = Vault("password123")
=======
    sample_vault = Vault(entry_keys)
>>>>>>> 49a64ff7914fad6b304123329126d3b9187c4dce
    sample_vault.create_data("password123", "arkasfile.txt")
    sample_entry = sample_vault.get_data("password123", "arkasfile.txt")
    print(sample_entry.get_key())
    