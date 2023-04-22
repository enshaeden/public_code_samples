from datetime import datetime, timedelta
from dateutil.parser import parse as dparser


"""
Class defining the ticket data object for the Cherwell ticket data.
"""


def read_json(json_file):
    import json
    with open(json_file, encoding='utf-8') as jsonf:
        data = json.load(jsonf)
    return data


def generate_csv_header(output_file):
        print(f"ticket_id\tcreated_date\tcustomer start date\temail\tcustomer\tsubcategory\trole\tteam\tgroup\tfocus area\tline of business\tcustomer_cost_centre\texpedite_asked\tt2_escalation\tt3_escalation\tfirst 30 days", file=open(output_file, "w"))


def output_to_file(ticket_id, created_date, start_date, email, employee_name, ticket_category, role, team, team_group, team_focus, LOB, customer_cost_centre, expedite_asked, t2_requested, t3_requested, first_30_days, output_file):
    """
    Function to return a standard output string for the ticket data.
    """
    print(f"{ticket_id}\t{created_date}\t{start_date}\t{email}\t{employee_name}\t{ticket_category}\t{role}\t{team}\t{team_group}\t{team_focus}\t{LOB}\t{customer_cost_centre}\t{expedite_asked}\t{t2_requested}\t{t3_requested}\t{first_30_days}", file=open(output_file, "a"))


def dict_sort(dictionary):
    """
    Function to sort a dictionary by its values in decending order

    Attributes:
        dictionary (dict): Dictionary to be sorted
    
    Parameters:
        main_dict (dict): Dictionary to be sorted
        sorted_list (list): List of sorted dictionary values
        sorted_dict (dict): Dictionary to be returned

    Returns:
        sorted_dict (dict): Sorted dictionary
    """
    main_dict = dictionary
    sorted_list = sorted(main_dict.values(), reverse=True)
    sorted_dict = {}
    for i in sorted_list:
        for k in main_dict.keys():
            if main_dict[k] == i:
                sorted_dict[k] = main_dict[k]
                break
    return sorted_dict


class Ticket_Details:
    
    def __init__(self, ticket_data, **kwargs):
        """
        Arguments:
            ticket_data: A dictionary containing the ticket data.
        """

        self.ticket_id = ticket_data['\ufeffID']
        self.ticket_category = ticket_data['Subcategory']
        self.ticket_description = ticket_data['Description']
        self.ticket_close_notes = ticket_data['Close Description']
        self.macro_category = ticket_data['Service']
        self.created_date = ticket_data['Created Date Time']
        self.on_behalf_of = ticket_data['On Behalf Of']
        self.requester = ticket_data['Requester']
        self.customer = ticket_data['Customer Name']
        self.email = ticket_data['Email']
        self.customer_department = ticket_data['Requester Department']
        self.customer_cost_centre = ticket_data['CostCenter Name']
        self.Line_of_Business = ticket_data['Line Of Business Name']
        self.assigned_team = ticket_data['Assigned Team']
        self.assignee = ticket_data['Assigned To']
        self.origin = ticket_data['Call Source']
        self.expedite_asked = ticket_data['Expedite Requested']
        self.software_requested = ticket_data['Software List']
        self.t2_requested = ticket_data['Level 2 Escalation Complete']
        self.t2_team = ticket_data['Level 2 Escalation Team']
        self.t3_requested = ticket_data['Level 3 Escalation Complete']
        self.t3_team = ticket_data['Level 3 Escalation Team']
        self.current_status = ticket_data['Status']
        self.csat_summary = ticket_data['Answer Six']
        self.csat_score = ticket_data['Score']
    

    def process_software_requested(self):
        import json

        """
        Function to process the software requested field. If the field is empty, return 'No Software Requested', otherwise return the software requested.
        """
        
        def read_json(json_file):
            with open(json_file, encoding='utf-8') as jsonf:
                data = json.load(jsonf)
            return data

        if self.ticket_category == "Approved Software Access":
            if self.software_requested == '':
                return 'No software requested'

            # Find software whose's selection is "Other" in the list
            elif "Other" in self.software_requested:
                # Gather a list of all software titles from the G2_Data.json file.
                approved_software_list = []
                g2_info = read_json('./Data/Source/known_approved_software.json')
                for row in g2_info:
                    if "Product Name" in row:
                        app = G2_title_data(row)
                        software_title = app.software_title
                    if software_title not in approved_software_list:
                        approved_software_list.append(software_title)

                # Add software titles to a list if they a match is found between the G2 titles and the user's comments
                software_requested_list = {"Other": []}
                ticket_comments = self.ticket_description.lower()
                
                for software in approved_software_list:
                    if software.lower() in ticket_comments and "Microsoft" not in software:
                        software_requested_list["Other"].append(software)
                    
                    # Microsoft Office multiple title filter
                    if "microsoft" in ticket_comments or "ms" in ticket_comments or "excel" in ticket_comments or "powerpoint" in ticket_comments or "word" in ticket_comments:
                        return "Microsoft Office"

                    # Jetbrains multiple title filter
                    if "jetbrains" in ticket_comments or "intellij" in ticket_comments or "webstorm" in ticket_comments or "phpstorm" in ticket_comments:
                        return "Jetbrains products"
                    elif "pycharm" in ticket_comments:
                        return "PyCharm"
                    elif "goland" in ticket_comments:
                        return "GoLand"

                return software_requested_list

        elif self.ticket_category == "Microsoft Office":
            keyword_library = ["access", "set up", "setup", "need", "license", "licensing", "requesting", "request", "provision", "provide", "grant", "install", "download"]
            for word in range(0, len(keyword_library)):
                if keyword_library[word] in self.ticket_description.lower():
                    return "Microsoft Office"
        
        elif self.ticket_category == "Tableau Access":
            return "Tableau Software"
        
        else:
            return self.software_requested


    def ticket_type(self):
        ticket_categories = read_json('/Users/jsadow/src/Service Desk Tools/Cherwell_Ticket_Processing/Data/Source/catalog_pathways.json')
        for row in ticket_categories:
            # print(self.ticket_category)
            # print(row)
            if self.ticket_category == row['Subcategory']:
                # print(row['Incident Type'])
                return row['Incident Type']


class Ticket_Filters:
    class Time_Based_Filters:


        def find_this_year():
            output_file = './Data/Output/This_Year_Tickets.tsv'
            workday_data = read_json('./Data/Source/Workday_Export.json')
            ticket_data = read_json('./Data/Source/converted_csv.json')
            this_year = datetime.now().strftime("%Y")
            first_30_days = "NULL"
            generate_csv_header(output_file)
            for row in ticket_data:
                ticket = Ticket_Details(row)
                if this_year in ticket.created_date:
                    if ticket.customer != "Default Customer":
                        for row in workday_data:
                            user = Workday_Information(row)
                            if ticket.email == user.email:
                                output_to_file(ticket.ticket_id, ticket.created_date, user.start_date, user.email, user.employee_name, ticket.ticket_category, user.role, user.team, user.team_group, user.team_focus, user.LOB, ticket.customer_cost_centre, ticket.expedite_asked, ticket.t2_requested, ticket.t3_requested, first_30_days, output_file)

        
        def find_this_month():
            output_file = './Data/Output/This_Month_Tickets.tsv'
            workday_data = read_json('./Data/Source/Workday_Export.json')
            ticket_data = read_json('./Data/Source/converted_csv.json')
            this_month = datetime.now().strftime("%m")
            this_year = datetime.now().strftime("%Y")
            first_30_days = "NULL"
            generate_csv_header(output_file)
            for row in ticket_data:
                ticket = Ticket_Details(row)
                ticket_date = dparser(ticket.created_date, fuzzy=True, dayfirst=True).strftime("%m")
                ticket_year = dparser(ticket.created_date, fuzzy=True, dayfirst=True).strftime("%Y")
                if this_month == ticket_date and this_year == ticket_year:
                    if ticket.customer != "Default Customer":
                        for line in workday_data:
                            user = Workday_Information(line)
                            if ticket.email == user.email:
                                output_to_file(ticket.ticket_id, ticket.created_date, user.start_date, user.email, user.employee_name, ticket.ticket_category, user.role, user.team, user.team_group, user.team_focus, user.LOB, ticket.customer_cost_centre, ticket.expedite_asked, ticket.t2_requested, ticket.t3_requested, first_30_days, output_file)


        def find_this_week():
            output_file = './Data/Output/This_Week_Tickets.tsv'
            workday_data = read_json('./Data/Source/Workday_Export.json')
            ticket_data = read_json('./Data/Source/converted_csv.json')
            this_week = datetime.now().strftime("%U")
            this_year = datetime.now().strftime("%Y")
            first_30_days = "NULL"
            generate_csv_header(output_file)
            for row in ticket_data:
                ticket = Ticket_Details(row)
                ticket_week = dparser(ticket.created_date, fuzzy=True, dayfirst=True).strftime("%U")
                ticket_year = dparser(ticket.created_date, fuzzy=True, dayfirst=True).strftime("%Y")
                if this_week == ticket_week and this_year == ticket_year:
                    if ticket.customer != "Default Customer":
                        for line in workday_data:
                            user = Workday_Information(line)
                            if ticket.email == user.email:
                                output_to_file(ticket.ticket_id, ticket.created_date, user.start_date, user.email, user.employee_name, ticket.ticket_category, user.role, user.team, user.team_group, user.team_focus, user.LOB, ticket.customer_cost_centre, ticket.expedite_asked, ticket.t2_requested, ticket.t3_requested, first_30_days, output_file)


        def find_last_week():
                output_file = './Data/Output/Last_Week_Tickets.tsv'
                workday_data = read_json('./Data/Source/Workday_Export.json')
                ticket_data = read_json('./Data/Source/converted_csv.json')
                last_week = (datetime.now() + timedelta(weeks=-1)).strftime("%U")
                this_year = datetime.now().strftime("%Y")
                first_30_days = "NULL"
                generate_csv_header(output_file)
                for row in ticket_data:
                    ticket = Ticket_Details(row)
                    ticket_date = ((dparser(ticket.created_date, fuzzy=True, dayfirst=True))).strftime("%U")
                    ticket_year = dparser(ticket.created_date, fuzzy=True, dayfirst=True).strftime("%Y")
                    if last_week == ticket_date and this_year == ticket_year:
                        if ticket.customer != "Default Customer":
                            for line in workday_data:
                                user = Workday_Information(line)
                                if user.email == ticket.email:
                                    output_to_file(ticket.ticket_id, ticket.created_date, user.start_date, user.email, user.employee_name, ticket.ticket_category, user.role, user.team, user.team_group, user.team_focus, user.LOB, ticket.customer_cost_centre, ticket.expedite_asked, ticket.t2_requested, ticket.t3_requested, first_30_days, output_file)


        def week_over_week():
            this_week_count = 0
            this_week_last_year = 0
            last_week_count = 0
            last_week_last_year = 0

            workday_data = read_json('./Data/Source/Workday_Export.json')
            ticket_data = read_json('./Data/Source/converted_csv.json')
            this_week = datetime.now().strftime("%U")
            last_week = (datetime.now() + timedelta(weeks=-1)).strftime("%U")
            this_year = datetime.now().strftime("%Y")
            last_year = (datetime.now() + timedelta(weeks=-52)).strftime("%Y")

            for row in ticket_data:
                ticket = Ticket_Details(row)
                ticket_date = ((dparser(ticket.created_date, fuzzy=True, dayfirst=True))).strftime("%U")
                ticket_year = dparser(ticket.created_date, fuzzy=True, dayfirst=True).strftime("%Y")

                if this_year == ticket_year:
                    if last_week == ticket_date:
                        if ticket.customer != "Default Customer":
                            last_week_count += 1
                    if this_week == ticket_date:
                        if ticket.customer != "Default Customer":
                            this_week_count += 1
                elif last_year == ticket_year:
                    if last_week == ticket_date:
                        if ticket.customer != "Default Customer":
                            last_week_last_year += 1
                    if this_week == ticket_date:
                        if ticket.customer != "Default Customer":
                            this_week_last_year += 1
            return this_week_count, this_week_last_year, last_week_count, last_week_last_year


    class New_Hire_Filters:

        def find_new_hire_tickets_incidents():
            cherwell_data = read_json('./Data/Source/converted_csv.json')
            workday_data = read_json('./Data/Source/Workday_Export.json')
            output_file = './Data/Output/new_hire_incidents.tsv'
            generate_csv_header(output_file)
            for row in cherwell_data:
                ticket = Ticket_Details(row)
                user_email = ticket.email
                ticket_type = ticket.ticket_type()
                if ticket_type == "Incident":
                    if user_email != "":
                        for row2 in workday_data:
                            user = Workday_Information(row2)
                            if user.email == user_email:
                                if User_Information.new_hire_requests(user.start_date, ticket.created_date):
                                    if ticket.ticket_category != "Approved Software Access" and ticket.ticket_category != "Microsoft Office" and ticket.ticket_category != "Tableau Access":
                                        print(f"{ticket.ticket_id}\t{ticket.created_date}\t{user.start_date}\t{user.email}\t{user.employee_name}\t{ticket.ticket_category}\t{user.role}\t{user.team}\t{user.team_group}\t{user.team_focus}\t{user.LOB}\t{ticket.customer_cost_centre}\t{ticket.expedite_asked}\t{ticket.t2_requested}\t{ticket.t3_requested}\tTrue", file=open(output_file, "a"))

                            
        def find_new_hire_tickets_requests():
            cherwell_data = read_json('./Data/Source/converted_csv.json')
            workday_data = read_json('./Data/Source/Workday_Export.json')
            output_file = './Data/Output/new_hire_requests.tsv'
            generate_csv_header(output_file)
            for row in cherwell_data:
                ticket = Ticket_Details(row)
                user_email = ticket.email
                ticket_type = ticket.ticket_type()
                # print(ticket_type)
                if ticket_type == "Service Request":
                    if user_email != "":
                        for row2 in workday_data:
                            user = Workday_Information(row2)
                            if user.email == user_email:
                                if User_Information.new_hire_requests(user.start_date, ticket.created_date):
                                    if ticket.ticket_category != "Approved Software Access" and ticket.ticket_category != "Microsoft Office" and ticket.ticket_category != "Tableau Access":
                                        print(f"{ticket.ticket_id}\t{ticket.created_date}\t{user.start_date}\t{user.email}\t{user.employee_name}\t{ticket.ticket_category}\t{user.role}\t{user.team}\t{user.team_group}\t{user.team_focus}\t{user.LOB}\t{ticket.customer_cost_centre}\t{ticket.expedite_asked}\t{ticket.t2_requested}\t{ticket.t3_requested}\tTrue", file=open(output_file, "a"))


    class Subcategory_Filters:


        def subcategory_counter():
            cherwell_json = './Data/Source/converted_csv.json'
            cherwell_data = read_json(cherwell_json)
            category_count_file = './Data/Output/category_count.tsv'
            new_hire_count_file = './Data/Output/category_new_hire_count.tsv'
            category_count = {}
            tickets_counted = {}
            
            generate_csv_header(new_hire_count_file)
            for row in cherwell_data:
                ticket = Ticket_Details(row)
                incident_type = ticket.ticket_type()
                requester = ticket.email
                created_date = ticket.created_date
                ticket_id = ticket.ticket_id
                ticket_category = ticket.ticket_category
                customer_cost_centre = ticket.customer_cost_centre
                expedite_asked = ticket.expedite_asked
                t2_requested = ticket.t2_requested
                t3_requested = ticket.t3_requested
                software_requested = ticket.process_software_requested()
                first_30_days = "NULL"
                

                if software_requested == '' and ticket_id not in tickets_counted:
                    tickets_counted[ticket_id] = "True"
                    try:
                        start_date, user_role, user_team, user_team_group, user_team_focus, user_LOB, employee_name = User_Information.generate_user_information(requester)
                        new_hire_check = User_Information.new_hire_requests(start_date, created_date)
                    except TypeError:
                        pass

                    if incident_type == "Service Request":
                        if ticket_category not in category_count:
                            category_count[ticket_category] = 1
                        elif ticket_category in category_count:
                            category_count[ticket_category] += 1
                    
                        if new_hire_check:
                            output_to_file(ticket_id, created_date, start_date, requester, employee_name, ticket_category, user_role, user_team, user_team_group, user_team_focus, user_LOB, customer_cost_centre, expedite_asked, t2_requested, t3_requested, first_30_days, new_hire_count_file)

                elif ticket_id in tickets_counted:
                    pass

            print("sorting...")
            sorted_count = dict_sort(category_count)
            print("Category\tCount", file=open(category_count_file, "w"))
            for key, value in sorted_count.items():
                print(f"{key}\t{value}", file=open(category_count_file, "a"))


        def count_submit_request_word_weights():
            cherwell_json = './Data/Source/converted_csv.json'
            cherwell_data = read_json(cherwell_json)
            word_count = {}

            for row in cherwell_data:
                ticket = Ticket_Details(row)
                category = ticket.ticket_category

                if category == "Submit Request":
                    summary = ticket.ticket_description.lower()
                    summarylist = summary.split()

                    for word in summarylist:
                        if word not in word_count:
                            word_count[word] = 1
                        elif word in word_count:
                            word_count[word] += 1
            sort = dict_sort(word_count)
            print(f"Word\tCount", file=open('./Data/Output/submit_request_word_count.tsv', 'w'))
            for key, value in sort.items():
                print(f"{key}\t{value}", file=open('./Data/Output/submit_request_word_count.tsv', 'a'))


        def count_submit_request_subcategory():
            give_me_words = ["access", "request", "requested", "need", "add", "wanted"]
            software_words = ["okta", "google", "email", "account", "slack", "tile", "app", "mode", "software", "drive", "jira", "folder", "acl", "tableau", "workday", "adobe", "adp", "api"]
            hardware_words = ["laptop", "phone"]

            cherwell_file = read_json('./Data/Source/converted_csv.json')

            processed_tickets = {}
            requests = {}

            print(f"Ticket\tRequest", file=open('./Data/Output/Submit_Request_Filter.tsv', 'w'))
            for row in cherwell_file:
                ticket = Ticket_Details(row)
                ticket_category = ticket.ticket_category
                ticket_id = ticket.ticket_id

                if ticket_category not in processed_tickets:
                    processed_tickets[ticket_id] = "True"

                    if ticket_category == "Submit Request":
                        ticket_summary = ticket.ticket_description.lower()
                        
                        for word in give_me_words:
                            if word in ticket_summary:
                                softrequested = []
                                for softrequest in software_words:
                                    if softrequest in ticket_summary:
                                        softrequested.append(softrequest)
                                if softrequested:
                                    requests[ticket_id] = f"{word} {softrequested}"
                                for hardrequest in hardware_words:
                                    if hardrequest in ticket_summary:
                                        requests[ticket_id] = f"{word} {hardrequest}"
                else:
                    pass

            for key, value in requests.items():
                print(f"{key}\t{value}", file=open('./Data/Output/Submit_Request_Filter.tsv', 'a'))

            print(f"Recommending 'Submit Request' re-classifications")
            Subcategory_Filters.recommend_recategorization_submit_request(requests)


        def recommend_recategorization_submit_request(requests):
            approved_software_file = './Data/Source/known_approved_software.json'
            approved_software_data = read_json(approved_software_file)

            print(f"Ticket\tRecategory", file=open('./Data/Output/Recategory_Filter.tsv', 'w'))
            for row in requests:
                for line in approved_software_data:
                    app = G2_title_data(line)
                    if app.software_title.lower() in requests[row]:

                        if "google" != app.software_title.lower():
                            print(f"{row}\t\"Approved Software Access\"", file=open('./Data/Output/Recategory_Filter.tsv', 'a'))
                        elif "google" == app.software_title.lower():
                            print(f"{row}\t\"Gmail/ Calendar\"", file=open('./Data/Output/Recategory_Filter.tsv', 'a')) 


class Team_Stats:


    def get_my_team_last_week(assignee):
        output_file = f'./Data/Output/{assignee}_Last_Week_Tickets.tsv'
        workday_data = read_json('./Data/Source/Workday_Export.json')
        ticket_data = read_json('./Data/Source/converted_csv.json')
        last_week = (datetime.now() + timedelta(weeks=-1)).strftime("%U")
        this_year = datetime.now().strftime("%Y")
        first_30_days = "NULL"
        
        generate_csv_header(output_file)
        
        for row in ticket_data:
            ticket = Ticket_Details(row)
            ticket_date = ((dparser(ticket.created_date, fuzzy=True, dayfirst=True))).strftime("%U")
            ticket_year = dparser(ticket.created_date, fuzzy=True, dayfirst=True).strftime("%Y")
            
            if ticket.assignee == assignee:
                if last_week == ticket_date and this_year == ticket_year:
                    if ticket.customer != "Default Customer":
                        for line in workday_data:
                            user = Workday_Information(line)
                            if user.email == ticket.email:
                                output_to_file(ticket.ticket_id, ticket.created_date, user.start_date, user.email, user.employee_name, ticket.ticket_category, user.role, user.team, user.team_group, user.team_focus, user.LOB, ticket.customer_cost_centre, ticket.expedite_asked, ticket.t2_requested, ticket.t3_requested, first_30_days, output_file)
            else:
                continue


class G2_title_data:

    def __init__(self, g2_data):
        self.software_title = g2_data['Product Name']


class Workday_Information:
    """
    Class to store the workday information for a user.
    """

    def __init__(self, workday_json, **kwargs):
        self.employee_firstname = workday_json['First Name']
        self.employee_lastname = workday_json['Last Name']
        self.employee_name = f"{self.employee_firstname} {self.employee_lastname}"
        self.email = workday_json['Work Email']
        self.start_date = workday_json['Start Date']
        self.role = workday_json['Job Family']
        self.team = workday_json['Team']
        self.team_group = workday_json['Group']
        self.team_focus = workday_json['Focus Area']
        self.LOB = workday_json['Line of Business']


    def workday_to_dict():
        import csv_reader
        
        workday_raw = './Data/Source/Workday_Export.csv'
        workday_json = './Data/Source/Workday_Export.json'
        
        # Make sure the json file exists
        csv_reader.csv_to_json(workday_raw, workday_json)

        workday_info = read_json(workday_json)
        user_data = {}
        for row in workday_info:
            user = Workday_Information(row)
            user_data[user.employee_name] = f"{user.role}, {user.start_date}, {user.team}, {user.team_group}, {user.team_focus}"
        
        return user_data
    

class User_Information:

    def new_hire_requests(start_date, ticket_date):
        from dateutil.parser import parse as dparser
        import datetime as datetime
        new_hire_requests = False
        user_start_date = dparser(start_date, fuzzy=True)
        ticket_date = dparser(ticket_date, fuzzy=True, dayfirst=True)
        if ticket_date <= (user_start_date + datetime.timedelta(days=30)):
            new_hire_requests = True
        return new_hire_requests


    def generate_user_information(user_inquest):
        workday_data = read_json('./Data/Source/Workday_Export.json')
        if user_inquest != "Default Customer":
            for row in workday_data:
                user = Workday_Information(row)
                email = user.email
                if email == user_inquest:
                    start_date = user.start_date
                    user_role = user.role
                    user_team = user.team
                    user_team_group = user.team_group
                    user_team_focus = user.team_focus
                    user_LOB = user.LOB
                    user_name = user.employee_name
                    return start_date, user_role, user_team, user_team_group, user_team_focus, user_LOB, user_name


if __name__ == "__main__":
    # ticket_data_raw = '/Users/jsadow/src/Service Desk Tools/Cherwell_Ticket_Processing/Data/Source/converted_csv.json'
    # ticket_data = read_json(ticket_data_raw)

    # workday_data_raw = '/Users/jsadow/src/Service Desk Tools/Cherwell_Ticket_Processing/Data/Source/Workday_Export.json'
    # workday_data = read_json(workday_data_raw)

    g2_data_raw = '/Users/jsadow/src/Service Desk Tools/Cherwell_Ticket_Processing/Data/Source/known_approved_software.json'
    g2_data = read_json(g2_data_raw)
    titles = {}

    for title in g2_data:
        app = G2_title_data(title)