import csv
import subprocess
import matplotlib.pyplot as plt

Scenario = [1, 2, 4, 8]
output = []
for i in Scenario:
    output.append(int(float(subprocess.getoutput(rf"python client.py C:\Users\Hamza\Documents\ThreadedSocket\dataToSend {i}"))))
    print(output)


plt.plot(output, Scenario)
plt.xlabel("Throughput")
plt.ylabel("Concurrency")
plt.show