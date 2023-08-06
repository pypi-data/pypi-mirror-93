from .hexa import get_hexa, get_printable

def test_get_printable ():
    printable = get_printable(b'\x33')
    assert printable == "3"
    printable = get_printable(b'\x46')
    assert printable == "F"
    printable = get_printable(b'\x34')
    assert printable == "4"
    ascii_string = get_printable(b"\x00")
    assert ascii_string == "."

def test_get_hexa ():
    ascii_string = get_hexa(b'\x33')
    assert ascii_string == "33 "
    ascii_string = get_hexa(b'\x00\x34')
    assert ascii_string == "00 34 "
    ascii_string = get_hexa(b"\x46")
    assert ascii_string == "46 "
