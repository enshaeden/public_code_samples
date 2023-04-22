import Classes.Ticket_Data as Ticket_Data
import csv_reader
import software_requests_with_csv_out as software_requests

if __name__ == "__main__":
    # csv_reader.run()

    Ticket_Filter = Ticket_Data.Ticket_Filters

    print(f"Finding tickets from this year...")
    Ticket_Filter.find_this_year()
    print(f"Finding tickets from this month...")
    Ticket_Filter.find_this_month()
    print(f"Finding tickets from this week...")
    Ticket_Filter.find_this_week()
    print(f"Finding tickets from last week...")
    Ticket_Filter.find_last_week()
    print(f"Finding new hire incident tickets...")
    Ticket_Filter.find_new_hire_tickets_incidents()
    print(f"Finding new hire request tickets...")
    Ticket_Filter.find_new_hire_tickets_requests()
    print(f"Counting all subcategories...")
    Ticket_Filter.subcategory_counter()
    print(f"Counting all 'Submit Request' subcategories and recommending re-classifications...")
    Ticket_Filter.count_submit_request_subcategory()
    print(f"Counting all Software Requests...")
    software_requests.run()
    print(f"Getting team stats...")
    Ticket_Filter.get_my_team_last_week("Rodel Estioco")
    Ticket_Filter.get_my_team_last_week("Kevin Kuchar")
    Ticket_Filter.get_my_team_last_week("Austen Ezenwa")
    
    Ticket_stats = Ticket_Data.Statistics

    this_week_count, this_week_last_year, last_week_count, last_week_last_year = Ticket_stats.week_over_week()

    print(f"""
Tickets last week: {last_week_count}
Tickets this week: {this_week_count}
This Week, Last Year: {this_week_last_year}
Last Week, Last Year: {last_week_last_year}
""")