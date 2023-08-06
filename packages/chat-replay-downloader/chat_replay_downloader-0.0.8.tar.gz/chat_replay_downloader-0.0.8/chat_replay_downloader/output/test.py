from continuous_write import ContinuousWriter
# from output.continuous_write import JSONCW
# from output.continuous_write import CSVCW

#f = ContinuousWriter('')
f_name = 'test.csv' # 'test.csv'

params = {
    'indent':4,
    'sort_keys':True
}

f = ContinuousWriter(f_name, **params)
#print(f)
d = {'e': True, 'c': 'd'}
f.write(d)

for i in range(5):
    d = {str(i): i, 'c': True}
    f.write(d)


f.close()





exit()
json_test_file_name = 'test.json'
json_test = JSONCW(json_test_file_name)

csv_test_file_name = 'test.csv'
csv_test = CSVCW(csv_test_file_name)

for i in range(5):

    print('write', d)
    json_test.write(d)
    csv_test.write(d)

    # add_to_json(d, fname, indent=4)  # , indentation_char='\t'
q = {'a': 1, 'b': True}
json_test.write(q)
csv_test.write(q)

for i in range(5):
    d = {'a': 'b', 'c': 'd'}
    print('write', d)
    json_test.write(d)
    csv_test.write(d)
# with JSONCW('test2.json') as f:
# 	print(f)
# 	f.write({'a':1,'b':True})


json_test.close()
csv_test.close()
# import output
