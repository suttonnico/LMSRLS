import csv
import matplotlib.pyplot as plt
import numpy as np


def averager(x,n):
    y = np.zeros(len(x))
    for i in range(n+1,len(x)-n-1):
        for j in range(-n,n):
            y[i]+= x[i+j]
        y[i] /= (2 * (n + 1))
    return y
JVFFRLS = np.zeros(20000)
with open('VFFRLS0.csv', 'rb') as csvfile:
    data_set = csv.reader(csvfile, delimiter=',')
    for row in data_set:
        J1 = row
    for i in range(0, 20000):
        JVFFRLS[i] = float(J1[i])
JVFFRLS = averager(JVFFRLS,30)

JRLS = np.zeros(20000)
with open('RLS0.csv', 'rb') as csvfile:
    data_set = csv.reader(csvfile, delimiter=',')
    for row in data_set:
        J1 = row

    for i in range(0, 20000):
        JRLS[i] = float(J1[i])

JRLS = averager(JRLS, 10)

JRLSl9900 = np.zeros(20000)
with open('RLSl9900.csv', 'rb') as csvfile:
    data_set = csv.reader(csvfile, delimiter=',')
    for row in data_set:
        J1 = row

    for i in range(0, 20000):
        JRLSl9900[i] = float(J1[i])

JRLSl9900 = averager(JRLSl9900, 30)

JRLSl950 = np.zeros(20000)
with open('RLSl950.csv', 'rb') as csvfile:
    data_set = csv.reader(csvfile, delimiter=',')
    for row in data_set:
        J1 = row

    for i in range(0, 20000):
        JRLSl950[i] = float(J1[i])

JRLSl950 = averager(JRLSl950, 30)


JRLSl900 = np.zeros(20000)
with open('RLSl900.csv', 'rb') as csvfile:
    data_set = csv.reader(csvfile, delimiter=',')
    for row in data_set:
        J1 = row

    for i in range(0, 20000):
        JRLSl900[i] = float(J1[i])

JRLSl900 = averager(JRLSl900, 30)


JRLSl850 = np.zeros(20000)
with open('RLSl850.csv', 'rb') as csvfile:
    data_set = csv.reader(csvfile, delimiter=',')
    for row in data_set:
        J1 = row

    for i in range(0, 20000):
        JRLSl850[i] = float(J1[i])

JRLSl850 = averager(JRLSl850, 30)


JRLSl800 = np.zeros(20000)
with open('RLSl80.csv', 'rb') as csvfile:
    data_set = csv.reader(csvfile, delimiter=',')
    for row in data_set:
        J1 = row

    for i in range(0, 20000):
        JRLSl800[i] = float(J1[i])

JRLSl800 = averager(JRLSl800, 30)




plt.figure()
plt.semilogy(JRLSl800,label='l=0.80')
plt.semilogy(JRLSl850,label='l=0.85')
plt.semilogy(JRLSl900,label='l=0.90')
plt.semilogy(JRLSl950,label='l=0.95')
plt.semilogy(JRLSl9900,label='l=0.99')
plt.semilogy(JVFFRLS,label='VFFRLS')
plt.legend(loc='upper center')
plt.title('J')
plt.xlabel('n')
plt.ylabel('Amp')

plt.figure()
plt.semilogy(JVFFRLS,label='VFFRLS')
plt.semilogy(JRLS,label='RLS')
plt.legend(loc='upper center')
plt.title('J')
plt.xlabel('tiempo')
plt.show()