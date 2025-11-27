# 1. add shopping dictionary (user_id -> category)
purchases = {}

with open('purchase_log.csv', encoding='utf-8') as f:
    next(f)
    for line in f:
        line = line.strip()
        if not line:
            continue
        parts = line.split(',')
        user_id = parts[0]
        category = parts[1]
        purchases[user_id] = category

# 2. read visit_log.csv for lines and write to  funnel.csv
with open('visit_log.csv', encoding='utf-8') as visit_file, \
     open('funnel.csv', 'w', encoding='utf-8') as funnel_file:

    header = 'user_id,source,category'
    funnel_file.write(header + '\n')
    print(header)

    next(visit_file)  # skip header

    # counter for first 3 lines
    max_print = 3
    count_printed = 0

    for line in visit_file:
        line = line.strip()
        if not line:
            continue

        parts = line.split(',')
        user_id = parts[0]
        source = parts[1]

        if user_id in purchases:
            category = purchases[user_id]
            row = f'{user_id},{source},{category}'
            funnel_file.write(row + '\n')

            # print first 3 lines
            if count_printed < max_print:
                print(row)
                count_printed += 1
# compare user_id in  visit_log.csv and purchase_log.csv
matches = 0
for user_id in purchases:
    if user_id in [line.split(',')[0] for line in open('visit_log.csv', encoding='utf-8')]:
        matches += 1

print("Количество совпадающих user_id:", matches)
