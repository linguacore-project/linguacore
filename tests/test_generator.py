import runpy
from pathlib import Path
def test_generator_creates_artifacts():
    ns=runpy.run_path('tools/generate.py')
    assert ns['generate']() >= 4
    assert (Path('generated')/'models.ts').exists()
    assert 'LanguageSpec' in (Path('generated')/'models.py').read_text()
