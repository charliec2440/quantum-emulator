from quantumfunctions import *
import datetime

def test_one():
    m = Matrix([3, 6], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18])
    print(m)
    print(repr(m))

def test_two():
    m_one = Matrix([4, 4], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16])
    m_two = Matrix([4, 4], [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31])
    m_three = Matrix([3, 2], [1, 2, 3, 4, 5, 6])
    m_four = Matrix([3, 2], [0, 5, 7, 2, 1, 0])
    x = m_one + m_two
    try:
        y = m_one + m_three
    except:
        y = -1
    z = m_three - m_four
    if x.data == [2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35, 38, 41, 44, 47] and y == -1 and z.data == [1, -3, -4, 2, 4, 6]:
        print( "Test two passed!")
    else:
        print( "Test two failed.")

def test_three():
    m_one = Matrix([1, 5], [1, 1, 1, 1, 1])
    m_two = Matrix([1, 5], [2, 2, 2, 2, 2])
    m_three = Matrix([1, 3], [1, 2, 3])
    x = m_one.dot(m_two)
    try:
        y = m_one.dot(m_three)
    except:
        y = None
    if x == 10 and y == None:
        print("Test three passed!")
    else:
        print( "Test three failed.")


def test_four():
    edges = []
    non_inv = 0
    start_time = datetime.datetime.now()
    for i in range(1000000):
        l = int((random() * 10) // 1) + 1
        m = Matrix([l, l], [(random()* 100)//1 for i in range(l * l)])
        id = identity(l)
        x = m.inverse()
        if x == -1:
            non_inv += 1
        else:
            y = m * m.inv
            for j in range(l * l):
                if round(y.data[j], 5) == id.data[j]:
                    pass
                else:
                    edges.append(m)
        if i % 1000 == 0 and i != 0:
            t = datetime.datetime.now()
            time_taken = (t - start_time).total_seconds()
            print(f"{int(i / 1000)} out of 1000 in {time_taken} seconds, estimated {(time_taken / (i / 1000000)) - time_taken} remaining")
    finish_time = datetime.datetime.now()
    print(f"Tested 1000000 matricies in {(finish_time - start_time).total_seconds()} seconds with {non_inv} non-invertable matrices and {len(edges)} edge cases")
    if len(edges) > 0:
        for i in edges:
            print([i.rows, i])

def test_five():
    q = QubitSystem([1, 16], [0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25])
    print(q)
    print(repr(q))
    v = q.measurement()
    w = q.specific_measurement(3)
    x = q.controlled_measurement(1, 1)
    y = q.large_specific_measurement(2, False)
    z = q.large_controlled_measurement(2, True, "11")
    print(v)
    print(w)
    print(x)
    print(y)
    print(z)

def test_six():
    qubit_one = QubitSystem([1, 2], [0, 1])
    qubit_two = QubitSystem([1, 2], [1 ,0])
    try:
        qubit_three = QubitSystem([2, 2], [1, 2, 3, 4])
        print("Test six failed.")
        return
    except:
        pass
    qubit_four = qubit_one.entanglement(qubit_two)
    gate_one = QuantumGate([4, 4], [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0])
    try:
        gate_two = QuantumGate([2, 3], [1, 2, 3, 4, 5, 6])
        print( "Test six failed.")
        return
    except:
        pass
    final_system = gate_one * qubit_four
    x = [0, 0, 0, 1]
    for i in range(len(final_system.data)):
        if final_system.data[i] == x[i]:
            pass
        else:
            print("Test six failed.")
            return
    print( "Test six passed!")


def test_seven():
    theta= PI/ 2
    x = pauli_x()
    #print(x)
    y = pauli_y()
    #print(y)
    z = pauli_z()
    #print(z)
    h = hadamard()
    #print(h)
    p = phase()
    #print(p)
    p_b_e = pi_by_eight()
    #print(p_b_e)
    x_r = x_rotation(theta)
    print(x_r)
    y_r = y_rotation(theta)
    print(y_r)
    z_r = z_rotation(theta)
    print(z_r)
    s = swap()
    print(s)

def test_eight():
    im_one = IrrationalNumber(3, 2)
    im_two = IrrationalNumber(5, -1)
    im_three = im_one * im_two
    c_one = im_one + im_two + im_one * im_two
    c_two = ComplexNumber([IrrationalNumber(4, 3), IrrationalNumber(7, -1), IrrationalNumber(8, 1)])
    c_three = c_one + c_two
    if im_three.absoulute_value() == 450 and c_three.abs() == 26.90724809414742:
        print( "Test eight passed!")
    else:
        print( "Test eight failed.")

def test_nine():
    print((2 ** -12), ANGLES[11])
    print((2 ** -24), ANGLES[23])
    print((2 ** -36), ANGLES[35])
    print((2 ** -48), ANGLES[47])
    print((2 ** -60), ANGLES[59])

def test_ten():
    a_one = PI / 6
    a_two = PI / 4
    a_three = PI / 3
    a_four = PI / 2
    print(sine(a_one))
    print(tangent(a_two))
    print(cosine(a_three))
    print(cordic(a_four))