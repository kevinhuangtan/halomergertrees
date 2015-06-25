GET TRUNK
%timeit treeCrawler.getTrunkTable(3061006267, 'sorted.hdf5')
100 loops, best of 3: 5.23 ms per loop

CLUMPY ACCRETION
%timeit treeCrawler.clumpy_accretion(3061006267, 'sorted.hdf5')
1 loops, best of 3: 25.6 ms per loop

SMOOTH ACCRETION
%timeit treeCrawler.smooth_accretion(3061006267, 'sorted.hdf5')
1 loops, best of 3: 30.7 ms per loop


ASCIIREADER

===================== 10e3 lines

timeit.timeit("a=myReader.RockstarReader('10000.txt')", setup ='import myReader', number = 1)

time: 0.2405529022216797

timeit.timeit("a=asciiReaderOld.RockstarReader('10000.txt')", setup ='import asciiReaderOld', number = 1)

time: 0.8121211528778076

timeit.timeit("a=asciiReader.RockstarReader('ignore/10000.txt','10000')", setup='import asciiReader', number = 1)

time: 0.9663569927215576

===================== 10e4 lines

timeit.timeit("a=asciiReaderOld.RockstarReader('100000.txt')", setup ='import asciiReaderOld', number = 1)

time: 2.215717077255249

timeit.timeit("a=asciiReader.RockstarReader('ignore/100000.txt','100000')", setup='import asciiReader', number = 1)

time: 3.9527878761291504

===================== 10e5 lines

timeit.timeit("a=asciiReaderOld.RockstarReader('1000000.txt')", setup ='import asciiReaderOld', number = 1)

time: 16.749769926071167

timeit.timeit("a=asciiReader.RockstarReader('ignore/1000000.txt','1000000')", setup='import asciiReader', number = 1)

time: 38.153778076171875

========================= 5e6 lines

timeit.timeit("a=asciiReader.RockstarReader('ignore/5000000.dat','5000000')", setup ='import asciiReader', number = 1)

time: 285.5777151584625

===================== 10e6 lines

timeit.timeit("a=asciiReaderOld.RockstarReader('10000000.txt')", setup ='import asciiReaderOld', number = 1)

time: 1384.1994287967682

timeit.timeit("a=asciiReader.RockstarReader('ignore/10000000.txt','10000000')", setup ='import asciiReader', number = 1)

time: 732.5528337955475

===================== 

timeit.timeit("a=asciiReader.RockstarReader('ignore/tree_0_2_2.dat','tree_0_2_2')", setup ='import asciiReader', number = 1)

RuntimeError: Unable to register datatype atom (Can't insert duplicate key)

