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

with open('JNLMS1.csv', 'rb') as csvfile:
    data_set = csv.reader(csvfile, delimiter=',')
    for row in data_set:
        J1 = row
with open('JNLMS2.csv', 'rb') as csvfile:
    data_set = csv.reader(csvfile, delimiter=',')
    for row in data_set:
        J2 = row
with open('JNLMS3.csv', 'rb') as csvfile:
    data_set = csv.reader(csvfile, delimiter=',')
    for row in data_set:
        J3 = row
with open('JNLMS4.csv', 'rb') as csvfile:
    data_set = csv.reader(csvfile, delimiter=',')
    for row in data_set:
        J4 = row
with open('JNLMS5.csv', 'rb') as csvfile:
    data_set = csv.reader(csvfile, delimiter=',')
    for row in data_set:
        J5 = row
with open('JNLMS6.csv', 'rb') as csvfile:
    data_set = csv.reader(csvfile, delimiter=',')
    for row in data_set:
        J6 = row
JNLMS = np.zeros(20000)
for i in range(0,20000):
    JNLMS[i] = (float(J1[i])+float(J2[i])+float(J3[i])+float(J4[i])+float(J5[i])+float(J6[i])) / 6

with open('JLMS1.csv', 'rb') as csvfile:
    data_set = csv.reader(csvfile, delimiter=',')
    for row in data_set:
        J1 = row
with open('JLMS2.csv', 'rb') as csvfile:
    data_set = csv.reader(csvfile, delimiter=',')
    for row in data_set:
        J2 = row
with open('JLMS3.csv', 'rb') as csvfile:
    data_set = csv.reader(csvfile, delimiter=',')
    for row in data_set:
        J3 = row
with open('JLMS4.csv', 'rb') as csvfile:
    data_set = csv.reader(csvfile, delimiter=',')
    for row in data_set:
        J4 = row
with open('JLMS5.csv', 'rb') as csvfile:
    data_set = csv.reader(csvfile, delimiter=',')
    for row in data_set:
        J5 = row
with open('JLMS6.csv', 'rb') as csvfile:
    data_set = csv.reader(csvfile, delimiter=',')
    for row in data_set:
        J6 = row
JLMS = np.zeros(20000)
for i in range(0,20000):
    JLMS[i] = (float(J1[i])+float(J2[i])+float(J3[i])+float(J4[i])+float(J5[i])+float(J6[i])) / 6


with open('JSIN1.csv', 'rb') as csvfile:
    data_set = csv.reader(csvfile, delimiter=',')
    for row in data_set:
        J1 = row
with open('JSIN2.csv', 'rb') as csvfile:
    data_set = csv.reader(csvfile, delimiter=',')
    for row in data_set:
        J2 = row
with open('JSIN3.csv', 'rb') as csvfile:
    data_set = csv.reader(csvfile, delimiter=',')
    for row in data_set:
        J3 = row
with open('JSIN4.csv', 'rb') as csvfile:
    data_set = csv.reader(csvfile, delimiter=',')
    for row in data_set:
        J4 = row
with open('JSIN5.csv', 'rb') as csvfile:
    data_set = csv.reader(csvfile, delimiter=',')
    for row in data_set:
        J5 = row
with open('JSIN6.csv', 'rb') as csvfile:
    data_set = csv.reader(csvfile, delimiter=',')
    for row in data_set:
        J6 = row
JSIN = np.zeros(20000)
for i in range(0,20000):
    JSIN[i] = (float(J1[i])+float(J2[i])+float(J3[i])+float(J4[i])+float(J5[i])+float(J6[i])) / 6


JNLMS=averager(JNLMS,10)
JLMS=averager(JLMS,10)
JSIN=averager(JSIN,10)
print JNLMS
plt.figure()
plt.plot(JNLMS,label='NLMS')
plt.plot(JLMS,label='LMS')
plt.plot(JSIN,label='SIN CONTROL')
plt.legend(loc='upper center')
plt.title('J')
plt.xlabel('tiempo')
plt.show()