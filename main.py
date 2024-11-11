import argparse
from menus import display_main_menu
from installer import install_app, list_installable_apps
import os
from rich.console import Console
from rich.panel import Panel

console = Console()


def print_header():
    header_text = "[bold cyan]🌐 Atlanti Server Management[/bold cyan]\n" \
                  "[bold magenta]Need server administration? Visit [link=https://atlanti.io]https://atlanti.io[/link][/bold magenta]"
    console.print(Panel(header_text, expand=False, style="bold magenta"))


def main():
    # Imprimir el encabezado al inicio
    print_header()

    parser = argparse.ArgumentParser(description="Atlanti Server Management CLI")
    subparsers = parser.add_subparsers(dest="command")

    # Subcomando 'apps'
    apps_parser = subparsers.add_parser("apps", help="Manage applications")
    apps_subparsers = apps_parser.add_subparsers(dest="action")

    # Subcomando 'install' dentro de 'apps'
    install_parser = apps_subparsers.add_parser("install", help="Install an app")
    install_parser.add_argument("app_name", type=str, help="Name of the app to install (e.g., 'docker')")

    args = parser.parse_args()

    # Verificar los subcomandos
    if args.command == "apps" and args.action == "install":
        app_name = args.app_name.lower()
        app_files = list_installable_apps()
        app_file = next((file[0] for file in app_files if os.path.basename(file[0]).startswith(app_name)), None)

        if app_file:
            install_app(app_file)
        else:
            console.print(
                Panel(f"⚠️ Application '{app_name}' not found. Please check the available apps.", style="bold red"))
    else:
        try:
            display_main_menu()
        except KeyboardInterrupt:
            console.print("\n👋 [bold red]Exiting Atlanti Server Management. See you soon![/bold red]")
            exit()


if __name__ == "__main__":
    main()
