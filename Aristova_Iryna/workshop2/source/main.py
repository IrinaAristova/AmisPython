"""
Функція getBrand(smth) виводить brand авто з найбільшою
кількістю власників.
"""
def getBrand(smth, index = 0, maximum = 0, brand = ''):
    if index < len(smth):
        num = len(smth[index]['owners'])
        if num > maximum:
            return getBrand(smth, index+1, num, smth[index]['brand'])
        else:
            return getBrand(smth, index+1, maximum, brand)
    else:
        return brand

"""
Функція addOwner(smth, name) додає до авто з брендом brand
нового власника з іменем name.
"""
def addOwner(smth, name, brand):
    for i in smth:
        if(i['brand'] == brand):
            owner_list=i['owners']
            owner_list.update({name})
    return owner_list

"""
Функція getNames(smth) повертає множину усых власників усіх автомобілів.
"""
def getNames(smth):
    names=set({})
    for j in smth:
        names.update(j['owners'])
    return names



smth=[
      {
       'brand': 'Ford',
       'model': 'Mustang',
       'year': 1964,
       'owners': {
                  'Bob',
                  'Boba'
                 }
      },
      {
       'brand': 'Mers',
       'model': 'C500',
       'year': 2000,
       'owners': {
                  'Bob'
                 }
      },
      {
       'brand': 'Wolksvagen',
       'model': 'Polo',
       'year': 2002,
       'owners': {}
      }
     ]

print(getBrand(smth))

print(addOwner(smth, 'Boban', 'Mers'))

print(getNames(smth))
