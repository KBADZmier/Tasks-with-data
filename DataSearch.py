import json
def ConvertToJson():
    filename = 'energia.txt'

    dict1 = {}
    fields = ['Data', 'Godzina', 'Zrodla_wiatrowe', 'Zrodla_fotowoltaiczne']
    with open(filename) as fh:
        l = 1
    for line in fh:
        description = list(line.strip().split(None, 4))
        print(description) 
        sno = 'energia' + str(l)
        i = 0
       
        dict2 = {}
        while i < len(fields):
            dict2[fields[i]] = description[i]
            i = i + 1
                
        dict1[sno] = dict2
        l = l + 1
      
    out_file = open("test2.json", "w")
    json.dump(dict1, out_file, indent=4)
    out_file.close()

ConvertToJson()