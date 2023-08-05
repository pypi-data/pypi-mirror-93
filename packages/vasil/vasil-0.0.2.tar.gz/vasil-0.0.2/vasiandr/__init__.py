def find_sum_of_raw(matrix, size):
    for i in range(int(size[0])):
        for j in range(int(size[1])):
            if i==j and matrix[i][j]<0:
                print('сумма {} рядку: {}'.format(i+1,sum(matrix[i])))
