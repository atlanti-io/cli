import subprocess
import yaml
from rich.console import Console
from rich.panel import Panel
from rich.live import Live
import os
import tempfile

console = Console()

GREEN_CHECK = "\033[92m✓\033[0m"


def load_yaml(file_path):
    """Loads YAML file content."""
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)


def is_installed(check_command):
    """Verifica si una aplicación está instalada ejecutando el comando de verificación."""
    try:
        result = subprocess.run(check_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.returncode == 0
    except Exception:
        return False


def install_app(yaml_file):
    """Installs an app based on the YAML configuration."""
    app_config = load_yaml(yaml_file)
    title = app_config.get("title", "Unknown App")
    description = app_config.get("description", "")
    commands = app_config.get("commands", [])
    check_command = app_config.get("check_command", "")

    if check_command and is_installed(check_command):
        console.print(f"✓ {title} is already installed.", style="green")
        console.input("\nPress Enter to continue.")
        return

    console.clear()
    install_panel = Panel(f"Installing {title}\n\n{description}", style="yellow", expand=False)
    console.print(install_panel)

    with tempfile.TemporaryDirectory() as temp_dir:
        console.print(f"Using temporary directory: {temp_dir}", style="dim")

        with Live(console=console, refresh_per_second=4) as live:
            for command in commands:
                live.update(Panel(f"[yellow]Running:[/yellow] {command}\n\n", expand=False))
                process = subprocess.Popen(command, shell=True, cwd=temp_dir, stdout=subprocess.PIPE,
                                           stderr=subprocess.STDOUT)

                output_lines = []
                for line in iter(process.stdout.readline, b''):
                    line_text = line.decode('utf-8').strip()
                    output_lines.append(line_text)
                    output_lines = output_lines[-10:]
                    live.update(Panel("\n".join(output_lines), title="Output (last 10 lines)", expand=True))

                process.stdout.close()
                process.wait()

                if process.returncode != 0:
                    console.print(f"❌ Command failed: {command}", style="red")
                    console.input("\nPress Enter to continue.")
                    return

            live.update(
                Panel(f"{GREEN_CHECK} {title} installed successfully.\n\nPress Enter to continue.", style="green",
                      expand=False))
            console.input()


def list_installable_apps():
    """Lists all YAML files in the 'apps' directory and checks their installation status."""
    apps_dir = os.path.join(os.path.dirname(__file__), "apps")
    yaml_files = [os.path.join(apps_dir, file) for file in os.listdir(apps_dir) if file.endswith('.yaml')]

    apps_with_status = []
    for file in yaml_files:
        app_config = load_yaml(file)
        title = app_config.get("title", "Unknown App")
        check_command = app_config.get("check_command", "")

        if check_command and is_installed(check_command):
            title = f"{GREEN_CHECK} {title}"

        apps_with_status.append((file, title))

    return apps_with_status


def main_menu():
    """Main menu for selecting apps to install."""
    while True:
        console.print("\n[bold]Available Applications to Install:[/bold]\n")
        apps = list_installable_apps()

        for idx, (_, title) in enumerate(apps, start=1):
            console.print(f"[{idx}] {title}")

        console.print("\n[0] Exit")

        try:
            choice = int(console.input("\nSelect an option: "))
            if choice == 0:
                break

            if 1 <= choice <= len(apps):
                yaml_file, _ = apps[choice - 1]
                install_app(yaml_file)

        except ValueError:
            console.print("[red]Invalid input. Please enter a number.[/red]")
        except KeyboardInterrupt:
            console.print("\n[red]Exiting...[/red]")
            break


if __name__ == "__main__":
    main_menu()
