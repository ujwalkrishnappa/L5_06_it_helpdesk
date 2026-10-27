"""IT Helpdesk Ticket Allocator."""
import hmac
import itertools
import json
import os
import re
import subprocess  # nosec B404
from datetime import datetime

MIN_URGENCY = 1
MAX_URGENCY = 5
HIGH_PRIORITY = 4
HOSTNAME_PATTERN = re.compile(
    r"^[A-Za-z0-9]([A-Za-z0-9.-]{0,251}[A-Za-z0-9])?$"
)

tickets = {}
TICKET_IDS = itertools.count(101)


def get_admin_password():
    """Return the admin password configured in the environment."""
    return os.environ.get("HELPDESK_ADMIN_PASSWORD", "")


def raise_ticket(user, issue_type, urgency="3", audit_trail=None):
    """Create a ticket with urgency from 1 to 5 and return its id."""
    if audit_trail is None:
        audit_trail = []
    priority = int(urgency)
    if not MIN_URGENCY <= priority <= MAX_URGENCY:
        raise ValueError(
            f"Urgency must be between {MIN_URGENCY} and {MAX_URGENCY}, "
            f"got {priority}"
        )
    ticket_id = next(TICKET_IDS)
    tickets[ticket_id] = {
        "user": user,
        "issue": issue_type,
        "priority": priority,
        "tech": None,
        "notes": [],
    }
    audit_trail.append(f"{user} raised #{ticket_id} at {datetime.now()}")
    return ticket_id


def assign_ticket(ticket_id, technician):
    """Assign a technician to an existing ticket."""
    tickets[ticket_id]["tech"] = technician


def add_note(ticket_id, note):
    """Add a note to a ticket and report if its id does not exist."""
    try:
        tickets[ticket_id]["notes"].append(note)
    except KeyError:
        print(f"Cannot add note: ticket #{ticket_id} does not exist")
        return False
    return True


def close_ticket(ticket_id, password):
    """Close a ticket only when the configured admin password is correct."""
    admin_password = get_admin_password()
    if not admin_password or not hmac.compare_digest(password, admin_password):
        print("Cannot close ticket: wrong or missing admin password")
        return False
    if ticket_id not in tickets:
        print(f"Cannot close ticket: #{ticket_id} does not exist")
        return False
    del tickets[ticket_id]
    return True


def unresolved_high_priority():
    """Return ids for high-priority tickets without an assigned technician."""
    return [
        ticket_id
        for ticket_id, ticket in tickets.items()
        if ticket["priority"] >= HIGH_PRIORITY and ticket["tech"] is None
    ]


def ping_user_machine(hostname):
    """Ping a machine once and return the command's exit code."""
    if not HOSTNAME_PATTERN.match(hostname):
        raise ValueError(f"Invalid hostname: {hostname!r}")
    count_flag = "-n" if os.name == "nt" else "-c"
    return subprocess.call(  # nosec B603 B607
        ["ping", count_flag, "1", hostname]
    )


def save_tickets(file="tickets.json"):
    """Save all tickets to a JSON file."""
    with open(file, "w", encoding="utf-8") as handle:
        json.dump(tickets, handle)


def main():
    """Run the helpdesk ticket demonstration."""
    printer_ticket = raise_ticket("anil", "printer", "5")
    raise_ticket("meera", "wifi", "4")
    vpn_ticket = raise_ticket("joe", "vpn", "2")
    assign_ticket(printer_ticket, "Tech-Kiran")
    add_note(999, "Called user")
    print("Unassigned high priority:", unresolved_high_priority())
    prompt = "Urgency for a new laptop ticket (1-5, Enter for 3): "
    level = input(prompt) or "3"
    try:
        raise_ticket("sana", "laptop", level)
    except ValueError as error:
        print(f"Ticket not created: {error}")
    close_ticket(vpn_ticket, get_admin_password())
    save_tickets()
    print("Open tickets:", list(tickets.keys()))


if __name__ == "__main__":
    main()
