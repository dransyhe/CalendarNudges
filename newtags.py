import pandas as pd
from checks import *



# read the input data file in CSV
col_names = ['username', 'jobrole', 'instructor', 'companyname', 'timezone', 'companysize', \
			 'teamsize', 'starttime', 'lastsync', 'meetingtitle', 'noguest', 'tag'] 
calendar_data = pd.read_csv("New Tagged.csv", header=0, names=col_names)

#creates lists of username, companyname, title, noguests, timezone and startime
calendar_data.username = calendar_data.username.astype(str)
usernames_list = calendar_data.username.values.tolist()

calendar_data.companyname = calendar_data.companyname.astype(str)
companyname_list =  calendar_data.companyname.values.tolist()

calendar_data.meetingtitle = calendar_data.meetingtitle.astype(str)
titles_list = calendar_data.meetingtitle.values.tolist()

calendar_data.noguest = calendar_data.noguest.astype(int)
noguest_list = calendar_data.noguest.values.tolist()

calendar_data.timezone = calendar_data.timezone.astype(str)
timezone_list = calendar_data.timezone.values.tolist()

calendar_data.starttime = calendar_data.starttime.astype(str)
starttime_list = calendar_data.starttime.values.tolist()

calendar_data.tag = calendar_data.tag.astype(str)
tag_list = calendar_data.tag.values.tolist()

#creates a list of dictonaries each representing a meeting and converts the starttime into a datetime object
meeting_list = []
for i in range(len(usernames_list)):
    meeting = {}
    meeting['username'] = usernames_list[i]
    meeting['companyname'] = companyname_list[i]
    meeting['title'] = titles_list[i]
    meeting['noguest'] = noguest_list[i]
    meeting['timezone'] = timezone_list[i]
    meeting['starttime'] = starttime_list[i]
    meeting['tag'] = tag_list[i]
    meeting = dates_and_times_corrector(meeting)
    meeting_list += [meeting]

company_dict = create_company_dict(meeting_list)




