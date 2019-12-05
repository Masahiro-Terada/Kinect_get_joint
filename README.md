# Kinect_get_joint
Kinectの関節座標取得によって得られるjsonファイルから特定の関節座標を時系列順に抜き出し、csvとして出力する。

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
* Numpy == 1.17.3
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
