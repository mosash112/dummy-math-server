from math import *

def function_creator(expr):
    # expr = expr.replace(" ","")
    try:
        y = round(eval(expr, {}, safe_dict),2)
    except Exception:
        y = "Error"
    return y

safe_list = ['acos', 'asin', 'atan', 'atan2', 'ceil', 'cos',
                 'cosh', 'degrees', 'e', 'exp', 'fabs', 'floor',
                 'fmod', 'frexp', 'hypot', 'ldexp', 'log', 'log10',
                 'modf', 'pi', 'pow', 'radians', 'sin', 'sinh', 'sqrt',
                 'tan', 'tanh']
 
# creating a dictionary of safe methods
safe_dict = {}
for safe_key in safe_list:
    safe_dict[safe_key] = locals().get(safe_key)