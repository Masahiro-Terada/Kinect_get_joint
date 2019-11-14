import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

class joint_graph_multi():
    def __init__(self, name, in_dir=os.getcwd(),  out_dir=os.getcwd()):
        if not os.path.exists(os.path.join(out_dir, 'knee')):
            os.mkdir(os.path.join(out_dir, 'knee'))
        if not os.path.exists(os.path.join(out_dir, 'underarm')):
            os.mkdir(os.path.join(out_dir, 'underarm'))
        self.out_file_knee = os.path.join(out_dir, 'knee', name.replace('.csv', '') + '_knee.png') #膝のグラフの出力ディレクトリ
        self.out_file_underarm = os.path.join(out_dir, 'underarm', name.replace('.csv', '') + '_underarm.png') #脇のグラフの出力ディレクトリ
        self.csv_file = os.path.join(in_dir, name) #入力CSVファイル
        df = pd.read_csv(self.csv_file)
        self.spinebase = df.iloc[:,0] #腰
        self.hip_x = df.iloc[:,1]  # 右尻
        self.hip_y = df.iloc[:,2]
        self.hip_z = df.iloc[:,3]
        self.knee_x = df.iloc[:,4]  # 右ひざ
        self.knee_y = df.iloc[:,5]
        self.knee_z = df.iloc[:,6]
        self.ankle_x = df.iloc[:,7]  # 右足首
        self.ankle_y = df.iloc[:,8]
        self.ankle_z = df.iloc[:,9]

        self.wrist_x = df.iloc[:,10]  # 右手首
        self.wrist_y = df.iloc[:,11]
        self.wrist_z = df.iloc[:,12]
        self.shoulder_x = df.iloc[:,13]  # 右肩
        self.shoulder_y = df.iloc[:,14]
        self.shoulder_z = df.iloc[:,15]

    def con(self):
        num = 15
        sm = np.ones(num) / num
        self.hip_x = np.convolve(self.hip_x, sm, mode='same')
        self.hip_y = np.convolve(self.hip_y, sm, mode='same')
        self.hip_z = np.convolve(self.hip_z, sm, mode='same')
        self.knee_x = np.convolve(self.knee_x, sm, mode='same')
        self.knee_y = np.convolve(self.knee_y, sm, mode='same')
        self.knee_z = np.convolve(self.knee_z, sm, mode='same')
        self.ankle_x = np.convolve(self.ankle_x, sm, mode='same')
        self.ankle_y = np.convolve(self.ankle_y, sm, mode='same')
        self.ankle_z = np.convolve(self.ankle_z, sm, mode='same')
        self.spinebase = np.convolve(self.spinebase, sm, mode='same')

        self.wrist_x = np.convolve(self.wrist_x, sm, mode='same')
        self.wrist_y = np.convolve(self.wrist_y, sm, mode='same')
        self.wrist_z = np.convolve(self.wrist_z, sm, mode='same')
        self.shoulder_x = np.convolve(self.shoulder_x, sm, mode='same')
        self.shoulder_y = np.convolve(self.shoulder_y, sm, mode='same')
        self.shoulder_z = np.convolve(self.shoulder_z, sm, mode='same')

        return self

    def knee_graph(self):
        titles = ['hip_x', 'hip_y', 'hip_z', 'knee_x', 'knee_y', 'knee_z',
                  'ankle_x', 'ankle_y', 'ankle_z', 'spinbase']
        datas = [self.hip_x, self.hip_y, self.hip_z, self.knee_x, self.knee_y, self.knee_z,
                 self.ankle_x, self.ankle_y, self.ankle_z, self.spinebase]

        plt.close('all')
        fig = plt.figure(figsize=(20, 16))
        plt.subplots_adjust(hspace=0.8)

        # グラフをプロット
        for i, data, title in zip(np.arange(1, 11), datas, titles):
            ax = fig.add_subplot(4, 3, i)
            ax.plot(data)
            ax.set_title(title)
            ax.set_xlabel('time')

        plt.savefig(self.out_file_knee)
        # plt.show()

    def underarm_graph(self):
        titles = ['wrist_x', 'wrist_y', 'wrist_z', 'shoulder_x', 'shoulder_y', 'shoulder_z',
                  'hip_x', 'hip_y', 'hip_z', 'hand']
        datas = [self.wrist_x, self.wrist_y, self.wrist_z, self.shoulder_x, self.shoulder_y, self.shoulder_z,
                 self.hip_x, self.hip_y, self.hip_z, self.wrist_y]

        plt.close('all')
        fig = plt.figure(figsize=(20, 16))
        plt.subplots_adjust(hspace=0.8)

        # グラフをプロット
        for i, data, title in zip(np.arange(1, 11), datas, titles):
            ax = fig.add_subplot(4, 3, i)
            ax.plot(data)
            ax.set_title(title)
            ax.set_xlabel('time')
        plt.savefig(self.out_file_underarm)

'''
if __name__ == '__main__':
    joint = joint_graph_multi('191112143944.csv')
    joint.con().knee_graph()
    joint.con().underarm_graph()

    file = os.listdir(os.path.join('up_down_org', 'jikken2b'))
    for i in file:
        print(i)
        joint = joint_graph_multi('up_down_org/jikken2b', i, 'up_down_output/graph_jikken2') #引数:入力ファイルのあるディレクトリ,入力ファイル名
        joint.con().knee_graph()
        joint.con().underarm_graph()
'''


