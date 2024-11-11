# Atlanti Server Management

[Atlanti Server Management](https://atlanti.io) is a CLI tool designed to simplify server setup on Ubuntu, supporting both ARM and x64 architectures. This tool lets you quickly install essential applications on a new server, streamlining the configuration process.

![Atlanti Server Management Demo](https://raw.githubusercontent.com/atlanti-io/cli/refs/heads/main/docs/atlanticli-install.gif)

### Installation

To install **Atlanti Server Management** on your server

```bash
wget -qO atlanti get.atlanti.io && sudo bash atlanti
```


### Key Features

With **Atlanti Server Management**, you can easily install and manage popular applications commonly used on servers, including:

- PHP
- Redis
- Node.js
- Python
- Fail2ban
- Nginx
- UFW (Uncomplicated Firewall)
- Docker
- PostgreSQL
- Certbot
- MySQL

### Usage

#### 1. Interactive CLI

Run `atlanti` in your terminal, then select **Install apps/services** to browse and install applications interactively.

#### 2. Direct Commands

Use these commands for quick, direct access:

- **List available applications:** `atlanti apps list`
- **Install an application:** `atlanti apps install <app_name>`

### Server Support

If you encounter any issues with your server, open a support ticket directly from the CLI by running `atlanti` and selecting the option **Request server support**. This service is available to everyone, regardless of your customer status, and connects you directly to our expert support team for assistance.

![Atlanti Server Management Demo Ticket](https://raw.githubusercontent.com/atlanti-io/cli/refs/heads/main/docs/atlanticli-ticket.gif)

### Contributing

If you’d like to see additional applications included, feel free to open a pull request! We welcome contributions that help make Atlanti Server Management more versatile and user-friendly.

---

### About Us

We are a team of server management experts at [Atlanti](https://atlanti.io). With **Atlanti Server Management**, you’ll experience effective solutions designed by sysadmins, for sysadmins. We understand the tools and features sysadmins value most, and we’ve made them easy to access through our CLI.

---