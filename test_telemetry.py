from telemetry import make_telemetry,summary
from app import app

def test_deterministic(): assert make_telemetry()==make_telemetry()
def test_row_count(): assert len(make_telemetry(laps=12))==48
def test_wear_increases():
    rows=[r for r in make_telemetry() if r['driver']=='M. Patel']
    assert rows[-1]['tire_wear_pct']>rows[0]['tire_wear_pct']
def test_standings_sorted():
    scores=[r['total_time'] for r in summary(make_telemetry())]
    assert scores==sorted(scores)
def test_api():
    client=app.test_client(); res=client.get('/api/telemetry?laps=3')
    assert res.status_code==200 and len(res.json['records'])==12
    assert client.get('/api/telemetry?laps=0').status_code==400
