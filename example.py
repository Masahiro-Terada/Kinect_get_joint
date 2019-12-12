from jointgetter.io import KinectJson2CSV,Csv2graph

name = 'sample'
jtc = KinectJson2CSV()
jtc(name + '.json')

ctg = Csv2graph()
ctg.load_csv(name+'.csv')
ctg.make_graph([3,6,9])
ctg.to_image()

