import csv,json
from io import StringIO
from collections.abc import Mapping
def _plain(x):
 if isinstance(x,Mapping): return {k:_plain(v) for k,v in x.items()}
 if isinstance(x,tuple): return [_plain(v) for v in x]
 return x
def render_dataset_json(p): return json.dumps({'projection_version':p.version,'rows':[{'ref':str(r.ref),'object_type':r.object_type,'logical_id':r.logical_id,'fields':_plain(r.fields)} for r in p.rows]},ensure_ascii=False,sort_keys=True,separators=(',',':'))
def render_dataset_csv(p):
 out=StringIO(newline=''); w=csv.DictWriter(out,fieldnames=['ref','object_type','logical_id','fields_json'],lineterminator='\n'); w.writeheader()
 for r in p.rows:w.writerow({'ref':str(r.ref),'object_type':r.object_type,'logical_id':r.logical_id,'fields_json':json.dumps(_plain(r.fields),ensure_ascii=False,sort_keys=True,separators=(',',':'))})
 return out.getvalue()
