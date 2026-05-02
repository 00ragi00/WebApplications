import csv

sum_adult = 0.0
sum_pensioner = 0.0
sum_child = 0.0

with open('products.csv', 'r', encoding='utf-8') as f:
    r = csv.reader(f)
    next(r, None)
    
    for row in r:
        if row:
            sum_adult += float(row[1])
            sum_pensioner += float(row[2])
            sum_child += float(row[3])

print(f"{sum_adult:.2f} {sum_pensioner:.2f} {sum_child:.2f}")
