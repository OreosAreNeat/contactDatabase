import json
import sys
import re

listPeople = []
seperator = "----------------------------------------------------------------------------------"
fname = ""
lname = ""
phone = ""
filePath = 'C:\\Users\\cjackson\\Documents\\Scripting\\DataAtYourCommand\\db.json'

def checkInput(input):
    parts = input.split()
    parts[0] = parts[0].lower()
    if(input == "help"):
        print("\n\"add [fname] [lname] [phone]\" (Adds a contact, include dashes in number)\n\"list\" (Lists all contacts)\n\"find\" (Searches for a contact based on first or last name)\n\"del\" (Deletes a contact based on first or last name)\n\"quit\" (quits the app)")
    elif(parts[0] == "add"):
        if(len(parts) == 4):
            add(input)
        else:
            print("Incorrect syntax, please use (add [fname] [lname] [phone])")
    elif(parts[0] == "list"):
        if(len(parts) == 1):
            list()
        else:
            print("Correct syntax is just (list)")
    elif(parts[0] == "find"):
        if(len(parts) == 2):
            find(parts[1])
        else:
            print("Correct syntax is (find [fname]) or (find[lname])")
    elif(parts[0] == "del"):
        if(len(parts) == 2):
            delete(parts[1])
        else:
            print("Correct syntax is (del [fname]) or (find[lname])")
    elif(parts[0] == "quit"):
        if(len(parts) == 1):
            sys.exit()
    else:
        print("Unknown argument, please try again")

def add(theInput):
    parts = theInput.split()
    fname = parts[1]
    lname = parts[2]
    phone = parts[3]
    validateInput(fname, lname, phone)

def list():
    if(listPeople.count != 0):
        for person in listPeople:
            print(seperator)
            print(person['fname'])
            print(person['lname'])
            print(person['phone'])
    else:
        print("No users in the database yet")
    

def find(name):
    name = name.lower()
    personPrint = False
    for person in listPeople:
        if (person['fname'].lower() == name or person['lname'].lower() == name):
            print(person['fname'])
            print(person['lname'])
            print(person['phone'])
            personPrint = True
            return person
    if(personPrint == False):
        print("Nobody in database matches input name")

def delete(name):
    personToDelete = find(name)
    if(personToDelete):
        print(f"Removing {personToDelete['fname']} {personToDelete['lname']} from the list...")
        listPeople.remove(personToDelete)
    saveFile = open(filePath, "w")  
    json.dump(listPeople, saveFile, indent = 6)  
    saveFile.close()



def validateInput(fname, lname, phone):
    create = False
    validOrNot = bool(re.search(r'[\d\W]', fname))
    if(validOrNot == True):
        print("First name cannot contain any digits or symbols")
        create = True
    validOrNot = bool(re.search(r'[\d\W]', lname))
    if(validOrNot == True):
        print("Last name cannot contain any digits or symbols")
        create = True
    validOrNot = bool(re.search(r'^\d{3}-\d{3}-\d{4}$', phone))
    if(len(phone) != 12):
        print("Improper phone number length, please include dashes")
        create = True
    elif(validOrNot == False):
        print("Phone number must follow syntax of xxx-xxx-xxxx")
        create = True
    if(create == False):
        createDictionary(fname, lname, phone)


def createDictionary(fname, lname, phone):
    dictPerson = {
        "fname": fname,
        "lname": lname,
        "phone": phone
    }
    listPeople.append(dictPerson)
    print(f"{dictPerson['fname']} {dictPerson['lname']} now added!")
    saveFile = open(filePath, "w")  
    json.dump(listPeople, saveFile, indent = 6)  
    saveFile.close()

def accessFile():
    try:
        with open(filePath, 'r') as file:
            return json.load(file)
    except: 
        print("db.json does not yet exist, creating it now")
        with open(filePath, 'w') as file:
            pass
        return []



exit = 1
while exit!=0:
    try:
        listPeople = accessFile()
        print(seperator + "\nGreetings, welcome to the contact database! Type \"help\" for a list of options.")
        userInput = input()
        checkInput(userInput)

    except Exception as e:
        print("Error:", e)
