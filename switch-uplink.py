#!/usr/bin/env python3
import subprocess
import sys
import json

def get_default_gateway(interface):
    result = subprocess.run(['ip', '-j', 'route', 'show', 'dev', interface],
                            capture_output=True, text=True)
    routes = json.loads(result.stdout)
    for route in routes:
        if 'default' in route['dst']:
            return route['gateway']

def modify_route(action, gateway, interface, metric=None):
    command = ['sudo', 'ip', 'route', action, 'default', 'via', gateway, 'dev',
               interface]
    if metric:
        command.extend(['metric', str(metric)])
    subprocess.run(command)

def switch_route(interface1, interface2):
    gateway1 = get_default_gateway(interface1)
    gateway2 = get_default_gateway(interface2)

    # Delete the current default routes
    modify_route('del', gateway1, interface1)
    modify_route('del', gateway2, interface2)

    # Add the new default routes with appropriate metrics
    modify_route('add', gateway1, interface1, 100)
    modify_route('add', gateway2, interface2, 101)

if len(sys.argv) != 3:
    print("Usage: python3 switch_route.py <interface1> <interface2>")
else:
    switch_route(sys.argv[1], sys.argv[2])