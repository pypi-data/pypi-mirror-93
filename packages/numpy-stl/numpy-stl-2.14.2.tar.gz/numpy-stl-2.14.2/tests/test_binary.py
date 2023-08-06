import io
import numpy
import pytest
from stl import mesh, Mode


@pytest.mark.parametrize('mode', [Mode.BINARY, Mode.AUTOMATIC])
def test_ascii_like_binary(tmpdir, speedups, mode):
    _test(tmpdir, speedups, mode, False)
    _test(tmpdir, speedups, mode, True)


def test_binary_in_ascii_mode(tmpdir, speedups):
    with pytest.raises(RuntimeError):
        _test(tmpdir, speedups, mode=Mode.ASCII, use_filehandle=False)

    with pytest.raises(RuntimeError):
        _test(tmpdir, speedups, mode=Mode.ASCII, use_filehandle=True)


def _test(tmpdir, speedups, mode, use_filehandle=True):
    if use_filehandle:
        with open('tests/stl_binary/rear_case.stl', 'rb') as fh:
            mesh.Mesh.from_file('rear_case.stl', fh=fh, speedups=speedups,
                                mode=mode)

        with open('tests/stl_binary/rear_case.stl', 'rb') as fh:
            # Test with BytesIO
            fh = io.BytesIO(fh.read())
            mesh.Mesh.from_file('rear_case.stl', fh=fh, speedups=speedups,
                                mode=mode)
    else:
        mesh.Mesh.from_file('tests/stl_binary/rear_case.stl',
                            speedups=speedups, mode=mode)


@pytest.mark.parametrize("mode", [Mode.BINARY, Mode.AUTOMATIC])
def test_write_bytes_io(binary_file, mode):
    mesh_ = mesh.Mesh.from_file(binary_file)

    # Write to io.Bytes() in BINARY mode.
    fh = io.BytesIO()
    mesh_.save("mesh.stl", fh, mode=mode)

    assert len(fh.getvalue()) > 84
    assert fh.getvalue()[84:] == mesh_.data.tobytes()

    read = mesh.Mesh.from_file("nameless", fh=io.BytesIO(fh.getvalue()))
    assert numpy.allclose(read.vectors, mesh_.vectors)


def test_binary_file():
    list(mesh.Mesh.from_multi_file('tests/stl_tests/triamid.stl'))
