# convert RUCs into fichas
def ruc_to_ficha(ruc):
  new_ruc_years = [
    '2014',
    '2015',
    '2016',
    '2017',
    '2018',
    '2019',
    '2020',
    '2021'
  ]
  if(len(ruc) > 1):
    if 'DV' in ruc: ruc = ruc.split('DV')[0]
    ruc_slice=ruc.strip().split('-')
    if len(ruc_slice) > 2:
      return ruc_slice[0] if ruc_slice[2] in new_ruc_years else ruc_slice[2]
    else:
      return ruc
  else:
    return ''

# simplify an organizations name for easier matching
def simplify_org_name(name):
  endings = [
    'sa',
    's a',
    'inc',
    'corp',
    'co',
    'ltd',
    'llc',
    'corporation'
  ]
  simple_name = name.strip().lower().replace(',', '').replace('.', '').replace('-', '').replace('&', '')
  for ending in endings :
    print(ending, '-', simple_name)
    if(simple_name.endswith(ending)):
      simple_name = simple_name.removesuffix(ending)
  return simple_name