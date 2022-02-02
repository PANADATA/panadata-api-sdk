import requests
import unidecode
import random
import time
import os
import json
import sys
from multiprocessing import Pool
from difflib import SequenceMatcher
from panadata_api_sdk.csv import json_array_to_csv, csv_to_json_array

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

# adds fichas as calculated_ficha to each item of a json array
def append_fichas(json_array: list[dict]):
  try:
    for obj in json_array:
      obj['calculated_ficha'] = ruc_to_ficha(obj['input_ruc'])
    return json_array
  except Exception as e:
    raise Exception(e)

# simplify an organizations name for easier matching
def simplify_org_name(name: str):
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
    if(simple_name.endswith(ending)):
      simple_name = simple_name.removesuffix(ending)
  return simple_name.strip()

# adds a simplified organization name as simple_name to each item of a json array
def append_simple_names(json_array: list[dict]):
  try:
    for obj in json_array:
      obj['simple_name'] = simplify_org_name(obj['input_name'])
    return json_array
  except Exception as e:
    raise Exception(e)

# match an organization from a list with one from panadata by ficha
# the org must contain a field called input_name and another field called input_ruc
# the org can contain any other additional fields
def match_organization_ficha(org: dict):
  output_fields = ['ficha', 'ruc', 'nombre']
  results = api_request('organizations', org.get('calculated_ficha'))
  match = get_top_match(org, results['results'], 'input_name', 'nombre', .7)
  if match:
    for field in output_fields:
      org[f'panadata_{field}'] = match.get(field)
    org['ficha_match'] = True
    org['name_match'] = True
    org['ruc_match'] = get_ruc_match(org, .7)
    return org
  else:
    result_by_name = match_organization_name(org)
    return result_by_name

# match an organization from a list with one from panadata by ficha
# the org must contain a field called input_name and another field called input_ruc
# the org can contain any other additional fields
def match_organization_name(org:dict):
  output_fields = ['ficha', 'ruc', 'nombre']
  results = api_request('organizations', org.get('simple_name'))
  match = get_top_match(org, results['results'], 'input_name', 'nombre', .7, 'simple_name')
  if match:
    for field in output_fields:
      org[f'panadata_{field}'] = match.get(field)
    org['ficha_match'] = False
    org['name_match'] = True
    org['ruc_match'] = get_ruc_match(org, .7)
  else:
    org['ficha_match'] = False
    org['name_match'] = False
    org['ruc_match'] = False
  return org

# use multiprocessing to match multiple organizations in a list
# output_file, if provided, will save results to a json file with the given name. e.g. output -> output.json
def match_organizations(input_list: list[dict], output_fields: list[str], output_file=None):
  #output_field_list = [output_fields]*len(input_list)
  #print(output_field_list)
  initial_time = time.time()
  pool_processes = int(os.environ.get('PROCESSES'))
  with Pool(pool_processes) as p:
    # map should also contain array of output_fields
    results = p.map(match_organization_ficha, input_list)
  if output_file: 
    with open(f'{output_file}.json', "w") as f: json.dump(results, f)
  print('TOTAL TIME: ', time.time()-initial_time)
  return results

# make a request to the panadata API
def api_request(endpoint, query):
  with requests.Session() as s:
    r = s.get(f"https://panadata.net/api/v1/{endpoint}?query={query}", headers={'X-USER-TOKEN': os.environ.get('PANADATA_API_TOKEN')})
    print(r,r.elapsed.total_seconds())
    results = r.json() if r.status_code==200 else ['Error']
    return {'query': query, 'results': results}

# get the similarity ratio of two strings
def similar(a, b):
  return SequenceMatcher(None, a, b).ratio()

# Sort results from the panadata API by similarity to a given input field and get the result with the strongest match
# If a match_score param is specified, this method will only return if the top match has a higeher score than the match_score
# match_score should be a float number from 0 to 1
def get_top_match(item: dict, results: list[dict], input_field: str, panadata_field: str, match_score=0, includes=None) -> dict or None:
  def ratio(a, b):
    return similar(a.get(panadata_field), b.get(input_field))
  try:
    if len(results) > 0 and type(results[0]) is dict:
      sorted_results = sorted(results, key=lambda x: ratio(x, item), reverse=True)
      if includes and item[includes] in sorted_results[0][panadata_field].lower() or ratio(sorted_results[0], item) > match_score:
        return sorted_results[0]
      else:
        return None
    else:
      return None
  except Exception as e:
    raise Exception(e)

# get the similarity ratio of two RUCs
def get_ruc_match(org: dict, match_score:float):
  ratio = similar(str(org.get('panadata_ruc')), org.get('input_ruc')) if org.get('panadata_ruc') else 0
  result = True if ratio > match_score else False
  return result

# generates a CSV report that verifies information of a given organization (RUCs and names)
# input: a csv with the correct format that contains columns input_name and input_ruc plus any additional columns
# output: a csv with the input and output rucs/names/fichas and a match score
def organization_matches_report(input_csv, output_csv):
  json_array = csv_to_json_array(f'{input_csv}.csv')
  with_simple_names = append_simple_names(json_array)
  with_fichas = append_fichas(with_simple_names)
  json_results = match_organizations(with_fichas, ['ficha', 'ruc', 'nombre'], 'results')
  json_array_to_csv(json_results, output_csv)
  return json_results
