from itertools import combinations

# creators = {
#     "User": [1, 2, 3],
#     "Post": [1, 5, 6],
#     "Comment": [4, 5, 7]
# }

# # print(list(product(list(creators.values()))))

# # A = [[1, 2], [3, 4]]
# A = list(creators.values())
# print(list(product(*A)))


def subarrays(arr):
    for length in range(0, len(arr) + 1):
        for subarray in combinations(arr, length):
            yield subarray


optional_creates = ["A", "B", "C"]
optional_uses = ["D", "E"]

cnt = 0
for creates in subarrays(optional_creates):
    for uses in subarrays(optional_uses):
        print(list(creates) + list(uses))
        cnt += 1

        
