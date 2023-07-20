# Gateway Switch Utility

The Gateway Switch Utility is a Python script that helps manage default gateways on Linux systems. It allows you to switch between two default gateways with reversed priorities.

## How It Works

The utility uses the `ip` command-line tool to retrieve the current default gateways and their associated network interfaces. It then deletes the existing default routes and adds new default routes with reversed priorities.

## Usage

1. Clone the repository:

   ```shell
   git clone https://github.com/your-username/gateway-switch-utility.git
   ```

2. Change into the project directory:

   ```shell
   cd gateway-switch-utility
   ```

3. Run the script:

   ```shell
   python3 gateway_switch.py
   ```

   **Note:** The script requires root privileges to modify the network routes. You may be prompted to enter your password.

4. The script will display the found gateways and their associated network interfaces. It will then delete the existing default routes and add new default routes with reversed priorities.

## Generated with ChatCraft

This utility was generated with ChatCraft, a web-based, expert programming AI assistant. ChatCraft helps programmers learn, experiment, and be more creative with code. It provides assistance and generates code snippets based on user queries.

To learn more about ChatCraft, visit the [ChatCraft GitHub repository](https://github.com/chatcraft-team/chatcraft).
