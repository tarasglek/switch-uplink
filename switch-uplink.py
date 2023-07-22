#!/usr/bin/env python3
import subprocess
import json
import logging

logging.basicConfig(level=logging.INFO)

def get_default_gateways():
    result = subprocess.run(['ip', '-j', 'route'], capture_output=True, text=True)
    routes = json.loads(result.stdout)
    default_routes = [route for route in routes if 'default' in route['dst']]

    gateways = [(route['dev'], route['gateway']) for route in default_routes]

    for i, (interface, gateway) in enumerate(gateways):
        result = subprocess.run(['ip', '-j', '--brief', 'addr', 'show', interface], capture_output=True, text=True)
        interface_info = json.loads(result.stdout)
        ip = None
        for info in interface_info:
            for addr_info in info['addr_info']:
                if 'local' in addr_info:
                    ip = addr_info['local']
                    break
            if ip:
                break
        gateways[i] = (interface, gateway, ip)
    return gateways

def modify_route(action, gateway, interface, metric=None):
    command = ['sudo', 'ip', 'route', action, 'default', 'via', gateway, 'dev',
               interface]
    if metric:
        command.extend(['metric', str(metric)])
    subprocess.run(command)

def switch_route():
    gateways = get_default_gateways()
    if len(gateways) != 2:
        logging.error(f"Expected exactly two default gateways, but found {len(gateways)}. Gateways: {gateways}")
        return

    logging.info(f"Found gateways: {gateways}")

    # Delete the current default routes
    for interface, gateway, ip in gateways:
        logging.info(f"Deleting default route via {gateway} on {interface} with IP {ip}")
        modify_route('del', gateway, interface)

    # Add the new default routes with reversed priorities
    primary_interface, primary_gateway, primary_ip = gateways[1]
    backup_interface, backup_gateway, backup_ip = gateways[0]

    logging.info(f"Adding primary({primary_interface}) route via {primary_gateway} with IP {primary_ip} and metric 100")
    modify_route('add', primary_gateway, primary_interface, 100)
    logging.info(f"Adding backup({backup_interface}) route via {backup_gateway} with IP {backup_ip} and metric 101")
    modify_route('add', backup_gateway, backup_interface, 101)

if __name__ == "__main__":
    switch_route()