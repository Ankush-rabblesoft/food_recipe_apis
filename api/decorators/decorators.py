
from functools import wraps
import json


def auth_api(f):
    @wraps(f)
    def wrap(request, *args, **kwargs):
        
        if request.body: 
            try:
               request.json = json.loads(request.body)
            except:
                request.json = None
                
        return f(request, *args, **kwargs)
    return wrap
    
 