def test_import_module():
    """
    Vérifie que le module principal itcaa_ai_offline peut être importé.
    Ce test garantit que la structure du projet est correcte et que
    le PYTHONPATH est bien configuré dans le workflow CI/CD.
    """
    import itcaa_ai_offline
    assert hasattr(itcaa_ai_offline, "__doc__")
