"""
Probabilistic associativity checking
"""

import numpy as np
import timeit
import matplotlib.pyplot as plt


def additive(n):
  """
  Generate multiplication table of the additive
  group modulo n
  """
  S = np.zeros((n,n), dtype=int)
  for i in range(n):
    for j in range(n):
      S[i,j] = (i+j) % n
  return S


def special_table(n):
  """
  Generate multiplication table of a binary operation
  with only one nonassociative triple.
  """
  S = np.zeros((n,n), dtype=int)
  S[-1,-2] = n-1
  return S


def V(S,u,v):
  """
  Generate vector operation on a set with cardinality n
  where the operation is defined by multiplication table S
  """
  n = S.shape[0]
  sum = np.zeros(n)
  for i in range(n):
    for j in range(n):
      if u[i]*v[j]:
        sum[S[i,j]] += 1
  return sum % 2


def manual_check(S):
  """
  Manually check whether the binary operation defined 
  by multiplication table M is associative. 
  Return ASSOCIATIVE or NONASSOCIATIVE.
  """
  n = S.shape[0]
  for i in range(n):
    for j in range(n):
      for k in range(n):
        if S[S[i,j],k] != S[i,S[j,k]]:
          return "NONASSOCIATIVE"
  return "ASSOCIATIVE"


def check(S, trials=1):
  """
  Probabilistically check whether the binary operation defined
  by multiplication table M is associative with trials runs.
  """
  n = S.shape[0]
  for _ in range(trials):
    u = np.random.choice([0,1], size=n)
    v = np.random.choice([0,1], size=n)
    w = np.random.choice([0,1], size=n)
    if not (V(S,u,V(S,v,w))==V(S,V(S,u,v),w)).all():
      return "NONASSOCIATIVE"
  return "ASSOCIATIVE"


def visualise_matrix(S, title):
  """
  Visualise multiplication table S
  """
  n = S.shape[0]
  fig, ax = plt.subplots()
  ax.matshow(S, cmap=plt.cm.Blues)
  for i in range(n):
    for j in range(n):
      c = S[j,i]
      ax.text(i, j, str(c), va="center", ha="center")
  plt.title("{} Multiplication Table ({})".
    format(manual_check(S), title))
  plt.show()


if __name__=="__main__":

  # Visualise multiplication tables
  # n = 5
  # S = additive(n)
  # visualise_matrix(S, "Additive Group Modulo {}".format(n))
  # S = special_table(n)
  # visualise_matrix(S, "Only One Nonassociative Triple")

  # Check associativity
  TRIALS = 35 # probability of failure is under 1e-2
  MAX_SIZE = 125
  manual_check_time = []
  check_time = []
  for n in np.linspace(5,MAX_SIZE,num=MAX_SIZE//5):
    S = special_table(int(n))
    t = timeit.Timer(lambda: manual_check(S))
    manual_check_time.append(t.timeit(number=10))
    t = timeit.Timer(lambda: check(S, TRIALS))
    check_time.append(t.timeit(number=10))

  # Plot the results
  plt.figure()
  plt.plot(np.linspace(5,MAX_SIZE,num=MAX_SIZE//5), manual_check_time, label="Manual")
  plt.plot(np.linspace(5,MAX_SIZE,num=MAX_SIZE//5), check_time, label="Probabilistic with {} trials".format(TRIALS))
  plt.legend()
  plt.xlabel("Size of set")
  plt.ylabel("Time (s)")
  plt.title("Probabilistic Associativity Check")
  plt.show()