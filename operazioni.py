import re
import random
import sys

random_n = r"r\s*\(\s*\d*\s*-\s*\d*\s*\)"
operation_r = r"\[[\+x\-\:\s]*\]"
max_r = r"max\s*\(([^,]*)\,\s*(\d+)\s*\)"
min_r = r"min\s*\(([^,]*)\,\s*(\d+)\s*\)"

operation_syn = [["x","*"],[":","/"]]
incremental_flag =1

def is_k(op, bound):
  lb, ob = bound
  for a,b in operation_syn:
    op = op.replace(a,b)
  op = re.sub(r"\d+",put_dot_zero,op)
  res = eval(op)
  lb = (int(lb if lb is not None else 0) <=int(res) if lb is not None else True)
  ob = (int(res) <=int(ob if ob is not None else 0) if ob is not None else True)
  return lb and ob

def incremental_I(m):
  global incremental_flag
  incremental_flag+=1
  return incremental_flag

def gen_op(m):
  ops = m.group(0).replace(" ", "").replace("[","").replace("]","")
  tot = len(ops)
  return ops[random.randint(0,tot-1)]

def put_dot_zero(m):
  return m.group(0) + ".0"

def get_r_n(m):
  bounds = m.group(0).replace("r", "random.randint").replace("-",",")
  n = eval(bounds)
  return str(n)
  
def put_numbers(operation):
  global random_n
  return re.sub(random_n,get_r_n,operation)

def put_op(operation):
  global operation_r
  return re.sub(operation_r, gen_op, operation)

def get_upper_bound(operation):
  global max_r
  mtch = re.search(max_r, operation)
  if mtch == None:
    return None
  else:
    return mtch.group(2)

def get_lower_bound(operation):
  global min_r
  mtch = re.search(min_r, operation)
  if mtch == None:
    return None
  else:
    return mtch.group(2)

def remove_ub(operation):
  global max_r
  return re.sub(max_r, remove_ptn_ublb, operation)

def remove_lb(operation):
  global min_r
  return re.sub(min_r, remove_ptn_ublb,operation)
  
def remove_ptn_ublb(m):
  return m.group(1)

def gen_operazione(operation):
  global max_r
  global min_r
  with_n = put_numbers(operation)
  with_n = put_op(with_n)
  max, min = None, None
  max_index = [x.start() for x in re.finditer(max_r,with_n)]
  min_index = [x.start() for x in re.finditer(min_r,with_n)]
  if len(max_index) is not 0 and len(min_index) is not 0:
    if max_index[0] > min_index[0]: #minindex contains maxindex
      max = get_upper_bound(with_n)
      with_n = remove_ub(with_n)
      min = get_lower_bound(with_n)
      with_n = remove_lb(with_n)
    else:
      min = get_lower_bound(with_n)
      with_n = remove_lb(with_n)
      max = get_upper_bound(with_n)
      with_n = remove_ub(with_n)
  elif len(max_index) is not 0:
    max = get_upper_bound(with_n)
    with_n = remove_ub(with_n)
  elif len(min_index) is not 0:
    min = get_lower_bound(with_n)
    with_n = remove_lb(with_n)
  return with_n, max, min

def gen_op_bound(operation):
  with_n, max, min = gen_operazione(operation)
  while not(is_k(with_n,(min,max))):
    with_n, max, min = gen_operazione(operation)
  return with_n
  
def generate(operation):
  return gen_op_bound(operation)
  


