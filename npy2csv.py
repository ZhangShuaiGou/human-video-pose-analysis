import numpy as np
import sys

b = np.load(sys.argv[1])
n=1
for x in b:
	np.savetxt(str(n)+'.csv',x, delimiter = ' ')
	n+=1

print(len(b))
print("done")
