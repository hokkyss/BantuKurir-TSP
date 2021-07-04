def reduce_matrix(adj_matrix) -> tuple:
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
