import tkinter as tk
import re, os
import webbrowser
from tkinter import filedialog
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.action_chains import ActionChains

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

    match_set = set(reg_match)

    return list(match_set)

#Takes list and dictionary then compares set to dictionary keys,
#returns list of matched dictionary values (IP Addresses)
def compareUsers(logs_list, users_dict):

    matched_values = set()
    
    #Match MACs from logs_set to MACs from users_dict
    for i in range(0, len(logs_list)):
        #Splice last two digits from MAC in order to add and subtract
        #in order to test against Authenticated Users MACs
        if logs_list[i][-2:] == 'ff':
            overflow = hex(int(logs_list[i][-4:-3], 16) + 1)
            if (logs_list[i][:-4] + overflow + '00') in users_dict.keys():
                matched_values.add(users_dict[logs_list[i][:-4] + overflow + '00'])
                continue
        if logs_list[i][-2:] == '00':
            overflow = hex(int(logs_list[i][-4:-3], 16) - 1)
            if (logs_list[i][:-4] + overflow + 'ff') in users_dict.keys():
                matched_values.add(users_dict[logs_list[i][:-4] + overflow + 'ff'])
                continue
        base_MAC = logs_list[i][:-2]
        last_pair_plus = hex(int(logs_list[i][-2:], 16) + 1)
        last_pair_minus = hex(int(logs_list[i][-2:], 16) - 1)
        if base_MAC + last_pair_plus[2:] in users_dict.keys():
            matched_values.add(users_dict[base_MAC + last_pair_plus[2:]])
        if base_MAC + last_pair_minus[2:] in users_dict.keys():
            matched_values.add(users_dict[base_MAC + last_pair_minus[2:]])
        if logs_list[i] in users_dict.keys():
            matched_values.add(users_dict[logs_list[i]])
            
    return list(matched_values)

def changeModem(modem_IP):

"""    chrome_path = "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s"
    webbrowser.get(chrome_path).open('')
    counter = 0
    for IP in modem_IP:
        webbrowser.open_new_tab(IP)
        login = driver.find_element_by_name('AuthName')
        login.send_keys('admin')
        password = driver.find_element_by_name('Display')
        password.send_keys('ArViG1432Rg')
        password.send_keys(Keys.RETURN)
        counter++
        if (counter % 10) == 0:
            os.system("pause")"""

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

#Iterates through list and opens a webpage for each IP
#changeModem(matched_list)

#Prints IP Addresses to file until modem login automation implemented
os.chdir(os.path.dirname(auth_users))
testwrite = open('Test List.txt', 'w')

for y in range(0, len(matched_list)):
    testwrite.write(matched_list[y] + '\n')

testwrite.close()
