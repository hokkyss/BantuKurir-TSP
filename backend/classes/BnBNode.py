class Node:
    # constructor
    def __init__(self, city: str, adj_matrix: list, cost: float, path: list):
        self.city = city
        self.adj_matrix = adj_matrix
        self.cost = cost
        self.path = path
    
    # toString
    def __str__(self) -> str:
        from_matrix = ""
        for row in self.adj_matrix:
            from_matrix = from_matrix.__add__(str(row) + "\n")
        return from_matrix + str(self.cost) + "\n" + str(self.path) + "\n"