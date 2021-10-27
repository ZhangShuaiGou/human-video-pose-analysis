# Analysis of human postures and movements from video

This project aims to abstract key parameters from human postures and movements from video. 

To detect the human from videos, I used [```Videopose3D```](https://github.com/facebookresearch/VideoPose3D) .

```COM_calculator.py``` and ```joint_angle_calculator.py``` calculated key parameters, including Centre of Mass and multiple angles of 9 key joints. 

```drawfigure.py``` and ```statistic.py``` are used to display the parameters in more details.

```getFileInfo.py``` and ```npy2csv.py``` are relevant tool scripts. 

Two example figures are provided below. 

<img src="D:\Study\PhD\Observation of climbing\paper_v4\figure collection\com_2.png" style="zoom:75%;" />

<img src="D:\Study\PhD\Observation of climbing\paper_v4\figure collection\elbow_knee_angle.png" alt="ds" style="zoom:50%;" />