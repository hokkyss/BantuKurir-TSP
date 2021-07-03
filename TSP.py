def reduce(adj_matrix) -> tuple:
    result = [(row.copy()) for row in adj_matrix]
    cost = 0
    N = len(result)

    # iterate row
    for i in range(N):
        subtractor = -1
        for j in range(N):
            if (result[i][j] == -1):
                continue
            if(subtractor == -1):
                subtractor = result[i][j]
                continue
            subtractor = min(subtractor, result[i][j])
        
        if(subtractor == -1):
            continue

        cost += subtractor
        for j in range(N):
            if(result[i][j] == -1): continue

            result[i][j] -= subtractor

    # iterate column
    for j in range(N):
        subtractor = -1
        for i in range(N):
            if(result[i][j] == -1): 
                continue
            if subtractor == -1:
                subtractor = result[i][j]
                continue                    
            subtractor = min(result[i][j], subtractor)
        
        if(subtractor == -1):
            continue

        cost += subtractor
        for i in range(N):
            if(result[i][j] == -1): continue
            result[i][j] -= subtractor

    return (result, cost)

class Node:
    def __init__(self, city: str, adj_matrix: list, cost: int, path: list):
        self.city = city
        self.adj_matrix = adj_matrix
        self.cost = cost
        self.path = path
    
    def __str__(self) -> str:
        from_matrix = ""
        for row in self.adj_matrix:
            from_matrix = from_matrix.__add__(str(row) + "\n")
        return from_matrix + str(self.cost) + "\n" + str(self.path) + "\n"

class Graph:
    def __init__(self, first_city_name: str, adj_matrix: list, city_list: list):
        self.adj_matrix = adj_matrix
        self.city_list = city_list
        self.first_city_name = first_city_name
        self.N = len(adj_matrix)

    @staticmethod
    def parse_file(file_stream):
        blob = file_stream.stream.read()

        print(blob)

        if blob == None:
            return []

        text = blob.decode("UTF8")
        print(text)
        pass

    def BranchAndBound(self) -> tuple:
        key = lambda node : node.cost

        mat, cost = reduce(self.adj_matrix)

        priority_queue:list = [Node(self.first_city_name, mat, cost, [self.first_city_name])]

        while len(priority_queue) > 0:
            first = priority_queue.pop(0)
            print(first)

            if len(first.path) == self.N:
                return (first.path, first.cost)

            R = first.city
            A = first.adj_matrix
            i = self.city_list.index(R)
            first_city_idx = self.city_list.index(self.first_city_name)

            for j in range(self.N):
                S = self.city_list[j]

                if(A[i][j] == -1):
                    continue

                B = [row.copy() for row in A]
                B[j][first_city_idx] = -1

                for col in range(self.N):
                    B[i][col] = -1
                for row in range(self.N):
                    B[row][j] = -1
                
                new_path = first.path.copy()
                new_path.append(S)

                B, cost = reduce(B)
                priority_queue.append(Node(S, B, first.cost + cost + A[i][j], new_path))

            priority_queue.sort(key=key)