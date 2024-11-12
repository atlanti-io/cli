from rich.table import Table
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
import argparse
from menus import display_main_menu
from installer import install_app, list_installable_apps
import os

console = Console()

def print_header():
    header_text = "[bold cyan]🌐 Atlanti Server Management[/bold cyan]\n" \
                  "[bold magenta]Need server administration? Visit [link=https://atlanti.io]https://atlanti.io[/link][/bold magenta]"
    console.print(Panel(header_text, expand=False, style="bold magenta"))

def list_apps():
    apps = list_installable_apps()

    table = Table()
    table.add_column("Application")
    table.add_column("Status", style="green")

    for idx, (file, title) in enumerate(apps, start=1):
        status = Text("Installed", style="green") if title.startswith("✓") else Text("Not installed", style="red")
        app_name = title[1:].strip() if title.startswith("✓") else title
        table.add_row(app_name, status)

    console.print(table)

def show_help():
    """Muestra una tabla con los comandos disponibles y su descripción."""
    table = Table()
    table.add_column("Command", style="cyan", justify="left")
    table.add_column("Description", style="magenta", justify="left")

    commands = [
        ("apps list", "List all available applications."),
        ("apps install <app_name>", "Install a specified application (e.g., 'docker')."),
        ("help", "Show this help message."),
    ]

    for command, description in commands:
        table.add_row(command, description)

    console.print(table)

def main():
    print_header()

    parser = argparse.ArgumentParser(description="Atlanti Server Management CLI")
    subparsers = parser.add_subparsers(dest="command")

    # Subcomando 'apps'
    apps_parser = subparsers.add_parser("apps", help="Manage applications")
    apps_subparsers = apps_parser.add_subparsers(dest="action")

    # Subcomando 'install' dentro de 'apps'
    install_parser = apps_subparsers.add_parser("install", help="Install an app")
    install_parser.add_argument("app_name", type=str, help="Name of the app to install (e.g., 'docker')")

    # Subcomando 'list' dentro de 'apps'
    apps_subparsers.add_parser("list", help="List all available apps")

    # Comando 'help'
    help_parser = subparsers.add_parser("help", help="Show help")

    args = parser.parse_args()

    try:
        if args.command == "apps":
            if args.action == "install":
                app_name = args.app_name.lower()
                app_files = list_installable_apps()
                app_file = next((file[0] for file in app_files if os.path.basename(file[0]).startswith(app_name)), None)

                if app_file:
                    install_app(app_file)
                else:
                    console.print(
                        Panel(f"⚠️ Application '{app_name}' not found. Please check the available apps.",
                              style="bold red"))
            elif args.action == "list":
                list_apps()
        elif args.command == "help":
            show_help()
        else:
            display_main_menu()

    except KeyboardInterrupt:
        console.print("\n👋 [bold red]Exiting Atlanti Server Management. See you soon![/bold red]")
        exit()

if __name__ == "__main__":
    main()
