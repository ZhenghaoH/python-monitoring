import random
import networkx as nx
import matplotlib.pyplot as plt

class Node:
    def __init__(self, node_type, id):
        self.node_type = node_type
        self.id = id

    def __str__(self):
        return f"{self.node_type}{self.id}"

class Link:
    def __init__(self, node1, node2):
        self.node1 = node1
        self.node2 = node2

    def __str__(self):
        return f"{self.node1} <-> {self.node2}"

class NetworkTopology:
    def __init__(self, num_hosts, num_servers, num_switches):
        self.num_hosts = num_hosts
        self.num_servers = num_servers
        self.num_switches = num_switches
        self.hosts = [Node("h", i) for i in range(1, num_hosts + 1)]
        self.servers = [Node("server", i) for i in range(1, num_servers + 1)]
        self.access_switches = [Node("as", i) for i in range(1, num_hosts + num_servers + 1)]
        self.core_switches = [Node("cs", i) for i in range(1, num_switches - (num_hosts + num_servers) + 1)]
        self.links = []

        self.create_topology()

    def create_topology(self):
        # Ensure hosts and servers connect to different access switches
        available_access_switches = self.access_switches.copy()

        for host in self.hosts:
            access_switch = available_access_switches.pop(0)
            self.links.append(Link(host, access_switch))

        for server in self.servers:
            access_switch = available_access_switches.pop(0)
            self.links.append(Link(server, access_switch))

        # Connect access switches to core switches
        for access_switch in self.access_switches:
            core_switch = random.choice(self.core_switches)
            self.links.append(Link(access_switch, core_switch))

        # Ensure every core switch is connected to every other core switch
        for i in range(len(self.core_switches)):
            for j in range(i + 1, len(self.core_switches)):
                self.links.append(Link(self.core_switches[i], self.core_switches[j]))

    def draw_topology(self, filename="network_topology.png"):
        G = nx.Graph()

        color_map = []
        legend_elements = []

        for node in self.hosts:
            G.add_node(str(node), label=str(node))
            color_map.append("skyblue")
        
        for node in self.servers:
            G.add_node(str(node), label=str(node))
            color_map.append("darkgoldenrod")
        
        for node in self.access_switches:
            G.add_node(str(node), label=str(node))
            color_map.append("lightcoral")
        
        for node in self.core_switches:
            G.add_node(str(node), label=str(node))
            color_map.append("lightcoral")
        
        for link in self.links:
            G.add_edge(str(link.node1), str(link.node2))
        
        pos = nx.spring_layout(G)
        plt.figure(figsize=(12, 8))
        nx.draw(G, pos, with_labels=True, node_size=600, node_color=color_map, font_size=10, font_weight="bold", edge_color="gray")
        
        # Create legend
        legend_elements = [
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='skyblue', markersize=10, label='Hosts'),
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='darkgoldenrod', markersize=10, label='Servers'),
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='lightcoral', markersize=10, label='Switches')
        ]
        plt.legend(handles=legend_elements, loc='upper right')
        
        plt.title("Network Topology")
        plt.savefig(filename)
        plt.show()

    def __str__(self):
        topology = "Nodes:\n"
        for node in self.hosts + self.servers + self.access_switches + self.core_switches:
            topology += str(node) + "\n"

        topology += "Links:\n"
        for link in self.links:
            topology += str(link) + "\n"

        return topology


