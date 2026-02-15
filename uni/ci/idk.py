def de_morgan_test(a, b):
    left = 1 - max(a, b)
    right = min(1-a, 1-b)
    return abs(left-right) < 1e-6

import numpy as np

def fuzzy_composition(A, R):
    A = np.array(A)
    R = np.array(R)
    B = []
    for j in range(R.shape[1]):
        col = R[:, j]
        B.append(max(min(A[i], col[i]) for i in range(len(A))))
    return B

import numpy as np

# s-norms (Union)
def s_max(a, b):
    return np.maximum(a, b)

def s_algebraic(a, b):
    return a + b - a*b

def s_bounded(a, b):
    return np.minimum(1, a + b)

def s_drastic(a, b):
    res = np.zeros_like(a)
    mask = (a > 0) & (b > 0)
    res[mask] = 1
    res[~mask] = np.maximum(a[~mask], b[~mask])
    return res


# t-norms (Intersection)
def t_min(a, b):
    return np.minimum(a, b)

def t_product(a, b):
    return a * b

def t_lukasiewicz(a, b):
    return np.maximum(0, a + b - 1)

def t_drastic(a, b):
    res = np.zeros_like(a)
    mask = (a == 1) | (b == 1)
    res[mask] = np.minimum(a[mask], b[mask])
    return res


# Negation
def neg_standard(a):
    return 1 - a

def fuzzy_cartesian(A, B, tnorm=t_min):
    # A: shape (n,)
    # B: shape (m,)
    n, m = len(A), len(B)
    R = np.zeros((n, m))
    for i in range(n):
        for j in range(m):
            R[i, j] = tnorm(A[i], B[j])
    return R


def fuzzy_relation_composition(R, S, tnorm=t_min, snorm=np.max):
    # R: (n, m)
    # S: (m, k)
    n, m = R.shape
    m2, k = S.shape
    assert m == m2
    
    T = np.zeros((n, k))
    for i in range(n):
        for j in range(k):
            vals = []
            for y in range(m):
                vals.append(tnorm(R[i, y], S[y, j]))
            T[i, j] = snorm(vals)
    return T

def fuzzy_inference(A, R, tnorm=t_min, snorm=np.max):
    # A: (n,)
    # R: (n, m)
    n, m = R.shape
    B = np.zeros(m)
    for j in range(m):
        vals = []
        for i in range(n):
            vals.append(tnorm(A[i], R[i, j]))
        B[j] = snorm(vals)
    return B
def binary_to_gray_str(binary):
    gray = binary[0]
    for i in range(1, len(binary)):
        if binary[i-1] == binary[i]:
            gray += '0'
        else:
            gray += '1'
    return gray
def gray_to_binary_str(gray):
    binary = gray[0]
    for i in range(1, len(gray)):
        if binary[i-1] == gray[i]:
            binary += '0'
        else:
            binary += '1'
    return binary
print(binary_to_gray_str('1010'))
import random

def pmx(p1, p2):
    n = len(p1)
    c1, c2 = sorted(random.sample(range(n), 2))
    child = [-1] * n

    # copy middle part from parent1
    child[c1:c2+1] = p1[c1:c2+1]

    # mapping
    for i in range(c1, c2+1):
        if p2[i] not in child:
            val = p2[i]
            pos = i
            while True:
                mapped = p1[pos]
                pos = p2.index(mapped)
                if child[pos] == -1:
                    child[pos] = val
                    break

    # fill remaining from parent2
    for i in range(n):
        if child[i] == -1:
            child[i] = p2[i]

    return child

import random

def ox(p1, p2):
    n = len(p1)
    c1, c2 = sorted(random.sample(range(n), 2))
    child = [-1] * n

    # copy slice from parent1
    child[c1:c2+1] = p1[c1:c2+1]

    # fill remaining from parent2 in order
    p2_filtered = [x for x in p2 if x not in child]

    idx = 0
    for i in range(n):
        if child[i] == -1:
            child[i] = p2_filtered[idx]
            idx += 1

    return child

def cx(p1, p2):
    n = len(p1)
    child = [-1] * n
    visited = [False] * n

    index = 0
    while not visited[index]:
        visited[index] = True
        child[index] = p1[index]
        index = p1.index(p2[index])

    for i in range(n):
        if child[i] == -1:
            child[i] = p2[i]

    return child

p1 = [5,6,2,4,8,3,7,1]
p2 = [6,8,1,3,7,5,4,2]

print("Parent1:", p1)
print("Parent2:", p2)

print("PMX :", pmx(p1, p2))
print("OX  :", ox(p1, p2))
print("CX  :", cx(p1, p2))
