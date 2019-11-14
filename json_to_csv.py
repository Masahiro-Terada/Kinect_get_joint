import pandas as pd
import os
import numpy as np

class json_to_csv():
    def __init__(self):
        self.spinebases = []
        self.hips = []
        self.knees = []
        self.ankles = []
        self.wrists = []
        self.shoulders = []


    def csv(self, name, in_dir=os.getcwd(), out_dir=os.getcwd()):
        df = pd.read_json(os.path.join(in_dir,name), lines=True)
        for i in range(len(df)):
            data = df.iloc[i,15]
            data_hip = data['HipRight']['Position']
            data_knee = data['KneeRight']['Position']
            data_ankle = data['AnkleRight']['Position']
            data_wrist = data['WristRight']['Position']
            data_shoulder = data['ShoulderRight']['Position']

            self.spinebases.append([data['SpineBase']['Position']['Y']])
            self.hips.append([data_hip['X'], data_hip['Y'], data_hip['Z']])
            self.knees.append([data_knee['X'], data_knee['Y'], data_knee['Z']])
            self.ankles.append([data_ankle['X'], data_ankle['Y'], data_ankle['Z']])
            self.wrists.append([data_wrist['X'], data_wrist['Y'], data_wrist['Z']])
            self.shoulders.append([data_shoulder['X'], data_shoulder['Y'], data_shoulder['Z']])
        out_df = pd.DataFrame(np.array(self.spinebases), columns=['SpineBase'])
        out_df = out_df.assign(hip_x= np.array(self.hips)[:,0], hip_y=np.array(self.hips)[:,1], hip_z=np.array(self.hips)[:,2],
                               knee_x=np.array(self.knees)[:,0], knee_y=np.array(self.knees)[:,1], knee_z=np.array(self.knees)[:,2],
                               ankle_x=np.array(self.ankles)[:,0], ankle_y=np.array(self.ankles)[:,1], ankle_z=np.array(self.ankles)[:,2],
                               wrist_x=np.array(self.wrists)[:,0], wrist_y=np.array(self.wrists)[:,1], wrist_z=np.array(self.wrists)[:,2],
                               shoulder_x=np.array(self.shoulders)[:,0], shoulder_y=np.array(self.shoulders)[:,1], shoulder_z=np.array(self.shoulders)[:,2]
                               )
        out_df = out_df.assign(time=df.iloc[:,16])
        out_df.to_csv(os.path.join(out_dir,name.replace('.json', '.csv')), header=False, index=False)

'''
if __name__ == '__main__':
    in_dir = 'up_down_json'
    out_dir = 'up_down_org/jikken2b'
    jtc = json_to_csv()
    jtc.csv('191112143944.json')
    
    files = os.listdir(in_dir)
    for file in files:
        print(file)
        to_csv(in_dir, file, out_dir)
'''