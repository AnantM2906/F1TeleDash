"""Seeded synthetic racing telemetry; no real F1 or team telemetry data."""
import math
import random

DRIVERS=[('M. Patel','Apex GP','#1'),('L. Chen','Velocity Racing','#2'),('S. Rivera','Northstar','#3'),('J. Okafor','Apex GP','#4')]

def make_telemetry(seed=42,laps=18):
    if laps < 1 or laps > 100: raise ValueError('laps must be 1..100')
    rng=random.Random(seed)
    records=[]
    for d,(name,team,number) in enumerate(DRIVERS):
        elapsed=0.0
        for lap in range(1,laps+1):
            tire_wear=min(100,round((lap-1)*3.8+rng.uniform(0,2),1))
            sectors=[round(27.5+d*.38+rng.uniform(-.6,.7)+tire_wear*.006,3),
                     round(33+d*.4+rng.uniform(-.8,.8)+tire_wear*.008,3),
                     round(24.2+d*.3+rng.uniform(-.5,.6)+tire_wear*.005,3)]
            lap_time=round(sum(sectors),3); elapsed+=lap_time
            speed=round(310-d*2+8*math.sin(lap*.7+d)+rng.uniform(-3,3)-tire_wear*.04,1)
            records.append({'driver':name,'team':team,'number':number,'lap':lap,
                            's1':sectors[0],'s2':sectors[1],'s3':sectors[2],
                            'lap_time':lap_time,'speed_kph':speed,'tire_wear_pct':tire_wear,
                            'elapsed':round(elapsed,3)})
    return records

def summary(records):
    by_driver={}
    for item in records: by_driver.setdefault(item['driver'],[]).append(item)
    result=[]
    for name,rs in by_driver.items():
        result.append({'driver':name,'team':rs[0]['team'],'laps':len(rs),
                      'total_time':round(sum(r['lap_time'] for r in rs),3),
                      'best_lap':min(r['lap_time'] for r in rs),
                      'avg_speed':round(sum(r['speed_kph'] for r in rs)/len(rs),1)})
    return sorted(result,key=lambda x:x['total_time'])
