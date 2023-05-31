from itertools import product

creators = {
    "User": [1, 2, 3],
    "Post": [1, 5, 6],
    "Comment": [4, 5, 7]
}

# print(list(product(list(creators.values()))))

# A = [[1, 2], [3, 4]]
A = list(creators.values())
print(list(product(*A)))