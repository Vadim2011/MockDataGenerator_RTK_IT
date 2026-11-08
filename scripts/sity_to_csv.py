
print('---------')
# PATH = r'../backend/test/list_city.txt'
# PATH_TO = r'../backend/test/list_city.csv'

# PATH = r'../backend/test/list_street.txt'
# PATH_TO = r'../backend/test/list_street.csv'

# PATH = r'../backend/test/list_f_name.txt'
# PATH_TO = r'../backend/test/list_f_name.csv'

# PATH = r'../backend/test/list_surname.txt'
# PATH_TO = r'../backend/test/list_surname.csv'

PATH = r'../backend/test/list_patronomic.txt'
PATH_TO = r'../backend/test/list_patronomic.csv'

with open(PATH,'r', encoding='utf-8') as f:
    data = f.read()

data_ls = data.split('\n')


res_data = []
# for i in data_ls:
#     if i and len(i) < 12:
#         res_data.append(i.title())

for i in range(0, len(data_ls), 4):
    if data_ls[i] == 'М':
        res_data.append(data_ls[i - 1].title())

res_data = "\n".join(res_data)

print(res_data[:100])

with open(PATH_TO,'w', encoding='utf-8') as f:
    f.write(res_data)

















