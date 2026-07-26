from fastapi.testclient import TestClient
from linguacore.main import app
client=TestClient(app)
def test_health():
    r=client.get('/v1/health'); assert r.status_code==200; assert r.json()['version']=='0.3.0'
def test_language_and_sentence_flow():
    language=client.post('/v1/languages',json={'name':'Bororo','native_name':'Boe','iso_639_3':'bor'}); assert language.status_code==201
    lid=language.json()['id']
    sentence=client.post('/v1/sentences',json={'language_id':lid,'sequence':1,'transcription':'Boe ewadaru.'}); assert sentence.status_code==201
    assert client.get('/v1/sentences',params={'language_id':lid}).json()[0]['transcription']=='Boe ewadaru.'
def test_invalid_audio_alignment():
    r=client.post('/v1/sentences',json={'language_id':'x','sequence':1,'transcription':'x','start_ms':20,'end_ms':10})
    assert r.status_code==422
