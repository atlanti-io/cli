import time
import subprocess
from rich.console import Console
from rich.panel import Panel
import requests  # Ensure `requests` is installed with `pip install requests`
from rich.prompt import Prompt
import re  # Importing regex for email validation

console = Console()

API_URL = "https://6731fd217aaf2a9aff13009e.mockapi.io/api/v1"

EMAIL_REGEX = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

def send_otp_request(email):
    """Requests an OTP by sending the email to the API."""
    try:
        response = requests.post(f"{API_URL}/request-otp", json={"email": email}, timeout=15)
        if response.status_code == 200 or response.status_code == 201:
            return True
        elif response.status_code == 400:
            console.print("[red]Failed to request OTP: Invalid email format.[/red]")
        elif response.status_code == 429:
            console.print("[red]Failed to request OTP: Too many requests. Please try again later.[/red]")
        elif response.status_code == 500:
            console.print("[red]Failed to request OTP: Server error. Please try again later.[/red]")
        else:
            console.print(f"[red]Failed to request OTP. Error code: {response.status_code}[/red]")
    except requests.exceptions.Timeout:
        console.print("[red]Request timed out. Please try again later.[/red]")
        if not retry_or_cancel("request OTP"):
            return False
    except requests.exceptions.RequestException as e:
        console.print(f"[red]Request failed: {e}[/red]")
        if not retry_or_cancel("request OTP"):
            return False
    return False

def retry_or_cancel(action):
    """Ask the user whether to retry or cancel the action."""
    retry = Prompt.ask(f"Do you want to retry the {action}? (y/n)", choices=["y", "n"], default="y")
    if retry == "y":
        return True
    return False

def verify_otp(email, otp):
    """Verifies the entered OTP and returns the token if successful."""
    try:
        response = requests.post(f"{API_URL}/verify-otp", json={"email": email, "otp": otp}, timeout=15)
        if response.status_code == 200 or response.status_code == 201:
            return response.json().get("token")  # Assuming the server returns a token
        elif response.status_code == 400:
            console.print("[red]Invalid OTP: Please check the code and try again.[/red]")
        elif response.status_code == 401:
            console.print("[red]Unauthorized: OTP verification failed. Please request a new OTP.[/red]")
        elif response.status_code == 500:
            console.print("[red]OTP verification failed: Server error. Please try again later.[/red]")
        else:
            console.print(f"[red]OTP verification failed. Error code: {response.status_code}[/red]")
    except requests.exceptions.Timeout:
        console.print("[red]Request timed out. Please try again later.[/red]")
        if not retry_or_cancel("verify OTP"):
            return None
    except requests.exceptions.RequestException as e:
        console.print(f"[red]Request failed: {e}[/red]")
        if not retry_or_cancel("verify OTP"):
            return None
    return None

def submit_ticket(description, message, email, otp_token):
    """Submits the ticket to the API along with the OTP token."""
    try:
        response = requests.post(f"{API_URL}/submit-ticket", json={
            "description": description,
            "message": message,
            "email": email,
            "otp_token": otp_token  # Send the OTP token with the ticket
        }, timeout=15)
        if response.status_code == 200:
            return True
        elif response.status_code == 400:
            console.print("[red]Failed to send ticket: Invalid data format.[/red]")
        elif response.status_code == 500:
            console.print("[red]Failed to send ticket: Server error. Please try again later.[/red]")
        else:
            console.print(f"[red]Failed to send ticket. Error code: {response.status_code}[/red]")
    except requests.exceptions.Timeout:
        console.print("[red]Request timed out. Please try again later.[/red]")
        if not retry_or_cancel("submit ticket"):
            return False
    except requests.exceptions.RequestException as e:
        console.print(f"[red]Request failed: {e}[/red]")
        if not retry_or_cancel("submit ticket"):
            return False
    return False

def is_valid_email(email):
    """Validates the email format using regex."""
    return re.match(EMAIL_REGEX, email) is not None

def open_ticket():
    console.clear()
    console.print(Panel(
        "🌐 Atlanti.io - Open a Ticket\n\n"
        "Experiencing an issue with your server?\n"
        "Contact our team of experts for technical assistance and reliable support.",
        expand=False, style="cyan"
    ))

    try:
        short_description = ""
        while len(short_description) < 5:
            short_description = Prompt.ask("[magenta]Short description[/magenta]", default="e.g., Server is down")
            if len(short_description) < 5:
                console.print("[red]Description must be at least 5 characters long.[/red]")

        message = ""
        while len(message) < 10:
            message = Prompt.ask("[magenta]Your message[/magenta]", default="e.g., The server stopped responding after the last update.")
            if len(message) < 10:
                console.print("[red]Message must be at least 10 characters long.[/red]")

        email = ""
        while not is_valid_email(email):
            email = Prompt.ask("[magenta]Your email[/magenta]", default="e.g., bugs.bunny@acme.inc")
            if not is_valid_email(email):
                console.print("[red]Invalid email format. Please enter a valid email address.[/red]")

        if not send_otp_request(email):
            return  # End if OTP request failed

        otp = console.input("Enter the OTP sent to your email: ")

        otp_token = verify_otp(email, otp)
        if not otp_token:
            console.print("[red]Invalid OTP. Ticket creation canceled.[/red]")
            console.input("Press Enter to return to the main menu.")  # Pause before returning
            return

        if submit_ticket(short_description, message, email, otp_token):
            console.clear()
            console.print(Panel("✅ [bold green]Ticket sent successfully![/bold green]", expand=False, style="green"))
            time.sleep(3)  # Show confirmation for 3 seconds
        else:
            console.print("[red]Failed to send the ticket. Please try again later.[/red]")
            console.input("Press Enter to return to the main menu.")  # Pause before returning

    except KeyboardInterrupt:
        console.clear()
        console.print(Panel("⚠️ Ticket creation canceled. Returning to the main menu...", style="yellow"))
