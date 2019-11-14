from json_to_csv import json_to_csv
from graph5b_ver2 import joint_graph_multi

if __name__ == '__main__':
    name = 'sample'
    jtc = json_to_csv()
    jtc.csv(name + '.json')
