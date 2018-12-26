import math

grad_mods = (180/math.pi, 60, 60)
grad_names = ("гр.", "хв.", "сек.")
'''
Переведення радіанної міри кута в градуси, хвилини, секунди 
'''
def get_grad(rad, index = 0):
    if index < len(grad_mods):
        value = rad*grad_mods[index]
        result = int(value)
        return " {0} {1}{2}".format(result, grad_names[index], get_grad(value-result, index+1))
    else:
        return ""

'''
Введення трьох дійсних чисел та піднесення до квадрата невід'ємних та у четверту ступінь - від'ємних 
'''
def get_nums(index=0):
    if index < 3:
        value = float(input("Введіть {0} число ".format(index+1)))
        if (value < 0):
            result = value**4
        else:
            result = value**2
        if index > 0:
            delim = ", "
        else:
            delim = ""
        return "%s%.3f%s"%(delim, result, get_nums(index+1))
    else:
        return ""

Rad = float(input("Введіть радіанну міру кута "))
print("Значення кута{0}".format(get_grad(Rad)))

print(get_nums())