import lhctodd as m


def test_version():
    assert m.__version__

def test_data():
    try:
        m.list()
    except:
        raise RuntimeError('Failed to fetch data from database')

def test_thoery():
    # check alpha_s
    print("as(MZ) = ", m.theory.width._as(9.1200000e+01))
    print("gamma_vector_qq = ", m.theory.width.vector_qq(100))
    print("gamma_vector_ll = ", m.theory.width.vector_ll(100))
    print("gamma_vector_nn = ", m.theory.width.vector_nn(100))
    print("gamma_vector_dm = ", m.theory.width.vector_dm(100))
    print("gamma_axial_qq = ", m.theory.width.axial_qq(100))
    print("gamma_axial_ll = ", m.theory.width.axial_ll(100))
    print("gamma_axial_nn = ", m.theory.width.axial_nn(100))
    print("gamma_axial_dm = ", m.theory.width.axial_dm(100))






    



