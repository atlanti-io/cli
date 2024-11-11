import cutie
from rich.console import Console
from rich.panel import Panel
from installer import list_installable_apps, install_app, load_yaml
from system_info import system_info_panel
from ticket import open_ticket

console = Console()

def display_main_menu():
    main_menu_options = [
        "Install Apps/Services",
        "View System Information",
        "Request Server Support",
        "Exit"
    ]

    while True:
        console.clear()
        header_text = "[bold cyan]🌐 Atlanti Server Management[/bold cyan]\n" \
                      "[bold magenta]Need server administration? Visit [link=https://atlanti.io]https://atlanti.io[/link][/bold magenta]"

        console.clear()
        console.print(Panel(header_text, expand=False, style="bold magenta"))
        selected_option = cutie.select(main_menu_options)

        if main_menu_options[selected_option] == "Install Apps/Services":
            display_install_menu()
        elif main_menu_options[selected_option] == "View System Information":
            system_info_panel()
        elif main_menu_options[selected_option] == "Request Server Support":
            open_ticket()
        elif main_menu_options[selected_option] == "Exit":
            console.print("\n👋 [bold red]Exiting Atlanti Server Management. See you soon![/bold red]")
            break


def display_install_menu():
    """Displays a menu of installable apps based on YAML configurations with an installed status."""
    yaml_files_with_status = list_installable_apps()

    install_menu_options = [title for _, title in yaml_files_with_status]
    install_menu_options.append("Back to Main Menu")

    while True:
        try:
            console.clear()
            console.print(Panel("Installable Apps/Services\nSelect an app to install or manage.", expand=False, style="cyan"))

            selected_option = cutie.select(install_menu_options)

            if install_menu_options[selected_option] == "Back to Main Menu":
                break
            else:
                yaml_file = yaml_files_with_status[selected_option][0]
                install_app(yaml_file)
                display_install_menu()  # Recargar el menú para reflejar el estado actualizado
                break

        except KeyboardInterrupt:
            console.print("\n⚠️ [yellow]Returning to the main menu...[/yellow]\n")
            break