
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


def mul_mat(M1, M2):
    if not (len(M1[0]) == len(M2)):
        raise Exception("On ne peut pas multiplier ces deux matrices !")
    else:
        res = []
        colRes = 0
        linRes = 0

        for i in range(0, len(M1)):
            res.append([])
            for j in range(0, len(M1[0])):
                res[i].append(0)

        for linA in range(0, len(M1)):
            for colB in range(0, len(M2[0])):
                linB = 0
                for colA in range(0, len(M1[0])):
                    res[linRes][colRes] += M1[linA][colA] * M2[linB][colB]
                    linB += 1
                colRes += 1
            linRes += 1
            colRes = 0
    return res


def mat_mod(M, mod):
    for i in range(0, len(M)):
        for j in range(0, len(M[0])):
            M[i][j] %= 26
    return M

M = [[12, 13], [14, 6]]
C = [[19, 17], [15, 4]]

print ("Calcul de l'inverse de C...")
Ci = calculer_inverse(C)
print (Ci)
Ci = mat_mod(Ci, 26)
print (Ci)
print ("Calcul de M*Ci...")
Ki = mul_mat(M, Ci)
Ki = mat_mod(Ki, 26)

print (Ki)
