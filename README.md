# Cloud File Encryptors (cfe)

Arka Bhattacharya  
Jenny Liang  
Leiyi Zhang  
Soham Pardeshi

# Getting Started

## Important Vocabulary
- *Encryption*: Encryption is a process where computers take data, such as text or files, and scrambles it into another format that is completely uninterpretable to humans. This keeps your information safe from cyberattackers. For example, if we have the text "Hello world", it can be transformed into "gSCsxf+rLqjrr66BiETc5g==". 

- *Decryption*: Decryption is a process where we take encrypted data and turn it back into its original format. This is how you can safely get your encrypted information back into a usable format. For example, if we had the text "gSCsxf+rLqjrr66BiETc5g==", we could decrypt it to "Hello world", based on the example above. 

## Tutorial
Below we outline a tutorial on how to use our application. This tutorial is primarily targeted towards Mac and Linux users, but most should apply to other operating systems.

Before we start, please ensure you are familiar with the following topics:
- [Opening a terminal](https://towardsdatascience.com/a-quick-guide-to-using-command-line-terminal-96815b97b955)
- Finding a path for a file:
  - [Tutorial for Windows users](https://www.sony.com/electronics/support/articles/00015251)
  - [Tutorial for MacOS usrs](https://macpaw.com/how-to/get-file-path-mac)

1. Ensure that you have Python 3.7 installed. If you don't, you can download Python and its package manager, `pip`, [here](https://www.python.org/downloads/).

2. Now, we can download the application. To do this, we should open our terminal and run the following command:
```
pip install cfe
```

3. Next, create a shortcut to make CFE easier to use.
```
export cfe=python cfe
```
We're ready to use CFE!

4. After this, you're ready to use our application. Before we begin uploading or downloading files, we need to set up our vault. This will contain special metadata that CFE will use to securely encrypt and decrypt files. We do this by running the following command:
```
cfe init
```

5. Now, we need to add your Google Account to CFE so that CFE can upload and download data to it later. We'll also need to give your account a nickname so that we can reference it later. To do this, we run:
```
cfe add provider your-provider-nickname
```
You will be prompted to log into Google Drive.

6. Now, let's get some data to encrypted on your Google Drive. Let's upload our first file! You'll need collect the following information:
- The file path of the file you'd like to upload
- The provider nickname (from step 4)
- A nickname for the file on your Drive (you can make this up!)
- A password to encrypt the file with

Now that you have this information, we can encrypt and upload the file to Google Drive. Let's run the following command:
```
cfe upload your-file-path your-provider-nickname/your-file-nickname
```
You will be prompted to enter your password for the file. You can create groups of files by encrypting them with the same password. You may be prompted to log into Google Drive.

7. Next, let's download the file back to our computer. You'll need the following information:
- The nickname for the file on your Drive (from step 5)
- The provider nickname (from step 4)
- The file path you'd like to download the file (remember to give your file a name and extension, if applicable)
- The password associated with the file (from step 5)

We can now download the file to the following location by typing the following:
```
cfe download your-provider-nickname/your-file-nickname your-file-path
```
You will be prompted to enter your password for the file before decrypting it. You may be prompted to log into Google Drive.


8. Now, let's verify what files we have in our vault with the password we just used (from step 5). We can do this by typing:
```
cfe list
```
You will be prompted to enter your password. You should see the file you just uploaded listed.

9. Finally, we can delete the file we just uploaded on our local computer as well as Google Drive. You'll need the following information:
- The file path of the file you'd like to delete (from step 6)
- The password associated with the file (from step 5)

Now, run the following command:
```
cfe delete your-file-path
```
You will be prompted to enter the password for the file. You may be prompted to log into Google Drive.

10. Congrats, you're done! Now, you know the basics of our tool!

## Download Cloud File Encryptors
This project requires Python >= 3.7.

### Download from PyPi
To download the project from PyPi, Python's package distribution service:
1. Ensure that you have `pip` installed.
2. Run `pip install cfe`.
3. To execute a command, please run `python cfe <command> <params>` from the root of the folder. Refer to section 4.1 for API usage details (see https://docs.google.com/document/d/1_uyduzbevI2s905mJY5_yCmw1VDD-GkK3kCpRj788sE/edit#heading=h.accln9wrzjbf)

### Download from Source
To run the application from source:
1. Ensure that you have Python 3 and a Python package manager (e.g. pip) installed.
2. From the root of the folder, run `pip install -r requirements.txt`. Or, install all of the requirements detailed in requirements.txt.
3. To execute a command, please run `python cfe <command> <params>` from the root of the folder. Refer to section 4.1 for API usage details (see https://docs.google.com/document/d/1_uyduzbevI2s905mJY5_yCmw1VDD-GkK3kCpRj788sE/edit#heading=h.accln9wrzjbf)