

import numpy as np

# ------------------------------------------------------------
# 1. Creating Arrays
# ------------------------------------------------------------
a = np.array([1, 2, 3])                  # 1D array
b = np.array([[1, 2], [3, 4]])           # 2D array
print("Array a:", a)
print("Array b:\n", b)

zeros = np.zeros((2, 3))                 # 2x3 zeros
ones = np.ones((2, 3))                   # 2x3 ones
eye = np.eye(3)                          # identity matrix
rand = np.random.rand(2, 3)              # random floats
arange = np.arange(0, 10, 2)             # 0 to 10 step 2
lin = np.linspace(0, 1, 5)               # 5 points between 0 and 1

# ------------------------------------------------------------
# 2. Array Attributes
# ------------------------------------------------------------
print("Shape:", b.shape)
print("Dimensions:", b.ndim)
print("Data type:", b.dtype)
print("Size:", b.size)

# ------------------------------------------------------------
# 3. Indexing & Slicing
# ------------------------------------------------------------
arr = np.array([[10, 20, 30], [40, 50, 60]])
print(arr[0, 1])         # element at row 0, col 1 → 20
print(arr[:, 1])         # all rows, col 1
print(arr[0:2, 1:3])     # slicing submatrix
print(arr[-1])           # last row

# ------------------------------------------------------------
# 4. Reshaping
# ------------------------------------------------------------
r = np.arange(1, 13)       # [1,...,12]
print(r.reshape(3, 4))     # reshape to 3x4
print(r.reshape(-1, 6))    # let NumPy infer

# ------------------------------------------------------------
# 5. Stacking Arrays
# ------------------------------------------------------------
x = np.array([1, 2])
y = np.array([3, 4])
print(np.vstack((x, y)))   # vertical stack
print(np.hstack((x, y)))   # horizontal stack

# ------------------------------------------------------------
# 6. Basic Operations
# ------------------------------------------------------------
arr1 = np.array([1, 2, 3])
arr2 = np.array([4, 5, 6])

print(arr1 + arr2)         # element-wise add
print(arr1 * arr2)         # element-wise multiply
print(arr1 ** 2)           # power
print(np.dot(arr1, arr2))  # dot product

# Broadcasting
m = np.array([[1], [2], [3]])  # 3x1
n = np.array([10, 20, 30])     # 1x3
print(m + n)                   # broadcast to 3x3

# ------------------------------------------------------------
# 7. Universal Functions (ufuncs)
# ------------------------------------------------------------
print(np.sqrt(arr2))
print(np.exp(arr1))
print(np.log(arr2))
print(np.sin(np.pi / 2))

# ------------------------------------------------------------
# 8. Statistics
# ------------------------------------------------------------
stats = np.array([[1, 2, 3], [4, 5, 6]])
print(stats.sum())
print(stats.mean())
print(stats.std())
print(stats.min(), stats.max())
print(stats.sum(axis=0))   # column sums
print(stats.sum(axis=1))   # row sums

# ------------------------------------------------------------
# 9. Boolean Indexing & Filtering
# ------------------------------------------------------------
nums = np.array([10, 20, 30, 40, 50])
print(nums[nums > 25])          # filter values > 25
nums[nums > 25] = -1            # modify filtered values
print(nums)

# ------------------------------------------------------------
# 10. Fancy Indexing
# ------------------------------------------------------------
arr = np.arange(10, 100, 10)
print(arr[[0, 2, 4]])           # pick specific elements
print(arr[[1, 3, 5]] * 2)       # multiply selection

# ------------------------------------------------------------
# 11. Linear Algebra
# ------------------------------------------------------------
M = np.array([[1, 2], [3, 4]])
N = np.array([[5, 6], [7, 8]])
print(np.dot(M, N))             # matrix multiplication
print(np.linalg.inv(M))         # inverse
print(np.linalg.det(M))         # determinant
print(np.linalg.eig(M))         # eigenvalues/vectors

# ------------------------------------------------------------
# 12. Random Module
# ------------------------------------------------------------
print(np.random.rand(3))          # uniform [0,1)
print(np.random.randn(3))         # normal distribution
print(np.random.randint(1, 10, 5))# random ints
np.random.seed(42)                # reproducibility
print(np.random.rand(3))

# ------------------------------------------------------------
# 13. Advanced Indexing (Masks & Conditions)
# ------------------------------------------------------------
A = np.arange(1, 11)
mask = (A % 2 == 0)
print(A[mask])                    # even numbers
print(np.where(A > 5, "big", "small"))

# ------------------------------------------------------------
# 14. Advanced: Broadcasting in Practice
# ------------------------------------------------------------
X = np.arange(1, 4).reshape(3, 1)
Y = np.arange(1, 4)
print("Broadcasted Sum:\n", X + Y)

# ------------------------------------------------------------
# 15. Advanced: Structured Arrays
# ------------------------------------------------------------
dtype = [("Name", "U10"), ("Age", "i4"), ("Salary", "f8")]
people = np.array([("Alice", 25, 50000), ("Bob", 30, 60000)], dtype=dtype)
print("\nStructured Array:\n", people)
print("Names:", people["Name"])
print("Average Salary:", people["Salary"].mean())

# ------------------------------------------------------------
# 16. Advanced: Vectorization
# ------------------------------------------------------------
nums = np.arange(1, 6)
# Instead of loop: [n*n for n in nums]
print(nums ** 2)

# ------------------------------------------------------------
# 17. Advanced: Broadcasting with Higher Dimensions
# ------------------------------------------------------------
A = np.ones((3, 1))
B = np.arange(1, 4)
print("3x1 + 1x3 =\n", A + B)

# ------------------------------------------------------------
# 18. Advanced: Memory & Views
# ------------------------------------------------------------
x = np.arange(10)
y = x[2:7]      # view, not copy
y[:] = 99
print("Original after view modification:", x)

# ------------------------------------------------------------
# 19. Advanced: Saving & Loading
# ------------------------------------------------------------
np.save("array.npy", arr1)
loaded = np.load("array.npy")
print("Loaded:", loaded)

# Save/load text
np.savetxt("array.txt", arr1)
print("From txt:", np.loadtxt("array.txt"))

# ------------------------------------------------------------
# 20. Advanced: Meshgrid & Vectorized Computations
# ------------------------------------------------------------
x = np.linspace(-2, 2, 5)
y = np.linspace(-2, 2, 5)
X, Y = np.meshgrid(x, y)
Z = np.sqrt(X**2 + Y**2)
print("\nMeshgrid Z:\n", Z)


