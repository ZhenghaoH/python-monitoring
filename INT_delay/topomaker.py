import json

def generate_topology(num_hosts, num_switches):
    data = {
        "hosts": {},
        "switches": {},
        "links": []
    }

    # Generate hosts
    for i in range(1, num_hosts + 1):
        host_name = f"h{i}"
        data["hosts"][host_name] = {
            "ip": f"fc00::{i}",
            "mac": f"08:00:00:00:{i:02d}:{i:02d}",
            "commands": [
                f"route add default gw fc00::{i*10} dev eth0",
                f"arp -i eth0 -s fc00::{i*10} 08:00:00:00:{i:02d}:00"
            ]
        }
    
    # Generate switches
    for i in range(1, num_switches + 1):
        switch_name = f"s{i}"
        data["switches"][switch_name] = {
            "runtime_json": f"topo/{switch_name}-runtime.json"
        }
    # Track switch ports
    switch_ports = {f"s{i}": 1 for i in range(1, num_switches + 1)}

    # Generate links between hosts and switches
    for i in range(1, num_hosts + 1):
        host_name = f"h{i}"
        switch_index = (i % num_switches) + 1
        switch_name = f"s{switch_index}"
        port = switch_ports[switch_name]
        data["links"].append([host_name, f"{switch_name}-p{port}"])
        switch_ports[switch_name] += 1
    
    # Generate links between switches in a linear topology
    for i in range(1, num_switches):
        switch1 = f"s{i}"
        switch2 = f"s{i+1}"
        port1 = switch_ports[switch1]
        port2 = switch_ports[switch2]
        data["links"].append([f"{switch1}-p{port1}", f"{switch2}-p{port2}"])
        switch_ports[switch1] += 1
        switch_ports[switch2] += 1

    return data



def save_topology_to_json(topology, filename):
    with open(filename, 'w') as f:
        json.dump(topology, f, indent=4)

def generate_switch(num_switches):
    for i in range(1, num_switches + 1):
        switch_name = f"s{i}"
        filename = f"./topo/{switch_name}-runtime.json"
        switch_runtime = {
            "target": "bmv2",
            "p4info": "build/INT.p4.p4info.txt",
            "bmv2_json": "build/INT.json",
            "table_entries": [
            ]
        }
        with open(filename, 'w') as f:
            json.dump(switch_runtime, f, indent=4)

if __name__ == '__main__':
    num_hosts = 12  # 可以根据需求修改
    num_switches = 18  # 可以根据需求修改

    topology = generate_topology(num_hosts, num_switches)
    generate_switch(num_switches)
    save_topology_to_json(topology, './topo/topology.json')