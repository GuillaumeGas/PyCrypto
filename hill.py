
def bezout(a, b):
    ''' Calcule (u, v, p) tels que a*u + b*v = p et p = pgcd(a, b) '''
    if a == 0 and b == 0:
        return (0, 0, 0)
    if b == 0:
        return (a / abs(a), 0, abs(a))
    (u, v, p) = bezout(b, a % b)
    return (v, (u - v * (a / b)), p)


def inverse_mod(x, m):
    ''' Calcule y dans [[0, m-1]] tel que x*y % abs(m) = 1 '''
    (u, _, p) = bezout(x, m)
    if p == 1:
        return u % abs(m)
    else:
        raise Exception("%s et %s ne sont pas premiers entre eux" % (x, m))


def co_mat(M):  # tmp...
    tmp = M[0][0]
    M[0][0] = M[1][1]
    M[1][1] = tmp
    M[0][1] *= -1
    M[1][0] *= -1
    return M


def det_mat(M):  # tmp...
    return (M[0][0] * M[1][1]) - (M[0][1] * M[1][0])


def calculer_inverse(M):
    det = det_mat(M)
    idet = inverse_mod(det, 26)
    print ("Det inverse modulaire : %s" % idet)
    cM = co_mat(M)
    return mul_kmat(idet, cM)


def mul_kmat(k, M):
    for i in range(0, len(M)):
        for j in range(0, len(M[0])):
            M[i][j] *= k
    return M


def prod_mat(M1, M2, dimM1, dimM2):
    (dim_x_m1, dim_y_m1) = dimM1
    (dim_x_m2, dim_y_m2) = dimM2
    if not (len(M1[0]) == len(M2)):
        raise Exception("On ne peut pas multiplier ces deux matrices !")
    else:
        res = []
        colRes = 0
        linRes = 0

        for i in range(0, dim_x_m1):
            res.append([])
            for j in range(0, dim_y_m1):
                res[i].append(0)

        for linA in range(0, dim_x_m1):
            for colB in range(0, dim_y_m2):
                linB = 0
                for colA in range(0, dim_y_m1):
                    if dim_x_m2 > 1:
                        res[linRes][colRes] += M1[linA][colA] * M2[linB][colB]
                    else:
                        res[linRes][colRes] += M1[linA][colA] * M2[linB]
                    linB += 1
                colRes += 1
            linRes += 1
            colRes = 0
    return res


def mat_mod(M, mod):
    for i in range(0, len(M)):
        for j in range(0, len(M[0])):
            M[i][j] %= mod
    return M


def decrypt(key, code):
    res = []
    for vec in code:
        tmp = prod_mat(key, vec, (len(key), len(key)), (1, 2))
        res.append(tmp[0])
        res.append(tmp[1])
    print ("mat_mod")
    print (res)
    mat_mod(res, 26)
    print ("mat_mod")
    print (res)
    res2 = ""
    for i in res:
        for j in i:
            res2 += chr((j + 65))
    return res2

M = [[10, 18], [0, 3]]
C = [[19, 17], [15, 4]]
code = [[19, 15], [17, 4], [15, 10]]

print ("Matrices de depart : ")
print ("M : ")
print (M)
print ("C : ")
print (C)
print ("\n")

print ("Calcul de l'inverse de C...")
Ci = calculer_inverse(C)
print (Ci)
print ("\n")
print ("Calcul de Cmod26...")
Ci = mat_mod(Ci, 26)
print (Ci)
print ("\n")
print ("Calcul de M*Ci...")
Ki = prod_mat(M, Ci, (len(M), len(M)), (len(C), len(C)))
print (Ki)
print ("\n")
print ("Calcul de Kmod26...")
Ki = mat_mod(Ki, 26)

print (Ki)

m = decrypt(Ki, code)
print (m)
