
def evr_cyc(positions, matrix, min_dis, max_dis):
    import numpy as np
    import math
    
    bin_num = positions.shape[0]
    
    trans_matrix = np.zeros((bin_num, 3), np.float)

    f_value = 0.0
    for i in range(bin_num):
        pos_i = positions[i]

        divec = np.array([0.0, 0.0, 0.0], dtype = np.float)
        ervec = np.array([0.0, 0.0, 0.0], dtype = np.float)

        for j in range(bin_num):
            if j == i:
                continue
            pos_j = positions[j]

            divec = pos_j - pos_i

            mod = math.sqrt(divec[0] ** 2 + divec[1] ** 2 + divec[2] ** 2)
            dis = matrix[i, j]

            if dis == 0 or mod == 0:
                continue

            divec = divec / mod

            if i == (j + 1) % bin_num or i == (j - 1) % bin_num:
                if mod > max_dis:
                    err = mod - max_dis
                elif mod < min_dis:
                    err = mod - min_dis
                else:
                    err = 0.0
            else:
                err = mod - dis
            
            divec = divec * err
            ervec = ervec + divec
        
        ervec /= (bin_num * 2)
        trans_matrix[i] += ervec

    for vec in trans_matrix:
        f_value += math.sqrt(vec[0] ** 2 + vec[1] ** 2 + vec[2] ** 2)
    
    return trans_matrix, f_value


def evr_lin(positions, matrix, min_dis, max_dis):
    import numpy as np
    import math
    
    bin_num = positions.shape[0]
    
    trans_matrix = np.zeros((bin_num, 3), np.float)

    f_value = 0.0
    for i in range(bin_num):
        pos_i = positions[i]

        divec = np.array([0.0, 0.0, 0.0], dtype = np.float)
        ervec = np.array([0.0, 0.0, 0.0], dtype = np.float)

        for j in range(bin_num):
            if j == i:
                continue
            pos_j = positions[j]

            divec = pos_j - pos_i

            mod = math.sqrt(divec[0] ** 2 + divec[1] ** 2 + divec[2] ** 2)
            dis = matrix[i, j]

            if dis == 0 or mod == 0:
                continue

            divec = divec / mod

            if i == j + 1 or i == j - 1:
                if mod > max_dis:
                    err = mod - max_dis
                elif mod < min_dis:
                    err = mod - min_dis
                else:
                    err = 0.0
            else:
                err = mod - dis
            
            divec = divec * err
            ervec = ervec + divec
        
        ervec /= bin_num
        trans_matrix[i] += ervec

    for vec in trans_matrix:
        f_value += math.sqrt(vec[0] ** 2 + vec[1] ** 2 + vec[2] ** 2)
    
    return trans_matrix, f_value
