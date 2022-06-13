def make_divider_of(divider):
    def division_operation(divisible):
        return divisible / divider
    return division_operation


# Создали функцию с параметром divider
div2 = make_divider_of(2)
# Вызвали созданную функцию, передав в нее 10
print(div2(10))
# Выведет: 5.0

div5 = make_divider_of(5)
print(div5(20))
# Выведет: 4.0

print(div5(div2(20)))
# Выведет: 2.0
