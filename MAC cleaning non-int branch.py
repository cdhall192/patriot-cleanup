import tkinter as tk
import re, os
from tkinter import filedialog

#Takes csv of Authenticated Users, returns dictionary with MACs as keys and IPs as values
def getUsers(users):

    #Import auth_users csv and search for relevant data
    users_file = open(users)
    users_content = users_file.read()
    users_file.close()

    #Regex search for MAC and IP Addresses
    reg_match = MAC_IP_regex.findall(users_content)

    #Assign the MAC as a key to the dictionary with the following IP as it's value
    match_dict = {}
    for i in range(0, len(reg_match)):

        try:
            if MAC_only_regex.match(reg_match[i]) is not None \
               and IP_only_regex.match(reg_match[i+1]) is not None:
        
                match_dict[reg_match[i]] = reg_match[i+1]
        except IndexError:
            continue
        
    return match_dict

#Takes csv of DHCP logs, returns list of MACs
def DHCPLogs(logs):

    #Import logs_csv into list
    logs_file = open(logs)
    logs_content = logs_file.read()
    logs_file.close()

    #Regex search for MAC Addresses
    reg_match = MAC_only_regex.findall(logs_content)

    match_list = []

    for i in range(0, len(reg_match)):
        if reg_match[i] not in match_list:
            match_list.append(reg_match[i])

    return match_list

#Takes list and dictionary then compares list to dictionary keys,
#returns list of matched dictionary values (IP Addresses)
def compareUsers(logs_list, users_dict):

    #Match MACs from logs_list to MACs from users_dict
    matched_values = []

    for i in range(0, len(logs_list)):
        #Splice last two digits from MAC in order to add and subtract
        #in order to test against Authenticated Users MACs
        base_MAC = logs_list[i][:-2]
        last_pair_plus = hex(int(logs_list[i][-2:], 16) + 1)
        last_pair_minus = hex(int(logs_list[i][-2:], 16) - 1)
        if base_MAC + last_pair_plus[2:] in users_dict.keys():
            if users_dict[base_MAC + last_pair_plus[2:]] not in matched_values:
                matched_values.append(users_dict[base_MAC + last_pair_plus[2:]])
        elif base_MAC + last_pair_minus[2:] in users_dict.keys():
            if users_dict[base_MAC + last_pair_minus[2:]] not in matched_values:
                matched_values.append(users_dict[base_MAC + last_pair_minus[2:]])

    return matched_values

#TODO: Write code to automate modem logon and changes
#def changeModem(modem_IP):

    #TODO: Using IP from matchedList, go to modem and login
    #TODO: Check if correct interface has the IP
    #TODO: Go to network settings and disable unnecessary interfaces
    #TODO: Logout
    #TODO: Write errors in log

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

#Runs files through functions to get relevant data
cleaned_users = getUsers(auth_users)
cleaned_logs = DHCPLogs(logs_csv)

#Compares data to find IP Addresses of modems spamming the DHCP server
matched_list = compareUsers(cleaned_logs, cleaned_users)

#Prints IP Addresses to file until modem login automation implemented
os.chdir(os.path.dirname(auth_users))
testwrite = open('Test List.txt', 'w')

for y in range(0, len(matched_list)):
    testwrite.write(matched_list[y] + '\n')

testwrite.close()

#Iterates through list and runs changeModem on each IP
#for IP in range(0, len(matched_list)):
#    changeModem(matched_list[IP])
