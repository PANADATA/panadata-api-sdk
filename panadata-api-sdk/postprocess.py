from difflib import SequenceMatcher

def similar(a, b):
  return SequenceMatcher(None, a, b).ratio()

# get result with the strongest match for ruc
def get_ruc_match(val, arr):
  print('GETTING RUC MATCH')
  print(val)
  print(arr)
  def ratio(a, q):
    print(str(a.get('ruc')))
    print(q.get('input_ruc'))
    return similar(str(a.get('ruc')), q.get('input_ruc')) if a.get('ruc') else 0
  sorted_results = sorted(arr, key=lambda x: ratio(x, val), reverse=True)
  print(sorted_results)
  print(ratio(sorted_results[0], val))
  result = sorted_results[0] if ratio(sorted_results[0], val) > 0.7 else get_results_by_name(val)
  return result

# get result with the strongest match for name
def get_results_by_name(item):
  def ratio(a, q):
    print(str(a.get('ruc')))
    print(q.get('input_ruc'))
    return similar(str(a.get('nombre')), q.get('input_nombre'))
  response = req(simplify(item.get('input_nombre')))
  print('\n\nRESPONSE\n\n',response)
  sorted_results = sorted(response['results'], key=lambda x: ratio(x, item), reverse=True)
  #print(sorted_results)
  print(ratio(sorted_results[0], item))
  result = sorted_results[0] if ratio(sorted_results[0], item) > 0.6 else empty_response
  return result

# merges input and output values. selects the most similar result to the input
def join_jsons():
  def ratio(a, q):
    return similar(a.get('nombre'), q.get('input_nombre'))

  inputs_txt = open("input.json", "r")
  inputs = json.load(inputs_txt)

  res_txt = open("response.json", "r")
  res = json.load(res_txt)

  united_res = []
  for index, val in enumerate(inputs) :
    united_json = {}

    #sort results by their similarity to the input name
    if len(res[index]["results"]) > 0 and type(res[index]["results"][0]) is dict:
      sorted_results = sorted(res[index]['results'], key=lambda x: ratio(x, val), reverse=True)
      print('\n\n------------------')
      print(sorted_results[0])
      print(val)
      print(ratio(sorted_results[0], val))
      print('------------------\n\n')
      results = sorted_results[0] if ratio(sorted_results[0], val) > .6 else get_ruc_match(val, res[index]['results'])
    else:
      results = empty_response
    
    print(inputs[index])
    for attr, val in inputs[index].items():
      united_json[attr] = val
    print(results)
    for attr, val in results.items():
      united_json[attr] = val
    united_res.append(united_json)

  with open("results.json", "w") as f:
    json.dump(united_res, f)