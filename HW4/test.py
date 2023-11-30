import numpy as np
tester = np.array([[[0, 0, 0], [1, 1, 1], [2, 2, 2], [3, 3, 3], [4, 4, 4]],
                    [[5, 5, 5], [6, 6, 6], [7, 7, 7], [8, 8, 8], [9, 9, 9]],
                    [[10, 10, 10], [11, 11, 11], [12, 12, 12], [13, 13, 13], [14, 14, 14]],
                    [[15, 15, 15], [16, 16, 16], [17, 17, 17], [18, 18, 18], [19, 19, 19]]])
print(tester)
print(tester.shape)
test0 = tester[:, :, 0]
test1 = tester[:, :, 1]
test2 = tester[:, :, 2]
print(test2.shape)
print(test2)
out1 = np.multiply(test0, test1)
print("Multiplied: ")
print(out1)