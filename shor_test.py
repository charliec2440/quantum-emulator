from quantumfunctions import *
from random import randint

N = 21
euclidian_algorithm = lambda x, y : euclidian_algorithm(y, x % y) if y != 0 else x
# to get the gcf of two numbers

def shors_algorithm():
    if N % 2 == 0:
        # it it's even then you're finished
        return [2, N // 2]
    while True:
        checked = []
        a = randint(2, N - 1)
        # generate a guess
        if a in checked:
            if len(a) == N - 2:
                # if you've checked all the possibilites then it must be prime
                return [1, N]
            else:
                pass
        else:
            checked.append(a)
            k = euclidian_algorithm(a, N)
            if k != 1:
                # if it shares a factor then you're finished
                return [k, N//k]
            else:
                r = quantum_period_finding(a)
                # turns your guess a into a better option r
                if r % 2 == 1:
                    # a type of r that doesn't work
                    pass
                elif (a ** (r/2)) % N == N - 1:
                    # another type of r that doesn't work
                    pass
                else:
                    factor_one = euclidian_algorithm((a ** (r/2)) + 1, N)
                    factor_two = euclidian_algorithm((a ** (r/2)) - 1, N)
                    # generates two factors from an r that does work
                    return [factor_one, factor_two]

def quantum_period_finding(a):
    m = power_of_two_larger(N * N)
    n = power_of_two_larger(N)
    q_f_t = qft(2 ** m)
    v = IrrationalNumber(1, 1 / (2 ** m))
    while True:
        system_data = [v if (a ** i) % N == j else 0 for i in range(2 ** m) for j in range(2 ** n)]
        system = QubitSystem([1, (2 ** m) * (2 ** n)], system_data)
        result = system.large_specific_measurement(n, True)
        # generates the initial state and takes a measurement of part of it
        new_system = q_f_t * result[1]
        c = int(new_system.measurement(), 2)
        # uses a quantum farrier transform and another measurement to get a c value
        if c == 0:
            # checks that it is a useful values
            pass
        else:
            r = r_from_c(c, m)
            if r == None:
                #if it was not a useful value measured for c
                pass
            else:
                # you have found the period of your function
                return r

def qft(n):
    # creates a quantum fourier transform gate
    size = [n, n]
    data = []
    factor= 1 / IrrationalNumber(1, n)
    m = 2 * PI / n
    for a in range(n):
        for b in range(n):
            data.append(factor * ComplexNumber([IrrationalNumber(round(cosine(m * a * b), 5), 1), IrrationalNumber(round(sine(m * a * b), 5), - 1)]))
    return Matrix(size, data)
    #return QuantumGate(size, data)


def r_from_c(c, m):
    # generates r (the period) from a value c, as long as it was a useful value of c
    p = c
    q = 2 ** m
    subtractor = p / q
    target= 1 / (2 * N * N)
    c_f = []
    while p != 1:
        # creates the continued fraction for c/2Am and then uses that to get the r value along with the inequality that lc/2Am - k/rl < 1/(2 * NA2) for some arbitrary constant k
        # the continued fraction is because it turns out that the fraction k/r will be one of the convergants of the continued fraciton, so you just test each of those until you find the one that works
        print(p, q)
        t = continued_fraction(p, q)
        c_f.append(t[0])
        p, q = t[1][0], t[1][1]
        x = reconstruct_fraction(c_f)
        v = x[0] / x[1]
        if modulus(subtractor - v) < target and x[1] < N:
            return x[1]
    return None

continued_fraction = lambda p, q: [q // p, [q - q // p * p, p]]
# generates the next part of a continued fraction of a number


def reconstruct_fraction(values):
    # reconstructs a continued fraction
    p = 1
    q = values[-1]
    for i in range(1, len(values)):
        p, q = q, p + values[ -i - 1] * q
    return [p, q]

def power_of_two_larger(n):
    # gets the smallest power of two larger than a given input
    m = 1
    while True:
        if (2 ** m) < n:
            m += 1
        else:
            return m

modulus = lambda x: -x if x < 0 else x
# returns the modulus of a number (its absolute value)

print(shors_algorithm()) 
