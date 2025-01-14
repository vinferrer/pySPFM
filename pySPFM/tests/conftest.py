import os
import ssl
from urllib.request import urlretrieve

import pytest

import pySPFM


def pytest_addoption(parser):
    parser.addoption(
        "--skipintegration", action="store_true", default=False, help="Skip integration tests."
    )


@pytest.fixture
def skip_integration(request):
    return request.config.getoption("--skipintegration")


@pytest.fixture
def base_test_path():
    return os.path.join(os.path.dirname(pySPFM.__file__), "tests", "data")


def fetch_file(osf_id, path, filename):
    """
    Fetches file located on OSF and downloads to `path`/`filename`1
    Parameters
    ----------
    osf_id : str
        Unique OSF ID for file to be downloaded. Will be inserted into relevant
        location in URL: https://osf.io/{osf_id}/download
    path : str
        Path to which `filename` should be downloaded. Ideally a temporary
        directory
    filename : str
        Name of file to be downloaded (does not necessarily have to match name
        of file on OSF)
    Returns
    -------
    full_path : str
        Full path to downloaded `filename`
    """
    # This restores the same behavior as before.
    # this three lines make tests dowloads work in windows
    if os.name == "nt":
        orig_sslsocket_init = ssl.SSLSocket.__init__
        ssl.SSLSocket.__init__ = (
            lambda *args, cert_reqs=ssl.CERT_NONE, **kwargs: orig_sslsocket_init(
                *args, cert_reqs=ssl.CERT_NONE, **kwargs
            )
        )
        ssl._create_default_https_context = ssl._create_unverified_context
    url = "https://osf.io/{}/download".format(osf_id)
    full_path = os.path.join(path, filename)
    if not os.path.isfile(full_path):
        urlretrieve(url, full_path)
    return full_path


@pytest.fixture(scope="session")
def testpath(tmp_path_factory):
    """Test path that will be used to download all files"""
    return tmp_path_factory.getbasetemp()


@pytest.fixture
def pylops_results(base_test_path):
    # return fetch_file("bmhtr", testpath, "pylops_fista.npy")
    return os.path.join(base_test_path, "pylops_fista.npy")


@pytest.fixture
def sim_data(base_test_path):
    # return fetch_file("789z6", testpath, "sim_data.npy")
    return os.path.join(base_test_path, "sim_data.npy")


@pytest.fixture
def sim_hrf(base_test_path):
    # return fetch_file("j2u6n", testpath, "sim_hrf.npy")
    return os.path.join(base_test_path, "sim_hrf.npy")


@pytest.fixture
def mask_five_echo(base_test_path):
    # return fetch_file("j2u6n", testpath, "sim_hrf.npy")
    return os.path.join(base_test_path, "mask_five_echo.nii.gz")
