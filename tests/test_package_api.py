import waypy


def test_package_exports_public_api():
    assert waypy.Agent.__name__ == "Agent"
    assert waypy.Agente.__name__ == "Agente"
    assert waypy.__version__ == "0.2.0"
