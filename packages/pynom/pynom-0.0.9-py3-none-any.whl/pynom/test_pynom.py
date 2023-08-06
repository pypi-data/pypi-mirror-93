import pytest
from . import PyNom, CombinedException, ExceptionInfo

def test_pynom_allows_a_single_exception_type():
    pynom = PyNom(ZeroDivisionError, 3)
    assert pynom.exception_types_to_eat[0] == ZeroDivisionError
    assert len(pynom.exception_types_to_eat) == 1

def test_simple_pynom():
    pynom = PyNom([ZeroDivisionError], 3)

    for i in range(3):
        with pynom:
            1 / 0

    assert len(pynom._exception_information[ZeroDivisionError]) == 3

    try:
        with pynom:
            1/ 0
    except Exception as ex:
        assert isinstance(ex, ZeroDivisionError)
        assert isinstance(ex, CombinedException)
    else:
        assert 0, 'pynom did not raise'

    assert len(pynom._exception_information[ZeroDivisionError]) == 0

def test_pynom_custom_throw_up_action():
    def throw_up_action(ex):
        assert isinstance(ex, CombinedException)
        assert all([isinstance(a, ExceptionInfo) for a in ex.exception_infos])
        throw_up_action.val = True
        raise ex

    pynom = PyNom([ValueError], 1, throw_up_action)

    with pynom:
        raise ValueError("herro")

    with pytest.raises(ValueError):
        with pynom:
            raise ValueError('i am the breaking point')

    assert throw_up_action.val, 'throw_up_action was not called?'

def test_pynom_can_eat_all_exceptions():
    pynom = PyNom([PyNom.ALL_EXCEPTIONS], 1)

    with pynom:
        raise ValueError

    with pynom:
        raise EnvironmentError

    with pynom:
        raise Exception

    with pynom:
        raise TypeError

    with pytest.raises(ValueError):
        with pynom:
            raise ValueError

def test_pynom_wont_eat_not_listed_exception():
    pynom = PyNom([ValueError], 1)

    with pytest.raises(EnvironmentError):
        with pynom:
            raise EnvironmentError

def test_no_exception_should_not_throw_up():
    pynom = PyNom([PyNom.ALL_EXCEPTIONS], 1, throw_up_action=lambda x: 1/0)

    for i in range(3):
        with pynom:
            pass

def test_pynom_will_call_side_dish_action():
    def side_dish_action(ex):
        assert isinstance(ex, ExceptionInfo)
        if side_dish_action.call_count == 1:
            assert isinstance(ex.exception, RuntimeError)
        elif side_dish_action.call_count == 2:
            assert isinstance(ex.exception, ValueError)
        elif side_dish_action.call_count == 3:
            assert isinstance(ex.exception, EOFError)

        side_dish_action.call_count += 1

    side_dish_action.call_count = 1

    pynom = PyNom(PyNom.ALL_EXCEPTIONS, 2, side_dish_action=side_dish_action)

    with pynom:
        raise RuntimeError
    assert side_dish_action.call_count == 2

    with pynom:
        raise ValueError
    assert side_dish_action.call_count == 3

    with pynom:
        raise EOFError
    assert side_dish_action.call_count == 4

def test_pynom_will_not_call_side_dish_action_if_there_is_no_exception():
    def side_dish_action(ex):
        raise Exception("side_dish_action should not have been called since there was no exception")

    pynom = PyNom(PyNom.ALL_EXCEPTIONS, 2, side_dish_action=side_dish_action)

    for i in range(10):
        with pynom:
            pass
