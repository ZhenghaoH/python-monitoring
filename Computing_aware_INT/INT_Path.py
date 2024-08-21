class INT_Path:
    def __init__(self, network_topology):
        self.network_topology = network_topology
        self.nodes = self.network_topology.hosts + self.network_topology.servers + self.network_topology.access_switches + self.network_topology.core_switches
        self.node_index = {str(node): idx for idx, node in enumerate(self.nodes)}
        self.adj_matrix = self.create_adjacency_matrix()

    def create_adjacency_matrix(self):
        size = len(self.nodes)
        adj_matrix = [[0] * size for _ in range(size)]

        for link in self.network_topology.links:
            i, j = self.node_index[str(link.node1)], self.node_index[str(link.node2)]
            adj_matrix[i][j] = adj_matrix[j][i] = 1

        return adj_matrix

    def bfs_shortest_path(self, start_index, end_index):
        queue = [(start_index, [start_index])]
        visited = set()

        while queue:
            current, path = queue.pop(0)
            if current in visited:
                continue

            visited.add(current)
            if current == end_index:
                return path

            for neighbor, connected in enumerate(self.adj_matrix[current]):
                if connected and neighbor not in visited:
                    queue.append((neighbor, path + [neighbor]))

        return None

    def generate_path(self, start_host, end_server):
        start_switch = None
        end_switch = None

        for link in self.network_topology.links:
            if str(link.node1) == start_host:
                start_switch = str(link.node2)
            if str(link.node1) == end_server:
                end_switch = str(link.node2)

        if start_switch and end_switch:
            start_index = self.node_index[start_switch]
            end_index = self.node_index[end_switch]
            path_indices = self.bfs_shortest_path(start_index, end_index)

            if path_indices is None:
                return "No path found between the specified nodes."

            path_nodes = [str(self.nodes[idx]) for idx in path_indices]
            return path_nodes
        else:
            return "Start host or end server not found in the network."
