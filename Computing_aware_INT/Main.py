import topomaker, INT_Path 
# 示例用法
num_hosts = 10
num_servers = 5
num_switches = 20

network_topology = topomaker.NetworkTopology(num_hosts, num_servers, num_switches)
Path_generator = INT_Path.INT_Path(network_topology)
print(Path_generator.adj_matrix)
print(Path_generator.generate_path("h1", "server1"))
# network_topology.draw_topology("network_topology.png")