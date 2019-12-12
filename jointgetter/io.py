import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


class KinectJson2CSV(object):
    """

    Examples::
        >>> j2c = KinectJson2CSV()
        >>> j2c("sample.csv", "in_dir", "out_dir")
        >>> # or
        >>> j2c.load_json("some.json")
        >>> j2c.organize(['base','hir','kr','ar','shr'])
        >>> j2c.to_csv()
    """
    def __init__(self):
        self.joint_dic = {'base':'SpineBase', 'mid':'SpineMid', 'neck':'Neck','head':'Head', 'shl':'ShoulderLeft', 'ell':'ElbowLeft',
                          'wl':'WristLeft', 'hal':'HandLeft', 'shr':'ShoulderRight', 'elr':'ElbowRight', 'wr':'Wristright',
                          'har':'HandRight', 'hil':'HipLeft', 'kl':'KneeLeft', 'al':'AnkleLeft', 'fl':'FootLeft', 'hir':'HipRight',
                          'kr':'KneeRight', 'ar':'AnkleRight', 'fr':'FootRight', 'ssh':'SpineShoulder', 'htl':'HandTipLeft',
                          'tl':'ThumbLeft', 'htr':'HandTipRight', 'tr':'ThumbRight'}
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

    def organize(self, joints : list, time : bool = True) -> None:
        """
        読み込んだJSONファイルを整理します。

        args:
            joints: 取得したい関節の指定。　list
            Examples::['base','hir','kr','ar','shr']
'           {'base':'SpineBase', 'mid':'SpineMid', 'neck':'Neck','head':'Head', 'shl':'ShoulderLeft', 'ell':'ElbowLeft',
              'wl':'WristLeft', 'hal':'HandLeft', 'shr':'ShoulderRight', 'elr':'ElbowRight', 'wr':'Wristright',
              'har':'HandRight', 'hil':'HipLeft', 'kl':'KneeLeft', 'al':'AnkleLeft', 'fl':'FootLeft', 'hir':'HipRight',
              'kr':'KneeRight', 'ar':'AnkleRight', 'fr':'FootRight', 'ssh':'SpineShoulder', 'htl':'HandTipLeft',
              'tl':'ThumbLeft', 'htr':'HandTipRight', 'tr':'ThumbRight'}
            time: 時間を取得するかどうか　　bool
        """
        cols = []
        for joint in joints:
            cols.append(self.joint_dic[joint] + '_X')
            cols.append(self.joint_dic[joint] + '_Y')
            cols.append(self.joint_dic[joint] + '_Z')
        self.out_df = pd.DataFrame(index=[], columns=cols)

        for i in range(len(self.df)):
            data = self.df.iloc[i, 15]
            positions = []
            for joint in joints:
                positions.append(data[self.joint_dic[joint]]['Position']['X'])
                positions.append(data[self.joint_dic[joint]]['Position']['Y'])
                positions.append(data[self.joint_dic[joint]]['Position']['Z'])

            df_cache = pd.Series(positions,index=self.out_df.columns)
            self.out_df = self.out_df.append(df_cache,ignore_index=True)
        if time:
            self.out_df = self.out_df.assign(time=self.df.iloc[:, 16])

    def to_csv(self, out_dir: str = None):
        """
        読み込んだJSONファイルをCSVにして出力します。

        Args:
            out_dir: 保存先ディレクトリ名。指定しなかった場合、カレントディレクトリに格納されいます。 str

        """
        if out_dir is None:
            out_dir = os.getcwd()

        self.out_df.to_csv(os.path.join(out_dir, self.name.replace('.json', '.csv')), header=True, index=True)

    def __call__(self, name: str, in_dir: str = None, out_dir: str = None) -> None:
        """

        Args:
            name: ファイル名。 str
            in_dir: 引数1で指定したファイルが格納されているディレクトリのパス。 指定しなかった場合、プログラムのカレントディレクトリ。
            out_dir: 保存先ディレクトリ名。指定しなかった場合、カレントディレクトリに格納されいます。 str

        Examples::
            >>> j2c = KinectJson2CSV()
            >>> j2c("sample.json", "in_dir", "out_dir")
        """
        self.load_json(name, in_dir)
        self.organize(['base','hir','kr','ar','shr'])
        self.to_csv(out_dir)

class Csv2graph(object):
    """

    Examples::
        >>> c2g =Csv2graph()
        >>> c2g.load_csv("sample.csv")
        >>> c2g.make_graph([0,3,6])
        >>> c2g.to_image()
    """
    def __init__(self):
        self.out_file = None
        self.name = None
        self.df = None

    def load_csv(self, name: str, in_dir: str = None) -> None:
        """
        指定したCSVファイルを読み込みます。
        in_dir に何も指定しない場合は自動的にカレントディレクトリが指定されます。

        Args:
            name: ファイル名。 str
            in_dir: 引数1で指定したファイルが格納されているディレクトリのパス。 指定しなかった場合、プログラムのカレントディレクトリ。

        """
        if in_dir is None:
            in_dir = os.getcwd()

        self.name = name
        self.df = pd.read_csv(os.path.join(in_dir, name), index_col=0)

    def make_graph(self, columns: list, font_size=35) -> None:
        """
        読み込んだCSVファイルの時系列データをグラフ化します。

        Args:
            columns: グラフ化する関節を指定する。ここでは、X座標の列を基準とする。最大で3関節まで指定可　list
            font_size: グラフのタイトル、ラベル名、メモリの文字の大きさを指定する。　int

        Examples:


        """
        df_cache = pd.concat([self.df.iloc[:,columns[0]:columns[0]+3],self.df.iloc[:,columns[1]:columns[1]+3],
                             self.df.iloc[:,columns[2]:columns[2]+3]],axis=1)
        plt.close('all')
        self.fig = plt.figure(figsize=(35, 30))
        plt.subplots_adjust(left=0.1, right=0.95, bottom=0.12, top=0.95, wspace=0.3, hspace=0.5)

        # グラフをプロット
        for i,(title, data) in zip(range(1,10),df_cache.items()):
            ax = self.fig.add_subplot(3, 3, i)
            ax.plot(data)
            ax.set_title(title, fontsize=font_size)
            ax.set_xlabel('Time', fontsize=font_size)
            ax.set_ylabel('Coordinate', fontsize=font_size)
            plt.tick_params(labelsize=font_size - 7)

    def to_image(self, out_dir: str = None):
        """
        作成したグラフを画像にして出力します。

        Args:
            out_dir: 保存先ディレクトリ名。指定しなかった場合、カレントディレクトリに格納されいます。 str

        """
        if out_dir is None:
            out_dir = os.getcwd()

        self.fig.savefig(os.path.join(out_dir, self.name.replace('.csv', '.png')))

