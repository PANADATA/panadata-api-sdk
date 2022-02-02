import csv

def csv_to_json_array(filename):
  json_array = []
  with open(filename, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
      json_array.append(row)
  return json_array

def json_array_to_csv(json_array: list[dict], output_file='results'):
  def getKeysLength(e):
    return len(e.keys())
  try:
    json_array.sort(key=getKeysLength, reverse=True)
    csv_columns = list(json_array[0].keys())
    with open(f'{output_file}.csv', 'w') as csvfile:
      writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
      writer.writeheader()
      for data in json_array:
        writer.writerow(data)
  except Exception as e:
    raise Exception(e)

  