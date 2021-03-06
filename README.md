# Analysis of human postures and movements from video

This project aims to abstract key parameters from human postures and movements from video. 

To detect the human from videos, I used [```Videopose3D```](https://github.com/facebookresearch/VideoPose3D) and rebuilt the skeletons.

<img src="examplepics\rh_move.png" alt="rhg_move" style="zoom:80%;" />

<p align="center">
  <img src="examplepics\com_1.png" alt="d" style="width:40%; float:left"/>  <img src="examplepics\com_2.png" alt="c" style="width:40%; float:right"/> 
</p>

```COM_calculator.py``` and ```joint_angle_calculator.py``` calculated key parameters, including Centre of Mass and multiple angles of 9 key joints. 

```drawfigure.py``` and ```statistic.py``` are used to display the parameters in more details.

```getFileInfo.py``` and ```npy2csv.py``` are relevant tool scripts. 

<img src="examplepics\shoulder_hip_angle.png" alt="shoulder_hip_angle" style="zoom:80%;" />
