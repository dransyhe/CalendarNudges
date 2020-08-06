import Excel_Reader_Updated
from Excel_Reader_Updated import extract_from_excel
import datetime
import nltk
from nltk import word_tokenize

meeting_list = extract_from_excel("Multiplii Data 15072020.xlsx",["User Name","Job Role", "Report into", "Company", "Timezone", "Company Size", "Team Size","Start Time","Last Sync","Meeting Title","Number of Guests","Nudge Requested Date","Goals","Framework", "Nudge ID", "Relevant"])

zero_guests_words = ["prep"] #todo list probably add
irrelevant_words = ["block", "busy", "hold", "offline", "office hours", "lunch", "dinner", "edited", "cancel", "leave work"]





#checks whether the selected meeting title contains a particular word and has zero participants
def word_zero_guests(word, meeting):
    return ( word_in_title(word, meeting) and meeting["Number of Guests"] == '0')

#checks whether the selected meeting title contains a particular word
def word_in_title(word, meeting):
    return word.lower() in str(meeting["Meeting Title"]).lower()


def dic_check(meeting_list):
    for word in irrelevant_words:
        inc_meetings = [meeting for meeting in meeting_list if word_in_title(word, meeting)]
        count = len(inc_meetings)
        correct = len([1 for meeting in inc_meetings if meeting["Relevant"] == "n"])
        print(word + " " + str(count) + " " + str(correct))

#checks whether the user's company is in the title
def user_company_in_title(meeting):
    alternate_list = company_dict[meeting["Company"]]
    for alternate in alternate_list:
        if str(alternate).lower() in str(meeting["Meeting Title"]).lower():
            return True
    return False


#creates a dictonary of user companies which include the other spellings for the company name
def create_company_dict(meeting_list):
    company_dic = {}
    for company_name in list(set([meeting["Company"] for meeting in meeting_list])):
        company_dic[company_name] = [company_name]
    company_dic["People Collective"] = company_dic["People Collective"] +["PC"]
    company_dic["Grant Tree"] = company_dic["Grant Tree"] + ["GrantTree"]
    company_dic["BECO Capital"] = company_dic["BECO Capital"] + ["BECO"]
    company_dic["Shaper Impact Capital"] =  company_dic["Shaper Impact Capital"] + ["SIC"]
    return company_dic
        


#checks if the user's full name is in the title
def users_fullname(meeting):
    return str(meeting["User Name"]).lower() in str(meeting["Meeting Title"]).lower()

#checks if the meeting took place on a workday
def not_workday(meeting):
    return meeting["Start Time"].isocalendar()[2] >= 6

#checks if the meeting took place during workhours e.g (6am - 9pm) 
def not_worktime(meeting):
    return meeting["Start Time"].time() < datetime.time(6) or meeting["Start Time"].time() > datetime.time(21)


#checks if the meeting is a one word title with zero guests
def one_word_title_zero_guests(meeting):
    return meeting["Number of Guests"] == '0' and meeting_title_length(meeting) == 1


#returns number of words in meeting title
def meeting_title_length(meeting):
    return len(word_tokenize(str(meeting["Meeting Title"])))

#0 guests except for the user Christopher Dillon who's meetings have no guests
def zero_guests(meeting):
    return meeting["Number of Guests"] == "0" and meeting["User Name"] != "Christopher Dillon"




#checks if the meeting is a webinar (title more than 12 words, title mre than 9 words and 0 guests or >50 guests, includes the word webinar???
def check_webinar(meeting):
    if meeting_title_length(meeting) > 12:
        return True
    if meeting_title_length(meeting) > 10 and (meeting["Number of Guests"] == '0' or int(meeting["Number of Guests"]) >= 50):
        return True
    if word_in_title("webinar", meeting):
        return True
    return False



def basic_check_irrelevant(meeting):
    #for word in zero_guests_words:
    #   if word_zero_guests(word, meeting):
    #      return True
    for word in irrelevant_words:
       if word_in_title(word, meeting):
          return True
    if user_company_in_title(meeting):
        return True
    if zero_guests(meeting):
        return True
    if not_worktime(meeting):
        return True
    #if not_workday(meeting):
    #    return True
    if check_webinar(meeting):
        return True
    if users_fullname(meeting):
        return True
    return False

def irrelevant_words_check(meeting):
    for word in irrelevant_words:
        if word_in_title(word, meeting):
            return True
    return False

def first_name_only(meeting):
    user_names = word_tokenize(meeting["User Name"])
    return word_in_title(user_names[0], meeting) and not word_in_title(user_names[1], meeting)


def feature_creater(meeting):
    feature_dic = {}
    feature_dic["irrelevant words"] = irrelevant_words_check(meeting)
    feature_dic["user company in title"] = user_company_in_title(meeting)
    feature_dic["zero guests"] = zero_guests(meeting)
    feature_dic["not worktime"] = not_worktime(meeting)
    feature_dic["not workday"] = not_workday(meeting)
    feature_dic["webinar"] = check_webinar(meeting)
    feature_dic["user fullname"] = users_fullname(meeting)
    feature_dic["first name only"] = first_name_only(meeting)
    return feature_dic


        




def checks_success(meeting_list):
    irrelevant_meetings = [meeting for meeting in meeting_list if meeting["Relevant"] == "n"]
    filtered_meetings = [meeting for meeting in meeting_list if basic_check_irrelevant(meeting)]
    print(str(len(filtered_meetings)) + " ", str(len(irrelevant_meetings) - len(filtered_meetings)))
    print(len([1 for meeting in filtered_meetings if meeting["Relevant"] == "n"]))


company_dict = create_company_dict(meeting_list)

joiner_list = ["and", "/", "<>", "x"]

def experiment(meeting):
    for joiner in joiner_list:
        if word_in_title(joiner, meeting):
            first_half = meeting["Meeting Title"]
            
    



