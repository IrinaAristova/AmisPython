input_file = 'Data\DisneylandParis.csv'
import re
import plotly
import plotly.graph_objs as go

def getFirstIndex(text, subs, start=0):
    result = -1
    for e in subs:
        ind = text.find(e, start)
        if (ind >= 0) and ((result < 0) or (ind < result)):
            result = ind
    return result

def getElement(line):
    start = 0
    while True:
        ind = getFirstIndex(line, [",", "\"", "\'"], start)
        if ind < 0:
            return line, ""
        elif line[ind] == ",":
            return line[:ind], line[ind+1:]
        else:
            nextind = line.find(line[ind], ind+1)
            if nextind < 0:
                return line, ""
            else:
                start = nextind+1
    return line, ""

def getUser(line):
    element, line = getElement(line)
    user_id = re.findall(r'\w+', element)
    return user_id[0], line

def getReview(line):
    element, line = getElement(line)
    return element, line

def getStars(line):
    element, line = getElement(line)
    stars = re.findall(r'\d+', element)
    return stars[0], line

def getDate(line):
    element, line = getElement(line)
    date = re.findall(r'\d{4}-\d{2}-\d{2}', element)
    return date[0], line

def addData(dataset, user_id, date, review, stars):
    if user_id not in dataset.keys():
        dataset[user_id] = dict()
    if date not in dataset[user_id].keys():
        dataset[user_id][date] = list()
    dataset[user_id][date].append({"review": review, "stars": stars})

def loadDataset(filename, max_line = 0):
    result = dict()
    with open(input_file, encoding="utf-8", mode='r') as file:
        file.readline()
        line_number = 0
        for line in file:
            line = line.strip().rstrip()
            if not line:
                continue

            user_id, line = getUser(line)
            review, line = getReview(line)
            stars, line = getStars(line)
            date, line = getDate(line)

            addData(result, user_id, date, review, stars)
            line_number += 1
            if line_number == max_line:
                break
    return result

def addDateCountReview(dct, date, count_review):
    if date in dct.keys():
        dct[date] += count_review
    else:
        dct[date] = count_review

def getDateReviews(dataset):
    result = dict()
    for user in dataset.keys():
        for date in dataset[user].keys():
            addDateCountReview(result, date, len(dataset[user][date]))
    return result

try:
    DS = loadDataset(input_file, 1000)
    for user in DS.keys():
        print(user)
        for date in DS[user]:
            for item in DS[user][date]:
                print("  [{0}] Stars: {1}, Review: {2}".format(date, item["stars"], item["review"]))
        break

    DR = getDateReviews(DS)
    x = list(DR.keys())
    y = list()
    for data in x:
        y.append(DR[data])
    pie = go.Pie(labels=x, values=y)
    plotly.offline.plot([pie], filename='pie6.html')

    bar = go.Bar(x=x, y=y)
    plotly.offline.plot([bar], filename='bar6.html')

    scatter = go.Scatter(x=x, y=y)
    plotly.offline.plot([scatter], filename='scatter6.html')

except IOError as e:
   print ("I/O error({0}): {1}".format(e.errno, e.strerror))

except ValueError as ve:
    print("Value error {0} in line {1}".format(ve, line_number))
