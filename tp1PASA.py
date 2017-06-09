import juegoPASA
import time
import numpy as np
import matplotlib.pyplot as plt
import math
import csv
import scipy.signal as signal


def lms(u, d, M, mu, leak, w):
    y = np.dot(u, w)
    e = +d[M-1] - y
    yf= y
    w = w*leak+ mu * u * e / (np.dot(u,u)+1)
    return yf, math.pow(e,2), w


def rls(u, d, M, lam, w, P):
    in_lam =  1.0/lam
    lambda1Pu = in_lam * np.dot(P, u)
    k = lambda1Pu / (1 + np.dot(np.transpose(u), lambda1Pu))
    xi = d[M - 1] - np.dot(w, u)
    w += k * np.conj(xi);
    P = in_lam * (P - np.dot(np.dot(k, np.transpose(u)),P))
    return w, P

juegoPASA.setup()
prev_pos = 0
M = 4
ul = np.zeros(20000)
dl = np.zeros(20000)
yl = np.zeros(20000)
u = np.zeros(M)
d = np.zeros(M)
w = 2*(np.random.rand(M)-0.5) #np.zeros(M)
J = np.zeros(200000)
mu = math.pow(10,-1)
p_sign = np.zeros(M) + 0.2

w[M-1] = 1

yx = np.zeros(M)
pos_in=0
ac = 0
posicion = 0
#RLS
lam = 0.9
rlsDelta = 0.1
P = np.eye(M) / rlsDelta
ind = 0
while juegoPASA.done==0:
    deltax=0#.1*(np.random.rand()-0.5)
    deltay=0
    disparo=0
    dif = 0
    ac = ac*0.95
    arriba,abajo,izquierda,derecha,espacio=juegoPASA.readKey()
    if arriba==1:
        deltay=-4
    if abajo==1:
        deltay=4
    if izquierda==1:
        if ac>-10:
            ac -= 0.4
        dif = -4
    if derecha==1:
        if ac<10:
            ac += 0.4
        dif = 4
    if espacio==1:
        disparo=1
    deltax += dif
    d[0] = deltax
    d = np.roll(d,-1)

    dl[0] = deltax
    dl = np.roll(dl, -1)
    deltax_in = np.dot(d, w)
    yx[0] = deltax
    yx = np.roll(yx, -1)
    prev_pos = posicion
    posicion=juegoPASA.loop(deltax_in/3.2,deltay,disparo)
    delta_after = (posicion - prev_pos)


#    for i in range(0,1):
    #[y,JD,w] = lms(u, d, M, mu,1, w)
    [w,P] = rls(u, d, M,lam , w,P)
    u[0] = delta_after
    u = np.roll(u, -1)

    yl[0] = deltax_in
    yl = np.roll(yl, -1)
    ul[0] = delta_after
    ul = np.roll(ul, -1)
    J[ind] = math.pow(d[M-1]-u[M-1],2)
    #J = np.roll(J, -1)
    ind += 1
    time.sleep(0.02 )
juegoPASA.end()
plt.figure()
plt.plot(ul,label='Respuesta del sistema')
plt.plot(dl,label='Respuesta deseada')
plt.plot(yl,label='Entrada al sistema')
plt.legend(loc='upper center')
plt.title('Senales en tiempo')
plt.xlabel('tiempo')
plt.ylabel('amplitud')
plt.figure()
plt.plot(w)
plt.title('coeficientes del filtro')
plt.figure()
plt.plot(J)
plt.title('J')
plt.xlabel('tiempo')
plt.ylabel('Error cuadratico instantaneo')
plt.show()
print("Su puntaje fue: " + str(juegoPASA.score) + "puntos")

