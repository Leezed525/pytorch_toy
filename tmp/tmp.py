import matplotlib as plt
import numpy as np





if __name__ == '__main__':
    dp1 = [0, 1, 1, 2, 4, 6, 9]
    dp2 = [0, 1, 1, 2, 4, 6, 9]


    for i in range(7,10000):
        dp1.append(max(dp1[i - 2] * 2, dp1[i - 3] * 3))
        dp2.append(dp2[i - 3] * 3)
        print(i, dp1[i]==dp2[i])

