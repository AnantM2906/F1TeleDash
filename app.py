from flask import Flask, jsonify, render_template, request
from telemetry import DRIVERS,make_telemetry,summary
app=Flask(__name__)

@app.get('/')
def home(): return render_template('index.html')

@app.get('/api/telemetry')
def telemetry():
    try: laps=int(request.args.get('laps',18)); seed=int(request.args.get('seed',42))
    except ValueError: return jsonify({'error':'laps and seed must be integers'}),400
    if not 1<=laps<=100: return jsonify({'error':'laps must be 1..100'}),400
    rows=make_telemetry(seed=seed,laps=laps)
    return jsonify({'source':'synthetic simulator','records':rows,'standings':summary(rows),
                    'drivers':[d[0] for d in DRIVERS]})

if __name__=='__main__': app.run(debug=True,port=5000)
