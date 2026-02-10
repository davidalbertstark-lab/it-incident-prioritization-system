import webbrowser

# This list will store all incidents while the program is running
incidents = []

# -----------------------------
# Terminal color codes
# -----------------------------
RED = "\033[91m"
GREEN = "\033[92m"
RESET = "\033[0m"


# -----------------------------
# Function: Add a new incident
# -----------------------------
def add_incident():
    """
    This function collects incident details from the user
    and stores them in the incidents list.
    It prevents duplicate Incident IDs and validates inputs.
    """

    print("\n--- Add New Incident ---")

    # Incident ID input loop (must be unique)
    while True:
        incident_id = input("Enter Incident ID (e.g. INC001): ").strip()
        if any(incident["id"] == incident_id for incident in incidents):
            print(f"{RED}Notice: An incident with ID '{incident_id}' already exists. Please use a unique ID.{RESET}")
        else:
            break

    # System name input (cannot be empty)
    while True:
        system = input("Enter System Name (e.g. Checkout Service): ").strip()
        if system:
            break
        print(f"{RED}System Name cannot be empty.{RESET}")

    # Severity input validation
    while True:
        severity = input("Enter Severity (Low / Medium / High): ").capitalize()
        if severity in ["Low", "Medium", "High"]:
            break
        print(f"{RED}Invalid input. Please enter Low, Medium, or High.{RESET}")

    # Urgency input validation
    while True:
        urgency = input("Enter Urgency (Low / Medium / High): ").capitalize()
        if urgency in ["Low", "Medium", "High"]:
            break
        print(f"{RED}Invalid input. Please enter Low, Medium, or High.{RESET}")

    # Frequency input validation
    while True:
        frequency = input("Enter Frequency (Rare / Occasional / Frequent): ").capitalize()
        if frequency in ["Rare", "Occasional", "Frequent"]:
            break
        print(f"{RED}Invalid input. Please enter Rare, Occasional, or Frequent.{RESET}")

    # Create a dictionary to represent one incident
    incident = {
        "id": incident_id,
        "system": system,
        "severity": severity,
        "urgency": urgency,
        "frequency": frequency,
        "status": "OPEN"
    }

    # Add the incident to the global incidents list
    incidents.append(incident)

    print("Incident added successfully!")


# -----------------------------
# Function: View all incidents
# -----------------------------
def view_incidents():
    """
    Display all incidents in a clean table format with status colors.
    """

    print("\n--- All Incidents ---")

    if not incidents:
        print("No incidents recorded yet.")
        return

    # Table header
    header = f"{'ID':<10} {'System':<20} {'Severity':<10} {'Urgency':<10} {'Frequency':<12} {'Status':<10}"
    print(header)
    print("-" * len(header))  # separator line

    # Table rows
    for incident in incidents:
        status = incident["status"]
        if status == "OPEN":
            status_display = f"{RED}{status}{RESET}"
        else:
            status_display = f"{GREEN}{status}{RESET}"

        row = f"{incident['id']:<10} {incident['system']:<20} {incident['severity']:<10} {incident['urgency']:<10} {incident['frequency']:<12} {status_display:<10}"
        print(row)


# -----------------------------
# Function: Rank incidents by priority
# -----------------------------
def rank_incidents():
    """
    This function calculates priority scores for incidents
    and displays them in ranked order.
    """

    print("\n--- Incident Priority Ranking ---")

    # If there are no incidents, nothing to rank
    if not incidents:
        print("No incidents to rank.")
        return

    # Mapping qualitative values to numbers
    level_map = {
        "Low": 1,
        "Medium": 2,
        "High": 3,
        "Rare": 1,
        "Occasional": 2,
        "Frequent": 3
    }

    # Weights (importance of each factor)
    severity_weight = 0.5
    urgency_weight = 0.3
    frequency_weight = 0.2

    # Calculate priority score for each incident
    open_incidents = [i for i in incidents if i["status"] == "OPEN"]

    if not open_incidents:
        print("No OPEN incidents to rank.")
        return

    for incident in open_incidents:

        severity_score = level_map.get(incident["severity"], 0)
        urgency_score = level_map.get(incident["urgency"], 0)
        frequency_score = level_map.get(incident["frequency"], 0)

        priority_score = (
            severity_score * severity_weight +
            urgency_score * urgency_weight +
            frequency_score * frequency_weight
        )

        incident["priority_score"] = round(priority_score, 2)

    # Sort incidents by priority score (highest first)
    ranked_incidents = sorted(
        open_incidents,
        key=lambda x: x["priority_score"],
        reverse=True
    )

    # Display ranked incidents in table
    header = f"{'Rank':<5} {'ID':<10} {'System':<20} {'Severity':<10} {'Urgency':<10} {'Frequency':<12} {'Score':<6}"
    print(header)
    print("-" * len(header))

    for index, incident in enumerate(ranked_incidents, start=1):
        row = f"{index:<5} {incident['id']:<10} {incident['system']:<20} {incident['severity']:<10} {incident['urgency']:<10} {incident['frequency']:<12} {incident['priority_score']:<6}"
        print(row)


# -----------------------------
# Function: Update incident status
# -----------------------------
def update_incident_status():
    """
    Allows the user to mark an incident as RESOLVED.
    Keeps asking until a valid Incident ID is provided.
    """

    print("\n--- Update Incident Status ---")

    if not incidents:
        print("No incidents available.")
        return

    while True:
        incident_id = input("Enter Incident ID to resolve (or type 'cancel' to go back): ").strip()
        if incident_id.lower() == "cancel":
            print("Operation cancelled.")
            return

        for incident in incidents:
            if incident["id"] == incident_id:
                incident["status"] = "RESOLVED"
                print(f"{GREEN}Incident marked as RESOLVED.{RESET}")
                return

        print(f"{RED}Incident ID not found. Please try again.{RESET}")


import os

# -----------------------------
# Function: Generate HTML report
# -----------------------------
def generate_html_report(ranked=False):
    """
    Generate an HTML table report for incidents.
    If ranked=True, only OPEN incidents are sorted by priority score.
    The report is saved to reports/incidents.html and opened in the browser.
    """

    # Make sure the reports/ folder exists
    os.makedirs("reports", exist_ok=True)

    # Choose incidents to report
    if ranked:
        # Only OPEN incidents, ranked by priority
        level_map = {"Low": 1, "Medium": 2, "High": 3, "Rare": 1, "Occasional": 2, "Frequent": 3}
        severity_weight, urgency_weight, frequency_weight = 0.5, 0.3, 0.2
        open_incidents = [i for i in incidents if i["status"] == "OPEN"]

        for incident in open_incidents:
            priority_score = (
                level_map.get(incident["severity"], 0) * severity_weight +
                level_map.get(incident["urgency"], 0) * urgency_weight +
                level_map.get(incident["frequency"], 0) * frequency_weight
            )
            incident["priority_score"] = round(priority_score, 2)

        incident_list = sorted(open_incidents, key=lambda x: x["priority_score"], reverse=True)
    else:
        # All incidents, no ranking
        incident_list = incidents

    # Start HTML content
    html_content = """
    <html>
    <head>
        <title>IT Incident Report</title>
        <style>
            table {border-collapse: collapse; width: 100%;}
            th, td {border: 1px solid #999; padding: 8px; text-align: left;}
            th {background-color: #f2f2f2;}
            .open {color: red; font-weight: bold;}
            .resolved {color: green; font-weight: bold;}
        </style>
    </head>
    <body>
        <h2>IT Incident Report</h2>
        <table>
            <tr>
                <th>Rank</th>
                <th>ID</th>
                <th>System</th>
                <th>Severity</th>
                <th>Urgency</th>
                <th>Frequency</th>
                <th>Status</th>
    """

    if ranked:
        html_content += "<th>Priority Score</th>"

    html_content += "</tr>"

    # Add table rows
    for idx, incident in enumerate(incident_list, start=1):
        status_class = "open" if incident["status"] == "OPEN" else "resolved"
        html_content += f"<tr>"
        html_content += f"<td>{idx if ranked else ''}</td>"
        html_content += f"<td>{incident['id']}</td>"
        html_content += f"<td>{incident['system']}</td>"
        html_content += f"<td>{incident['severity']}</td>"
        html_content += f"<td>{incident['urgency']}</td>"
        html_content += f"<td>{incident['frequency']}</td>"
        html_content += f"<td class='{status_class}'>{incident['status']}</td>"
        if ranked:
            html_content += f"<td>{incident.get('priority_score', '')}</td>"
        html_content += "</tr>"

    # Close HTML
    html_content += """
        </table>
    </body>
    </html>
    """

    # Write to file
    report_path = "reports/incidents.html"
    with open(report_path, "w") as file:
        file.write(html_content)

    print(f"HTML report generated: {report_path}")

    # Open in default browser
    webbrowser.open(report_path)
