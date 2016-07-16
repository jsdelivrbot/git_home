
# coding: utf-8

# In[1]:

#Problem: Voters in Florida
#Group members: S. Wang, Y. Ye, M. Staton, W. Wang


# In[2]:

#access regex functions
import re


# In[3]:

#make a handle on the html file
html_handle = open("FloridaVoters.html", "r")

#read in one line at a time
new_line = html_handle.readline()

#make an empty list to store all lines
records = []

#it turns out the desired tag is "<td>". This line will retrieve all the lines
#inside the "<td>" tag
while len(new_line) != 0:
    
    if new_line.startswith("<td>"):
        
        records.append(str(new_line.strip("<td></td>\r\n")))
    
    new_line = html_handle.readline()
    
#close the handle to end the process
html_handle.close()


# In[4]:

#create an empty list to store the data
clean_list = []

#every state takes 6 places in the list, so iterate over the list by 6 every time
for i in range(0, len(records), 6):
    
    county = records[i]
    
    rep_count = int(records[i+1].replace(",",""))
    dem_count = int(records[i+2].replace(",",""))
    
    clean_list.append({"county": county, "rep": rep_count, "dem": dem_count})

#define a helper function to sort the list by democratic votes
def get_dem(dict):
    return dict["dem"]


# In[5]:

#sort the list by democratic votes
sorted_list = sorted(clean_list, key=get_dem)

#print the sorted list line by line
for elem in sorted_list:
    print "{:<15}{:>8}{:>8}".format(elem["county"], elem["rep"], elem["dem"])

