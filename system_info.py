import time
import psutil
import platform
import requests
import concurrent.futures
from rich.console import Console
from rich.live import Live
from rich.table import Table
from utils import create_block_bar
from rich.layout import Layout
from rich.panel import Panel

console = Console()


def fetch_public_ip():
    """Solicita la IP pública de forma asíncrona."""
    try:
        response = requests.get("https://api.ipify.org?format=text", timeout=5)
        return response.text if response.status_code == 200 else "Unavailable"
    except requests.RequestException:
        return "Unavailable"


def render_system_info():
    """Renderiza la tabla de métricas del sistema (CPU, Memoria, etc.)."""
    table = Table(title="System Stats", expand=True, show_header=False, box=None)

    cpu_usage = psutil.cpu_percent(interval=0.1)
    cpu_bar = create_block_bar(cpu_usage, color="blue", empty_color="grey37")
    table.add_row("CPU Usage (Total)", f"{cpu_usage}%", cpu_bar)

    memory = psutil.virtual_memory()
    memory_usage = f"{memory.percent}% ({memory.used // (1024 ** 2)} MB / {memory.total // (1024 ** 2)} MB)"
    mem_bar = create_block_bar(memory.percent, color="green", empty_color="grey37")
    table.add_row("Memory Usage", memory_usage, mem_bar)

    disk = psutil.disk_usage('/')
    disk_usage = f"{disk.percent}% ({disk.used // (1024 ** 3)} GB / {disk.total // (1024 ** 3)} GB)"
    disk_bar = create_block_bar(disk.percent, color="yellow", empty_color="grey37")
    table.add_row("Disk Usage", disk_usage, disk_bar)

    swap = psutil.swap_memory()
    swap_usage = f"{swap.percent}% ({swap.used // (1024 ** 2)} MB / {swap.total // (1024 ** 2)} MB)"
    swap_bar = create_block_bar(swap.percent, color="purple", empty_color="grey37")
    table.add_row("Swap Usage", swap_usage, swap_bar)

    net_io = psutil.net_io_counters()
    network_info = f"Sent: {net_io.bytes_sent // (1024 ** 2)} MB, Received: {net_io.bytes_recv // (1024 ** 2)} MB"
    table.add_row("Network IO", network_info)

    return table


def render_system_details(public_ip):
    """Renderiza la tabla de detalles adicionales del sistema, incluyendo la IP pública."""
    details = Table(title="System Details", expand=True, show_header=False, box=None)

    cpu_family = platform.processor() or "Unknown"
    details.add_row("CPU Family", cpu_family)

    os_name = platform.system()
    os_version = platform.release()
    details.add_row("OS", f"{os_name} {os_version}")

    details.add_row("Public IP", public_ip)

    for _ in range(5 - len(details.rows)):
        details.add_row("", "")

    return details


def system_info_panel():
    console.clear()

    with concurrent.futures.ThreadPoolExecutor() as executor:
        ip_future = executor.submit(fetch_public_ip)

        with Live(console=console, refresh_per_second=1) as live:
            public_ip = "Fetching..."  # Mensaje de carga inicial
            try:
                while True:
                    if ip_future.done() and public_ip == "Fetching...":
                        public_ip = ip_future.result()

                    layout = Layout()
                    layout.split_row(
                        Layout(render_system_info(), name="left", ratio=1),
                        Layout(render_system_details(public_ip), name="right", ratio=1)
                    )

                    wrapped_layout = Panel(
                        layout,
                        title="Atlanti.io - System Information",
                        title_align="left",
                        border_style="cyan"
                    )

                    live.update(wrapped_layout)
                    time.sleep(1)
            except KeyboardInterrupt:
                console.clear()
                console.print(Panel("Returning to the main menu...", style="bold yellow"))
