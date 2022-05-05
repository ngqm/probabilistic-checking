"""
Probabilistic matrix multiplication checking
"""

import numpy as np
import timeit
import matplotlib.pyplot as plt


def manual_check(A, B, C):
  """
  Manually check whether AB=C. Return CORRECT or INCORRECT.
  """
  if (A@B==C).all():
    return "CORRECT"
  return "INCORRECT"


def check(A,B,C, trials=1):
  """
  Probabilistically check whether AB=C with trials runs. Return 
  CORRECT or INCORRECT.
  """
  n = A.shape[0]
  for _ in range(trials):
    x = np.random.choice([0,1], size=n)
    if not (A@(B@x)==C@x).all():
      return "INCORRECT"
  return "CORRECT"


def generate_matrix(n):
  """
  Generate random matrices A, B, C=A@B of size nxn.
  """
  A = np.random.randn(n, n)
  B = np.random.randn(n, n)
  C = A@B
  return A, B, C


if __name__=="__main__":

  TRIALS = int(np.log2(100)) # probability of failure is under 1e-2
  MAX_SIZE = int(1e3)
  manual_check_time = []
  check_time = []
  for n in np.linspace(10,MAX_SIZE,num=MAX_SIZE//10):
    A, B, C = generate_matrix(int(n))
    t = timeit.Timer(lambda: manual_check(A, B, C))
    manual_check_time.append(t.timeit(number=10))
    t = timeit.Timer(lambda: check(A, B, C, TRIALS))
    check_time.append(t.timeit(number=10))
  
  # Plot running time
  plt.figure()
  plt.plot(np.linspace(10,MAX_SIZE,num=MAX_SIZE//10), manual_check_time, label="Manual")
  plt.plot(np.linspace(10,MAX_SIZE,num=MAX_SIZE//10), check_time, label="Probabilistic with {} trials".format(TRIALS))
  plt.legend()
  plt.xlabel("Matrix size $n$")
  plt.ylabel("Time (s)")
  plt.title("$n$-by-$n$ Matrix Multiplication Checking")
  plt.show()
