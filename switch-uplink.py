#!/usr/bin/env python3
import subprocess
import json
import logging

logging.basicConfig(level=logging.INFO)

def get_default_gateways():
    result = subprocess.run(['ip', '-j', 'route'], capture_output=True, text=True)
    routes = json.loads(result.stdout)
    default_routes = [route for route in routes if 'default' in route['dst']]
    return [(route['dev'], route['gateway']) for route in default_routes]

def modify_route(action, gateway, interface, metric=None):
    command = ['sudo', 'ip', 'route', action, 'default', 'via', gateway, 'dev',
               interface]
    if metric:
        command.extend(['metric', str(metric)])
    subprocess.run(command)

def switch_route():
    gateways = get_default_gateways()
    if len(gateways) != 2:
        logging.error("Expected exactly two default gateways.")
        return

    logging.info(f"Found gateways: {gateways}")

    # Delete the current default routes
    for interface, gateway in gateways:
        logging.info(f"Deleting default route via {gateway} on {interface}")
        modify_route('del', gateway, interface)

    # Add the new default routes with reversed priorities
    logging.info(f"Adding default route via {gateways[1][1]} on {gateways[1][0]} with metric 100")
    modify_route('add', gateways[1][1], gateways[1][0], 100)
    logging.info(f"Adding default route via {gateways[0][1]} on {gateways[0][0]} with metric 101")
    modify_route('add', gateways[0][1], gateways[0][0], 101)

if __name__ == "__main__":
    switch_route()