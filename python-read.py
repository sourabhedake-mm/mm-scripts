import csv
file = open("states.csv")
csvreader = csv.reader(file)
rows = []
for row in csvreader:
    rows.append(row)
file.close()

final = []
skip = 0
temprow = []
schools = {}
for x in rows:
    temprow = x
    while("" in temprow) :
        temprow.remove("")
    if len(temprow) >= 1 and str(x[0]).isdigit():
        skip = 0
        state = temprow[1] if temprow[1] != "" else temprow[2]
        district = temprow[2] if temprow[2] != "" else temprow[3]
        school = temprow[-1]
        if state not in schools:
            schools[state] = []
        if school not in schools[state]:
            final.append([state, district, school])
            schools[state].append(school)
        else:
            print("skipping ", school, state)
        temprow = x
    else:
        skip = 1
    # if (skip):
    #     if len(temprow)>=4 and x[4].strip() != "":
    #         temprow[4] = temprow[4] + " " + x[4]
    #     if len(temprow)>=4 and x[0].strip() != "":
    #         temprow[4] = temprow[4] + " " + x[0].strip()
    #     if len(temprow)>=4 and x[1].strip() != "":
    #         temprow[4] = temprow[4] + " " + x[1].strip()

# final.append(temprow)

# print (final)

filename = 'state-filtered.csv'
with open(filename, 'w', newline="") as file:
    csvwriter = csv.writer(file) # 2. create a csvwriter object
    csvwriter.writerows(final) # 5. write the rest of the data