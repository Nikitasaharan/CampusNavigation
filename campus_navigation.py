# Building Data ADT with BST/AVL

class BuildingNode:
    def __init__(self, building_id, name, location):
        self.building_id = building_id
        self.name = name
        self.location = location
        self.left = None
        self.right = None
        self.height = 1  # For AVL tree


class AVLTree:
    def insert(self, root, node):
        if not root:
            return node
        if node.building_id < root.building_id:
            root.left = self.insert(root.left, node)
        else:
            root.right = self.insert(root.right, node)

        # Update height
        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))

        # Balance factor
        balance = self.get_balance(root)

        # Left heavy
        if balance > 1 and node.building_id < root.left.building_id:
            return self.right_rotate(root)
        if balance < -1 and node.building_id > root.right.building_id:
            return self.left_rotate(root)
        if balance > 1 and node.building_id > root.left.building_id:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)
        if balance < -1 and node.building_id < root.right.building_id:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)

        return root

    def left_rotate(self, z):
        y = z.right
        T2 = y.left
        y.left = z
        z.right = T2
        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        return y

    def right_rotate(self, z):
        y = z.left
        T3 = y.right
        y.right = z
        z.left = T3
        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        return y

    def get_height(self, root):
        if not root:
            return 0
        return root.height

    def get_balance(self, root):
        if not root:
            return 0
        return self.get_height(root.left) - self.get_height(root.right)

    def inorder(self, root):
        if root:
            self.inorder(root.left)
            print(f"Building ID: {root.building_id}, Name: {root.name}, Location: {root.location}")
            self.inorder(root.right)



# Graph for Campus Navigation


import heapq


class Graph:
    def __init__(self, vertices):
        self.V = vertices
        self.graph = [[] for _ in range(vertices)]

    def add_edge(self, u, v, w):
        self.graph[u].append((v, w))
        self.graph[v].append((u, w))  # Assuming undirected graph

    def dijkstra(self, start):
        dist = [float('inf')] * self.V
        dist[start] = 0
        pq = [(0, start)]
        while pq:
            d, node = heapq.heappop(pq)
            if d > dist[node]:
                continue
            for neighbor, weight in self.graph[node]:
                if dist[node] + weight < dist[neighbor]:
                    dist[neighbor] = dist[node] + weight
                    heapq.heappush(pq, (dist[neighbor], neighbor))
        return dist

    # Kruskal's MST
    def kruskal(self):
        parent = [i for i in range(self.V)]

        def find(u):
            while parent[u] != u:
                parent[u] = parent[parent[u]]
                u = parent[u]
            return u

        def union(u, v):
            pu, pv = find(u), find(v)
            parent[pu] = pv

        edges = []
        for u in range(self.V):
            for v, w in self.graph[u]:
                if u < v:
                    edges.append((w, u, v))
        edges.sort()
        mst = []
        for w, u, v in edges:
            if find(u) != find(v):
                union(u, v)
                mst.append((u, v, w))
        return mst


# Expression Tree for Calculations

class ExprNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


def evaluate_expression_tree(node):
    if node.left is None and node.right is None:
        return float(node.value)
    left_val = evaluate_expression_tree(node.left)
    right_val = evaluate_expression_tree(node.right)
    if node.value == '+':
        return left_val + right_val
    elif node.value == '-':
        return left_val - right_val
    elif node.value == '*':
        return left_val * right_val
    elif node.value == '/':
        return left_val / right_val

# Example Usage


if __name__ == "__main__":
    # AVL Tree Example
    avl = AVLTree()
    root = None
    root = avl.insert(root, BuildingNode(1, "Library", "North Wing"))
    root = avl.insert(root, BuildingNode(2, "Cafeteria", "South Wing"))
    root = avl.insert(root, BuildingNode(3, "Lab Block", "East Wing"))
    print("Campus Buildings (Inorder Traversal):")
    avl.inorder(root)

    # Graph Example
    g = Graph(4)
    g.add_edge(0, 1, 5)
    g.add_edge(0, 2, 10)
    g.add_edge(1, 2, 3)
    g.add_edge(2, 3, 1)
    print("\nShortest distances from node 0:", g.dijkstra(0))
    print("Minimum Spanning Tree:", g.kruskal())

    # Expression Tree Example
    root_expr = ExprNode('+')
    root_expr.left = ExprNode('3')
    root_expr.right = ExprNode('*')
    root_expr.right.left = ExprNode('2')
    root_expr.right.right = ExprNode('4')
    print("\nExpression Tree Evaluation Result:", evaluate_expression_tree(root_expr))
