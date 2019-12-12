# Kinect_get_joint
Kinectの関節座標取得によって得られるjsonファイルから特定の関節座標を時系列順に抜き出し、csvとして出力する。  
また、得られたCSVファイルから時系列のトレンドグラフを画像ファイルとして出力する。

## Installation
clone this repository and

```shell script
cd Kinect_get_joint
pip install .
```

or 

Build Dockerfile
```shell script
cd Kinect_get_joint
docker build -t jointgetter .

docker run -it jointgetter -v ホストのin_dir:/anaconda/workspace
```

## Requirements
* Pandas == 0.25.2
* matplotlib == 3.0.2

## Usage

`jointgetter.io.KinectJson2CSV`

Kinectから得られるjsonファイルから特定の関節座標を抜き出し、CSVファイルとして出力する

example:
```python
from jointgetter.io import KinectJson2CSV
j2c = KinectJson2CSV()
j2c(name, in_dir,out_dir)

# name:input file
# in_dir:directory with input file(option)
# out_dir:directory to save output file(option)
```

`jointgetter.io.Csv2graph`

得られたCSVファイルから特定の複数関節の関節座標を時系列のトレンドグラフとして画像出力する

example:
```python
from jointgetter.io import Csv2graph
c2g = Csv2graph()
ctg.load_csv(name+'.csv', in_dir)
ctg.make_graph(columns)
ctg.to_image(out_dir)

# name:input file
# in_dir:directory with input file(option)
# columns:Specifying joint to graph (based on X axis)
# out_dir:directory to save output file(option)
```
