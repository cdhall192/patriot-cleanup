import tkinter as tk
import re, os
from tkinter import filedialog

#Select the files to compare
root = tk.Tk()
root.withdraw()
print("Please select the file with the DHCP logs.")
logs_csv = filedialog.askopenfilename()
print("Please select the file with the Authenticated Users.")
auth_users = filedialog.askopenfilename()

#Regex to find MAC and IP Addresses
MAC_IP_regex = re.compile(r'\d{1,3}[.]\d{1,3}[.]\d{1,3}[.]\d{1,3}|[0-9A-Fa-f]{2}[:-][0-9A-Fa-f]{2}[:-][0-9A-Fa-f]{2}[:-][0-9A-Fa-f]{2}[:-][0-9A-Fa-f]{2}[:-][0-9A-Fa-f]{2}')
IP_only_regex = re.compile(r'\d{1,3}[.]\d{1,3}[.]\d{1,3}[.]\d{1,3}')
MAC_only_regex = re.compile(r'[0-9A-Fa-f]{2}[:-][0-9A-Fa-f]{2}[:-][0-9A-Fa-f]{2}[:-][0-9A-Fa-f]{2}[:-][0-9A-Fa-f]{2}[:-][0-9A-Fa-f]{2}')

def getUsers(users):

    #Import auth_users csv and search for relevant data
    users_file = open(users)
    users_content = users_file.read()
    users_file.close()

    #Regex search for MAC and IP Addresses
    reg_match = MAC_IP_regex.findall(users_content)
    #reg_match_MAC = MAC_only_regex.findall(users_content)
    
    #Strip colons to prepare for conversion to integer
    for x in range(0, len(reg_match)):
        reg_match[x] = re.sub(r'[:]', '', reg_match[x])

    #Convert string to integer and store MAC/IP Pairs in dictionary
    match_dict = {}
    for i in range(0, len(reg_match), 2):
        #Convert only the MAC Addresses to Int
        try:
            reg_match[i] = int(reg_match[i], 16)
        except:
            continue
        #Assign the MAC as a key to the dictionary with the following IP as it's value
        match_dict[reg_match[i]] = reg_match[i+1]
        
    return match_dict

def DHCPLogs(logs):

    #Import logs_csv into list
    logs_file = open(logs)
    logs_content = logs_file.read()
    logs_file.close()

    #Regex search for MAC Addresses
    reg_match = MAC_only_regex.findall(logs_content)
    
    #Strip colons to prepare for conversion to hexadecimal
    for x in range(0, len(reg_match)):
        reg_match[x] = re.sub(r'[:]', '', reg_match[x])
    
    #Convert MACs to int, store MACs in list, and remove duplicates
    match_list = []
    for i in range(0, len(reg_match)):
        reg_match[i] = int(reg_match[i], 16)
        if reg_match[i] not in match_list:
            match_list.append(reg_match[i])
            
    return match_list

def compareUsers(compare_list, compare_dict):

    #Match MACs from logs_list to MACs from users_dict
    matched_values = []
    test_list = []
    for i in compare_dict.keys():
        test_list.append(i)

    for i in range(0, len(test_list)):
        if int(test_list[i]) + 1 in compare_list:
            matched_values.append(compare_dict[test_list[i]])
        elif int(test_list[i]) - 1 in compare_list:
            matched_values.append(compare_dict[test_list[i]])
            
    return matched_values

#def changeModem(modem_IP):

    #TODO: Using IP from matchedList, go to modem and login
    #TODO: Check if correct interface has the IP
    #TODO: Go to network settings and disable unnecessary interfaces
    #TODO: Logout
    #TODO: Write errors in log

#Takes csv of Authenticated Users, returns dictionary with MACs as keys and IPs as values
users_dict = getUsers(auth_users)

#Takes csv of DHCP logs, returns list of MACs
logs_list = DHCPLogs(logs_csv)

#Takes list and dictionary then compares, returns list of matched dictionary values (IP Addresses)
matched_list = compareUsers(logs_list, users_dict)

os.chdir(os.path.dirname(auth_users))
testwrite = open('Test List.txt', 'w')

for y in range(0, len(matched_list)):
    testwrite.write(matched_list[y] + '\n')
    
testwrite.close()

#Iterates through list and runs changeModem on each IP
#for IP in range(0, len(matched_list)):
#    changeModem(matched_list[IP])
    
