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
        >>> j2c.organize(['base','hir','kr','ar','shr'])
        >>> j2c.to_csv()
        >>> j2c.clear_buffer()
    """
    def __init__(self):
        self.joint_dic = {'base':'SpineBase', 'mid':'SpineMid', 'neck':'Neck','head':'Head','shl':'ShoulderLeft','ell':'ElbowLeft',
                          'wl':'WristLeft','hal':'HandLeft', 'shr':'ShoulderRight','elr':'ElbowRight','wr':'Wristright',
                          'har':'HandRight','hil':'HipLeft','kl':'KneeLeft','al':'AnkleLeft','fl':'FootLeft','hir':'HipRight',
                          'kr':'KneeRight','ar':'AnkleRight','fr':'FootRight','ssh':'SpineShoulder','htl':'HandTipLeft',
                          'tl':'ThumbLeft','htr':'HandTipRight','tr':'ThumbRight','time':'Time'}
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

    def organize(self, joints : list) -> None:
        """
        読み込んだJSONファイルを整理します。

        args:
            joints: 取得したい関節の指定。　list
            Examples::['base','hir','kr','ar','shr']
'           {'base':'SpineBase', 'mid':'SpineMid', 'neck':'Neck','head':'Head','shl':'ShoulderLeft','ell':'ElbowLeft',
            'wl':'WristLeft','hal':'HandLeft', 'shr':'ShoulderRight','elr':'ElbowRight','wr':'Wristright',
            'har':'HandRight','hil':'HipLeft','kl':'KneeLeft','al':'AnkleLeft','fl':'FootLeft','hir':'HipRight',
            'kr':'KneeRight','ar':'AnkleRight','fr':'FootRight','ssh':'SpineShoulder','htl':'HandTipLeft',
            'tl':'ThumbLeft','htr':'HandTipRight','tr':'ThumbRight','time':'Time'}
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

        self.out_df = self.out_df.assign(time=self.df.iloc[:, 16])

    def clear_buffer(self):
        """
        バッファーをクリアします。

        """
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

        self.out_df.to_csv(os.path.join(out_dir, self.name.replace('.json', '.csv')), header=True, index=True)

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
        self.organize(['base','hir','kr','ar','shr'])
        self.to_csv(out_dir)
        self.clear_buffer()
