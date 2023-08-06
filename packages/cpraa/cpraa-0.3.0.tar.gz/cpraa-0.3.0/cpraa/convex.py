from numpy import array
from pypoman import compute_polytope_vertices


# # no semantics, only constraints for  probability distribution
# A = array([
#     [-1, -1, -1, -1],
#     [1, 1, 1, 1],
#     [0, 0, 0, -1],
#     [0, 0, -1, 0],
#     [0, -1, 0, 0],
#     [-1, 0, 0, 0]])
# b = array([-1, 1, 0, 0, 0, 0])

# # CF semantics: p_A_B == 0
# A = array([
#     [-1, -1, -1, -1],
#     [1, 1, 1, 1],
#     [0, 0, 0, -1],
#     [0, 0, -1, 0],
#     [0, -1, 0, 0],
#     [-1, 0, 0, 0],
#     [0, 0, 0, -1],
#     [0, 0, 0, 1]])
# b = array([-1, 1, 0, 0, 0, 0, 0, 0])

# # ElmAdm semantics: p_nA_B == 0, p_A_B == 0
# A = array([
#     [-1, -1, -1, -1],
#     [1, 1, 1, 1],
#     [0, 0, 0, -1],
#     [0, 0, -1, 0],
#     [0, -1, 0, 0],
#     [-1, 0, 0, 0],
#     [0, 0, 0, -1],
#     [0, 0, 0, 1],
#     [0, -1, 0, 0],
#     [0, 1, 0, 0]])
# b = array([-1, 1, 0, 0, 0, 0, 0, 0, 0, 0])

# # PrAdm semantics: p_A_B == 0, p_nB >= 1, p_nA <= 1
# # i.e., - p_nA_nB - p_A_nB <= -1 and p_nA_nB + p_nA_B <= 1
# A = array([
#     [-1, -1, -1, -1],
#     [1, 1, 1, 1],
#     [0, 0, 0, -1],
#     [0, 0, -1, 0],
#     [0, -1, 0, 0],
#     [-1, 0, 0, 0],
#     [0, 0, 0, -1],
#     [0, 0, 0, 1],
#     [-1, 0, -1, 0],
#     [1, 1, 0, 0]])
# b = array([-1, 1, 0, 0, 0, 0, 0, 0, -1, 1])

# JntAdm/MinAdm semantics: p_A_B == 0, p_B == 0
A = array([
    [-1, -1, -1, -1],
    [1, 1, 1, 1],
    [0, 0, 0, -1],
    [0, 0, -1, 0],
    [0, -1, 0, 0],
    [-1, 0, 0, 0],
    [0, 0, 0, -1],
    [0, 0, 0, 1],
    [0, -1, 0, -1],
    [0, 1, 0, 1]])
print(A)
b = array([-1, 1, 0, 0, 0, 0, 0, 0, 0, 0])

# computes x with A * x <= b
vertices = compute_polytope_vertices(A, b)
print(vertices)
