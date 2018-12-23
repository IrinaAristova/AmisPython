import plotly
import plotly.graph_objs as go


def AddRecord(dataset, lst):
    if len(lst) >= 2:
        key = lst[0].strip()
        if len(lst) == 2:
            dataset.append({'quantity': float(key), 'price': float(lst[1].strip())})
        elif key in dataset.keys():
            AddRecord(dataset[key], lst[1:])
        else:
            if len(lst) == 3:
                dataset[key] = list()
            else:
                dataset[key] = dict()
            AddRecord(dataset[key], lst[1:])

def AddItem(dataset, user, date, product, quantity, price):
    AddRecord(dataset, [user, date, product, quantity, price])
    
def OpenDataSet(FileName):
    result = dict()
    file = open(FileName, encoding='utf-8')
    lst = file.read().splitlines()
    file.close()
    for i in range(1, len(lst)):
        s = lst[i].split(",")
        AddRecord(result, s)
    return result

def GetProductOfUser(userdataset):
    result = list()
    for datekey in userdataset.keys():
        result += list(userdataset[datekey].keys())
    return list(set(result))
    
def GetProductForAllUsers(dataset):
    result = list()
    first = True
    for user in dataset.keys():
        spisok = GetProductOfUser(dataset[user])
        if first:
            result += spisok
            first = False
        else:
            for item in result:
                  if item not in spisok:
                    result.remove(item)
    return result

def GetProductDatePrice(dataset, product):
    result = dict()
    for user in dataset.keys():
        for datekey in dataset[user].keys():
            if product in dataset[user][datekey]:
                result[datekey] = dataset[user][datekey][product][0]['price']
    return result

def GetUserMoney(dataset):
    result = dict()
    for user in dataset.keys():
        money = 0.0
        for datekey in dataset[user].keys():
            for product in dataset[user][datekey].keys():
                for item in dataset[user][datekey][product]: 
                    money += item['price']*item['quantity']
        result[user] = money
    return result

def GetPopularProduct(dataset):
    result = dict()
    maxmoney = 0.0
    maxproduct = "none"
    for user in dataset.keys():
        for datekey in dataset[user].keys():
            for product in dataset[user][datekey].keys():
                money = 0.0
                for item in dataset[user][datekey][product]: 
                    money = item['price']*item['quantity']
                if product in result:
                    result[product] += money
                else:
                    result[product] = money
                if result[product] > maxmoney:
                    maxmoney = result[product]
                    maxproduct = product
    return maxproduct

def GetMinimumProduct(dataset):
    result = dict()
    for user in dataset.keys():
        for datekey in dataset[user].keys():
            for product in dataset[user][datekey].keys():
                cnt = 0.0
                for item in dataset[user][datekey][product]:
                    cnt += item['quantity']
                if product in result:
                    result[product] += cnt
                else:
                    result[product] = cnt
    minproduct = "none"
    mincnt = 0.0
    first = True
    for product in result.keys():
        if first:
            first = False
            mincnt = result[product]
            minproduct = product
        elif result[product] < mincnt:
            mincnt = result[product]
            minproduct = product
    return minproduct
    

def GetBiggestCostProduct(dataset):
    maxmoney = 0.0
    maxproduct = "none"
    for user in dataset.keys():
        for datekey in dataset[user].keys():
            for product in dataset[user][datekey].keys():
                money = dataset[user][datekey][product][0]['price']
                if money > maxmoney:
                    maxmoney = money
                    maxproduct = product
    return maxproduct

def getProductClients(dataset):
    result = dict()
    for user in dataset.keys():
        for date in dataset[user].keys():
            for product in dataset[user][date].keys():
                if product in result.keys():
                    result[product] += [user]
                else:
                    result[product] = [user]
    return result

DS = OpenDataSet("Data\orders.csv")

for user in DS.keys():
    print(user, GetProductOfUser(DS[user]))

print("For all users ", GetProductForAllUsers(DS))
print("Price for apple ", GetProductDatePrice(DS, "apple"))
print("Money of users ", GetUserMoney(DS))
print("Popular product =", GetPopularProduct(DS))
print("Minimal buy product =", GetMinimumProduct(DS))
print("Big cost product =", GetBiggestCostProduct(DS))

priceapple = GetProductDatePrice(DS, "apple")
x = list(priceapple.keys())
x.sort()
y = list()
for date in x:
    y.append(priceapple[date])
scatter = go.Scatter(x=x, y=y)
plotly.offline.plot([scatter], filename='scatter5.html')

usermoney = GetUserMoney(DS)
x = list(usermoney.keys())
y = list()
for user in x:
    y.append(usermoney[user])
bar = go.Bar(x=x, y=y)
plotly.offline.plot([bar], filename='bar5.html')

productclients = getProductClients(DS)
x = list(productclients.keys())
y = list()
for product in x:
    y.append(len(set(productclients[product])))
pie = go.Pie(labels=x, values=y)
plotly.offline.plot([pie], filename='pie5.html')

