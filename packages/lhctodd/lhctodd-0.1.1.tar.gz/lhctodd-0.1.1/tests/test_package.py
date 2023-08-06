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
    print("Gamma_vector_qq = ", m.theory.width.vector_qq(100))


