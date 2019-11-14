# Kinect_get_joint
Kinectの関節座標取得によって得られるjsonファイルから特定の関節座標を時系列順に抜き出し、csvとして出力する。

## 必要ライブラリ
・Numpy 1.17.3 <br>
・Pandas 0.25.2 <br>
・matplotlib 3.0.2

## 使用方法

## json_to_csv()
## Kinectから得られるjsonファイルから特定の関節座標を抜き出し、CSVファイルとして出力する

example: <br>
jtc=json_to_csv() <br>
jtc.csv = (name, in_dir,out_dir)

name:input file <br>
in_dir:directory with input file(option) <br>
設定しない場合はカレントディレクトリから読み取る <br>
out_dir:directory to save output file(option) <br> 
設定しない場合はカレントディレクトリに保存する


