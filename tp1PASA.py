import juegoPASA
import time
import numpy as np
import matplotlib.pyplot as plt
import math
import csv
import scipy.signal as signal

def finish(juegoPASA,dl,yl,ul,J,w,rep, laml):
    plt.figure()
    plt.plot(ul, label='Respuesta del sistema')
    plt.plot(dl, label='Respuesta deseada')
    plt.plot(yl,label='Entrada al sistema')
    plt.legend(loc='upper center')
    plt.title('Senales en tiempo')
    plt.xlabel('tiempo')
    plt.ylabel('amplitud')
    plt.figure()
    plt.plot(w)
    plt.title('coeficientes del filtro')

    plt.figure()
    plt.plot(laml)
    plt.xlabel('n')
    plt.ylabel('valor')
    plt.title('Evolucion de lamda')

    plt.figure()
    plt.plot(J)
    plt.title('J')
    plt.xlabel('tiempo')
    plt.ylabel('Error cuadratico instantaneo')
    plt.show()
    save_str = 'VFFRLS'+str(rep)+'.csv'
    with open(save_str, 'wb') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(J)
    with open('d.csv', 'wb') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(dl)
    print("Su puntaje fue: " + str(juegoPASA.score) + "puntos")
    juegoPASA.end()


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


def vff_rls(u, d, M, lam, w, P, se, sv, sq):
    y = np.dot(u, w)
    e = +d[M - 1] - y
    q = np.dot(np.transpose(u), np.dot(P, u))
    Ka = 2
    a = 1 - 1 / (Ka * M)
    se = a * se + (1 - a) * e ** 2
    KB = 3.01
    B = 1 - 1 / (KB * M)
    sq = a * sq + (1-a) * q ** 2
    sv = B * sv + (1-B) * e ** 2
    lam = sq * sv / (np.abs((se - sv))+0.00000001)/6
    if lam >= 0.96:
        lam = 0.96
    if lam <= 0.7:
        lam = 0.7
    in_lam =  1.0/lam
    lambda1Pu = in_lam * np.dot(P, u)
    k = lambda1Pu / (1 + np.dot(np.transpose(u), lambda1Pu))
    xi = d[M - 1] - np.dot(w, u)
    w += k * np.conj(xi);
    P = in_lam * (P - np.dot(np.dot(k, np.transpose(u)),P))


    return w, P, se, sv, sq, float(lam)


with open('d.csv', 'rb') as csvfile:
    data_set = csv.reader(csvfile, delimiter=',')
    for row in data_set:
        d_in = row
repes = 10
def one_run(rep):
    juegoPASA.setup()
    prev_pos = 0
    M = 4
    ul = np.zeros(20000)
    dl = np.zeros(20000)
    yl = np.zeros(20000)
    sel = np.zeros(20000)
    svl = np.zeros(20000)
    sql = np.zeros(20000)
    laml = np.zeros(20000,'float')
    u = np.zeros(M)
    d = np.zeros(M)
    w = np.zeros(M) #0.4*(np.random.rand(M)-0.5) #np.zeros(M)
    J = np.zeros(200000)
    mu = math.pow(10,-1)
    p_sign = np.zeros(M) + 0.2

    w[M-1] = 1

    yx = np.zeros(M)
    pos_in=0
    ac = 0
    posicion = 0
    #RLS
    lam = 0.8
    rlsDelta = 0.1
    P = np.eye(M) / rlsDelta
    ind = 0
    se = 1.173047648723
    sv = 188.91380598538
    sq = 188.911555360456
    while 1:


        deltax=0
        deltay=0
        disparo=1
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

        deltax += float(d_in[ind])
        d[0] = deltax
        d = np.roll(d,-1)

        dl[ind] = deltax
        #dl = np.roll(dl, -1)
        deltax_in = np.dot(d, w)
        yx[0] = deltax_in
        yx = np.roll(yx, -1)
        prev_pos = posicion
        posicion=juegoPASA.loop(deltax_in,deltay,disparo)
        delta_after = (posicion - prev_pos)

        u[0] = delta_after
        u = np.roll(u, -1)

        #[y,JD,w] = lms(u, d, M, mu,1, w)
        #[w, P] = rls(u, yx, M, lam, w, P)
        [w,P,se,sv,sq, lam] = vff_rls(u, yx, M,lam , w,P,se,sv,sq)
        sel[ind] = se
        svl[ind] = sv
        sql[ind] = sq
        laml[ind] = lam
        yl[ind] = deltax_in
        #yl = np.roll(yl, -1)
        ul[ind] = delta_after
        #ul = np.roll(ul, -1)
        J[ind] = math.pow(d[M-1]-u[M-1],2)
        #J = np.roll(J, -1)
        ind += 1
        #time.sleep(0.01 )
        if ind == 6000:
            finish(juegoPASA, dl, yl, ul, J, w, rep, laml)
            juegoPASA.end()
            break
juegoPASA.end()
