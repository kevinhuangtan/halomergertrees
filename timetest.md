===================== 10e4 lines

timeit.timeit("a=myReader.RockstarReader('10000.txt')", setup ='import myReader', number = 1)

time: 0.2405529022216797

timeit.timeit("a=myReaderAppend.RockstarReader('10000.txt')", setup ='import myReaderAppend', number = 1)

time: 0.8121211528778076

timeit.timeit("a=asciiReader.RockstarReader('ignore/10000.txt','10000')", setup='import asciiReader', number = 1)

time: 0.9663569927215576

===================== 10e5 lines

timeit.timeit("a=myReader.RockstarReader('100000.txt')", setup ='import myReader', number = 1)

time: 2.4515230655670166

timeit.timeit("a=myReaderAppend.RockstarReader('100000.txt')", setup ='import myReaderAppend', number = 1)

time: 2.215717077255249

timeit.timeit("a=asciiReader.RockstarReader('ignore/100000.txt','100000')", setup='import asciiReader', number = 1)

time: 3.9527878761291504

===================== 10e6 lines

timeit.timeit("a=myReader.RockstarReader('1000000.txt')", setup ='import myReader', number = 1)

time: 20.84416890144348

timeit.timeit("a=myReaderAppend.RockstarReader('1000000.txt')", setup ='import myReaderAppend', number = 1)

time: 16.749769926071167

timeit.timeit("a=asciiReader.RockstarReader('ignore/1000000.txt','1000000')", setup='import asciiReader', number = 1)

time: 38.153778076171875

========================= 5000000 lines

timeit.timeit("a=asciiReader.RockstarReader('ignore/5000000.txt','5000000')", setup ='import asciiReader', number = 1)

time: 285.5777151584625

=====================


timeit.timeit("a=myReader.RockstarReader('10000000.txt')", setup ='import myReader', number = 1)

time: 1424.99400806427

timeit.timeit("a=myReaderAppend.RockstarReader('10000000.txt')", setup ='import myReaderAppend', number = 1)

time: 1384.1994287967682


