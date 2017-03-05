import re
import random

random_n = r"r\s*\(\s*\d*\s*-\s*\d*\s*\)"
operation_r = r"\[[\+x\-\:\s]*\]"
max_r = r"max\s*\(([^,]*),\s*(\d+)\s*\)"
min_r = r"min\s*\([^,]*,\s*(\d+)\s*\)"

operation_syn = [["x","*"],[":","/"]]
incremental_flag =1

def is_k(op, bound):
  lb, ob = bound
  for a,b in operation_syn:
    op = op.replace(a,b)
  op = re.sub("\\d*",put_dot_zero,op)
  res = eval(op)
  return lb <= res <=ob

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
  mtch = re.match(max_r, operation)
  if mtch == None:
    return None
  else:
    return mtch.group(2)

def get_lower_bound(operation):
  global min_r
  mtch = re.match(min_r, operation)
  if mtch == None:
    return None
  else:
    return mtch.group(2)

def remove_ub(operation):
  global max_r
  return re.match(max_r, operation).group(1)

def gen_operazione(operation):
  with_n = put_numbers("max(r(0-13) [ + -x :] r(30-40 ),10)")
  with_n = put_op(with_n)
  lower_bound = None
  upper_bound = get_upper_bound(with_n)
  if upper_bound is None:
	lower_bound = get_lower_bound(with_n)
  else:
    with_n = remove_ub(with_n)
  if lower_bound
  


gen_operazione("")







