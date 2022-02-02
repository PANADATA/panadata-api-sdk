# generate a random cedula
def gen_cedula():
  a = random.randrange(1, 13)
  b = random.randrange(111, 999)
  c = random.randrange(1111, 9999)
  ini = random.choices([str(a), 'P', 'PE', 'E', 'N', '1AV', '1PL'])
  cedula = '-'.join([ini[0], str(b), str(c)])
  return cedula

# generate n random cedulas
def gen_cedulas(n):
  arr = []
  i = 1
  while i < n:
    arr.append(generate_cedula())
    i+=1

# generate a random ruc
def gen_ruc():
  a = random.randrange(111111111, 999999999)
  b = random.randrange(2, 3)
  c = random.randrange(2000, 2021)
  dv = random.randrange(10, 29)
  ruc = '-'.join([str(a), str(b), str(c)])
  ruc = f"{ruc} DV {dv}"
  return ruc

# generate n random rucs and encode as urls
def gen_rucs(n):
  arr = []
  i = 1
  while i < n:
    ruc = generate_ruc()
    arr.append(to_url(ruc))
    i+=1
  arr.append(to_url('155667546-2-2018 DV 17'))
  return arr