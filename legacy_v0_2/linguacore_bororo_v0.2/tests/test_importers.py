from pathlib import Path
from importers.conllu import parse
from importers.dictionary_tsv import records

def test_conllu_is_never_validated(tmp_path: Path):
    p = tmp_path / "x.conllu"
    p.write_text("# sent_id = x\n# text = A.\n1\tA\ta\tNOUN\t_\t_\t0\troot\t_\t_\n\n", encoding="utf-8")
    sentence = next(parse(p))
    assert sentence["status"] == "imported_unverified"
    assert sentence["tokens"][0]["morphological_analyses"][0]["preferred"] is False

def test_dictionary_keeps_homographs(tmp_path: Path):
    p = tmp_path / "d.tsv"
    p.write_text("id\tentry\tdefinition\n1\tx\tone\n2\tx\ttwo\n", encoding="utf-8")
    data = list(records(p))
    assert len(data) == 2
    assert data[0]["resource_id"] != data[1]["resource_id"]
