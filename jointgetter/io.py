import os
import numpy as np
import pandas as pd


class KinectJson2CSV(object):
    """

    Examples::
        >>> j2c = KinectJson2CSV()
        >>> j2c("some.csv", "in_dir", "out_dir")
        >>> # or
        >>> j2c.load_json("some.csv")
        >>> j2c.organize()
        >>> j2c.to_csv()
        >>> j2c.clear_buffer()
    """
    def __init__(self):
        self.spinebases = []
        self.hips = []
        self.knees = []
        self.ankles = []
        self.wrists = []
        self.shoulders = []

        self.out_df = None
        self.name = None
        self.df = None

    def load_json(self, name: str, in_dir: str = None) -> None:
        """
        指定したJSONファイルを読み込みます。
        in_dir に何も指定しない場合は自動的にカレントディレクトリが指定されます。

        Args:
            name: ファイル名。 str
            in_dir: 引数1で指定したファイルが格納されているディレクトリのパス。 指定しなかった場合、プログラムのカレントディレクトリ。

        """
        if in_dir is None:
            in_dir = os.getcwd()

        self.name = name
        self.df = pd.read_json(os.path.join(in_dir, name), lines=True)

    def organize(self) -> None:
        """
        読み込んだJSONファイルを整理します。

        """
        for i in range(len(self.df)):
            data = self.df.iloc[i, 15]
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

        self.out_df = pd.DataFrame(np.array(self.spinebases), columns=['SpineBase'])
        self.out_df = self.out_df.assign(
            hip_x=np.array(self.hips)[:, 0], hip_y=np.array(self.hips)[:, 1], hip_z=np.array(self.hips)[:, 2],
            knee_x=np.array(self.knees)[:, 0], knee_y=np.array(self.knees)[:, 1], knee_z=np.array(self.knees)[:, 2],
            ankle_x=np.array(self.ankles)[:, 0], ankle_y=np.array(self.ankles)[:, 1], ankle_z=np.array(self.ankles)[:, 2],
            wrist_x=np.array(self.wrists)[:, 0], wrist_y=np.array(self.wrists)[:, 1], wrist_z=np.array(self.wrists)[:, 2],
            shoulder_x=np.array(self.shoulders)[:, 0], shoulder_y=np.array(self.shoulders)[:, 1], shoulder_z=np.array(self.shoulders)[:, 2]
        )
        self.out_df = self.out_df.assign(time=self.df.iloc[:, 16])

    def clear_buffer(self):
        """
        バッファーをクリアします。

        """
        self.spinebases.clear()
        self.hips.clear()
        self.knees.clear()
        self.ankles.clear()
        self.wrists.clear()
        self.shoulders.clear()

        self.out_df = None
        self.name = None
        self.df = None

    def to_csv(self, out_dir: str = None):
        """
        読み込んだJSONファイルをCSVにして出力します。

        Args:
            out_dir: 保存先ディレクトリ名。指定しなかった場合、カレントディレクトリに格納されいます。 str

        """
        if out_dir is None:
            out_dir = os.getcwd()

        self.out_df.to_csv(os.path.join(out_dir, self.name.replace('.json', '.csv')), header=False, index=False)

    def __call__(self, name: str, in_dir: str = None, out_dir: str = None) -> None:
        """

        Args:
            name: ファイル名。 str
            in_dir: 引数1で指定したファイルが格納されているディレクトリのパス。 指定しなかった場合、プログラムのカレントディレクトリ。
            out_dir: 保存先ディレクトリ名。指定しなかった場合、カレントディレクトリに格納されいます。 str

        Examples::
            >>> j2c = KinectJson2CSV()
            >>> j2c("some.csv", "in_dir", "out_dir")
        """
        self.load_json(name, in_dir)
        self.organize()
        self.to_csv(out_dir)
        self.clear_buffer()
