from pathlib import Path
import yaml
def test_entity_codes_are_unique():
    specs=[yaml.safe_load(p.read_text()) for p in Path('spec/entities').glob('*.yaml')]
    codes=[s['code'] for s in specs]
    assert len(codes)==len(set(codes))
def test_all_entities_have_description():
    for p in Path('spec/entities').glob('*.yaml'):
        assert yaml.safe_load(p.read_text()).get('description')
