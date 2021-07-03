from BnBNode import Node
from utility import reduce_matrix as reduce, euclidean_distance

class Graph:
    # constructor
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

    # Approximate TSP solution using BnB
    def BranchAndBound(self) -> tuple:
        key = lambda node : node.cost

        mat, cost = reduce(self.adj_matrix)
        priority_queue = [Node(self.first_city_name, mat, cost, [self.first_city_name])]
        best_so_far = -1
        best_path_so_far = []

        while len(priority_queue) > 0:
            first = priority_queue.pop(0)
            # print(first)

            # we have reached our solution
            if len(first.path) == self.N:
                if(best_so_far == -1):
                    best_so_far = first.cost
                    best_path_so_far = first.path
                else:
                    if(first.cost < best_so_far):
                        best_so_far = first.cost
                        best_path_so_far = first.path

            R = first.city
            A = first.adj_matrix
            i = self.city_list.index(R)
            first_city_idx = self.city_list.index(self.first_city_name)

            # iterate to all adjacent cities
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
        
        return best_path_so_far, best_so_far