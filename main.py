# main.py

# -----------------------------
# IT Incident Prioritization
# -----------------------------

# Import functions from incident.py
from incident import add_incident, view_incidents, rank_incidents, update_incident_status
from incident import generate_html_report, incidents


def choose_report_type():
    """
    Ask the user which report to generate: all incidents or ranked OPEN incidents.
    """
    while True:
        print("\nSelect report type:")
        print("1. All incidents")
        print("2. OPEN incidents (ranked by priority)")
        choice = input("Enter 1 or 2: ").strip()
        if choice == "1":
            generate_html_report(ranked=False)
            break
        elif choice == "2":
            generate_html_report(ranked=True)
            break
        else:
            print("Invalid choice. Please enter 1 or 2.")


def main_menu():
    """
    This function displays the main menu and
    handles user interaction.
    """

    while True:  # Keeps the menu running until user exits
        print("\n=== IT Incident Prioritization System ===")
        print("1. Add new incident")
        print("2. View all incidents") 
        print("3. Rank OPEN incidents by priority")
        print("4. Resolve an incident")
        print("5. Exit")
        print("6. Export incidents to HTML report")

        choice = input("Choose an option (1-6): ")

        if choice == "1":
            add_incident()
        elif choice == "2":
            view_incidents()
        elif choice == "3":
            rank_incidents()
        elif choice == "4":
            update_incident_status()
        elif choice == "5":  # Exit
            if incidents:  # only ask if there are incidents
                answer = input("Do you want to generate an HTML report before exiting? (y/n): ").strip().lower()
                if answer in ["y", "yes"]:
                    choose_report_type()  # ask what type of report
            print("Exiting program. Goodbye!")
            break

        elif choice == "6":  # Export report from menu
            if not incidents:
                print("No incidents available to report.")
            else:
                choose_report_type()
                print("Report exported. Returning to menu...")
        else:
            print("Invalid choice. Please enter a number between 1 and 6.")


# Program entry point
if __name__ == "__main__":
    main_menu()
