#people = {'hello': {0:{'text':'good morning'},1:{'text':'good evening'}},'not_hello': {0:{'text':'not morning'},1:{'text':'not evening'}}}
people = {'hello': {0:{'text':'good morning'}}}
#if hello not exist
    #people.update({'hello':{0:{'text':'good morning'}}})
#if hello exist 
    #hello_count = len(people['hello'])
    #people['hello'].update({len(people['hello'])+1:{'text':'good evening'}})

print(people['hello'])
print(type(people['hello']))
print(people['hello'][0])
print(type(people['hello'][0]))
for key1,value1 in people.items():
    aList = []
    for key2,value2 in value1.items():
        print(key2)
        print(value2)
        aList.append(value2)
    print(aList)
    print(type(aList))