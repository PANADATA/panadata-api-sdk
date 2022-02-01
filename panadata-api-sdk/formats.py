# convert csv into json
def csv_to_json():
  res = []
  csv = open("input.csv", "r")
  lines = csv.readlines()
  for line in lines:
    j = line.replace('\n','').rsplit(',', 1)
    res.append({'input_nombre': j[0].replace('"', ''), 'input_ruc': j[1]})
  with open("input.json", "w") as f:
    json.dump(res, f)

# convert output json into csv
def to_csv():
  res_txt = open("results.json", "r")
  res = json.load(res_txt)
  csv = ''

  for attr, value in empty_output.items():
    csv += f"{attr},"
  csv += "\n"

  for item in res:
    row = ""
    for attr, val in item.items():
      row += f'"{val}",'
    row+='\n'
    csv+=row

  f = open("results.csv", "w")
  f.write(csv)