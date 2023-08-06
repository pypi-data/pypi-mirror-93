import re
from pathlib import Path
import asyncio
import json
from dl2050utils.core import *

def q(db, qss):
    res = None
    for qs in qss.split(';'): res = asyncio.get_event_loop().run_until_complete(db.query(qs))
    return res

def get_model_names(path):
    models = []
    for f in Path(path).glob('*.json'):
        r = re.search('(.*)$', f.stem, re.IGNORECASE)
        if(r is None): continue
        models.append(r.group(1))
    return models

def create_model(db, model, fname=None, path='.'):
    fname = fname or f'{model}.json'
    fname = f'{path}/{fname}'
    try:
        with open(fname) as f: meta=json.load(f)
        q(db, f"insert into models (model,meta) values ('{model}','{json.dumps(meta)}')")
        return False
    except Exception as e:
        print(str(e))
        return True

def update_model(db, model, fname=None, path='.'):
    fname = fname or f'{model}.json'
    fname = f'{path}/{fname}'
    try:
        with open(fname) as f: meta=json.load(f)
        q(db, f"update models set meta='{json.dumps(meta)}' where model='{model}'")
        return False
    except Exception as e:
        print(str(e))
        return True
    
def merge_model(db, model, fname, path='.'):
    fname = f'{path}/{fname}'
    try:
        meta = get_model(db, model)
        with open(fname) as f: meta2=json.load(f)
        meta = {**meta, **meta2}
        q(db, f"update models set meta='{json.dumps(meta)}' where model='{model}'")
        return False
    except Exception as e:
        print(str(e))
        return True

def delete_model(db, model):
    return q(db, f"delete from models where model='{model}'")

def get_all_models(db):
    return [e['model'] for e in q(db,f"select model from models")]

def get_model(db, model):
    try:
        return json.loads(q(db, f"select meta from models where model='{model}'")[0]['meta'])
    except Exception as e:
        return 

async def get_meta(db, model):
    row = await db.select_one('models', {'model': model})
    if row is not None: return json.loads(row['meta'])
    return None