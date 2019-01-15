# videoavatars_custom

## 原版本Demo

请先使用原版本Demo来验证环境部署成功:[Video Avatars](https://github.com/thmoa/videoavatars/blob/master/README.md)

## 数据准备

这个部分，我们将利用自摄的视频来进行的建模尝试，首先需要有一段如[原论文视频](https://graphics.tu-bs.de/upload/publications/alldieck2018video/alldieck2018videoavatar.mp4)相同的自摄视频，提供我的格式：

| 项目     | 格式           |
| -------- | -------------- |
| 分辨率   | 1080*1080      |
| 帧率     | 24FPS          |
| 身体姿态 | A形姿态旋转3圈 |
|          |                |

之后你可以使用 `frame_get.py`来获取到所有视频帧，以供下一步处理。

### Step1:视频帧人体区域获取

​	这一步中，我们需要获得每一视频帧中，如下图形式的人体区域的二值图像：

​	![mask1](https://wpy-blog.oss-cn-shanghai.aliyuncs.com/mask1.jpg/wpy-blog)

在这一步中，我采用了百度AI开放平台的人像分割API来进行，你也可以采用其他AI开放平台的API，或者使用自己的语义分割实现。这一部分脚本在 `human_mask.py` 中可以找到。

​	![origin](https://wpy-blog.oss-cn-shanghai.aliyuncs.com/origin1.jpg/wpy-blog)

![mask2](https://wpy-blog.oss-cn-shanghai.aliyuncs.com/mask1.jpg/wpy-blog)

受限于一些图像干扰，以及语义分割本身问题，获取到的`mask`图像往往还需要进一步处理：

![mask3](https://wpy-blog.oss-cn-shanghai.aliyuncs.com/mask2.jpg/wpy-blog)

可以看到，有一些无意义的区域，为了提升准确率，需要对mask进行取最大连通域的处理，之后可以再进行一次形态学膨胀操作消除空洞。这部分工作在`mask_process.py`中实现。

![mask3](https://wpy-blog.oss-cn-shanghai.aliyuncs.com/mask3.jpg/wpy-blog)

至此，我们就完成了mask的处理工作，之后，利用`video_avatars/prpare_data/mask2hdf5.py`即可将其转化为HDF5文件。 

### Step2：人体关节点标识

​	这一步需要将每一帧的关节点及其坐标转换为Jason格式，这里直接使用，Openpose来进行关节点识别。同样你也可以使用自己的实现或其他途径来进行关节点识别，只需符合COCO模型的关节点模式：

![COCO模型](https://ws1.sinaimg.cn/large/662f5c1fly1fxnug3i1atj20dc0hpt8q.jpg)

Openpose具体安装和使用可以参考[这里](https://github.com/CMU-Perceptual-Computing-Lab/openpose/blob/master/doc/installation.md)，我就不再详细介绍。

获取到所有的关节点的json文件后，使用`video_avatars/prpare_data/2djoints2hdf5.py` 可将其转化为HDF5文件。

### Step3:相机相关参数

在`video_avatars/prpare_data`下，还有	`create_camera.py`来进行相机相关参数的序列化。

```python

parser.add_argument('out', type=str, help="Output file (.pkl)")
parser.add_argument('width', type=int, help="Frame width in px")
parser.add_argument('height', type=int, help="Frame height in px")
parser.add_argument('-f', type=float, nargs='*', help="Focal length in px (2,)")
parser.add_argument('-c', type=float, nargs='*', help="Principal point in px (2,)")
parser.add_argument('-k', type=float, nargs='*', help="Distortion coefficients (5,)")
```

主要参数是分辨率以及像素焦距（Focal length in pixels ），由于我使用手机拍摄，其他参数难以获取，如果你能获取到准确数据可以将相应数据加入。

对于像素焦距（Focal length in pixels ），有以下公式可以计算：

$$
Focal length in pixels = (image width in pixels) * (focal length on earth) / (CCD width on earth)
$$

## 构建运行

与之前的Demo相同，可以在[这里](https://github.com/thmoa/videoavatars#usage)找到具体命令。

## 最终效果

- 无衣着效果：

  ![result](https://wpy-blog.oss-cn-shanghai.aliyuncs.com/result1.PNG/wpy-blog)

- 有衣着效果：

  ​	![result2](https://wpy-blog.oss-cn-shanghai.aliyuncs.com/result2.PNG/wpy-blog)

## 联系我：

​	mail:wangpy1489@163.com