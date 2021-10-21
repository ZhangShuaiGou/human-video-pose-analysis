import numpy as np
import matplotlib.pyplot as plt

#COMnpz = "CU1_COM.npz"
#ANGnpz = "CU1_Ang.npz"

#COMnpz = "912_COM.npz"
COMnpz = "2012_COM.npz"
#ANGnpz = "912_Ang.npz"
ANGnpz = "2012_Ang.npz"

#COM data structure is: frameNum = all_frames, moveLimb = limb_str, pos = COM_pos, dist = COM_dist
data_COM = np.load(COMnpz)

#ANG data structure is: frameNum = all_frames, moveLimb = limb_str, armLen = arm_len, spineAng = spine_ang, elbowAng = elbow_ang, kneeAng = knee_ang, shoulderAng = shoulder_ang, hipAng = hip_ang
data_ANG = np.load(ANGnpz)

#print("\n The moving limb is: ", [i for i in data_COM['moveLimb']], end='\n')

#draw the vertical lines according to different phases
def drawvlines(data_ANG, _min, _max):
	_cur = data_ANG['moveLimb'][0]
	_last = _cur
	
	for idx, val in enumerate(data_ANG['moveLimb']):
		_cur = val
		if _cur != _last:
			#plt.vlines(data_ANG['frameNum'][idx],_min,_max,linestyles = 'dashed',colors = 'gray')
			plt.vlines(idx,_min,_max,linestyles = 'dashed',colors = 'gray')
				
		_last = _cur


#x1 = data_COM['frameNum']
x1 = range(0,len(data_COM['dist']))
#y1 = data_COM['dist']

y1 = data_ANG['armLen']


y2 = [i[0] for i in data_ANG['elbowAng']]
y3 = [i[1] for i in data_ANG['elbowAng']]

y4 = [i[0] for i in data_ANG['kneeAng']]
y5 = [i[1] for i in data_ANG['kneeAng']]

#[0] is angle in frontal plane
y6 = [i[0] for i in data_ANG['spineAng']]
#[1] is angle in median plane
y7 = [i[1] for i in data_ANG['spineAng']]

#[0][] flexion
y8 = [i[0][0] for i in data_ANG['shoulderAng']]
y9 = [i[0][1] for i in data_ANG['shoulderAng']]
#[1][] abduction
y10 = [i[1][0] for i in data_ANG['shoulderAng']]
y11 = [i[1][1] for i in data_ANG['shoulderAng']]

y12 = [i[0][0] for i in data_ANG['hipAng']]
y13 = [i[0][1] for i in data_ANG['hipAng']]
y14 = [i[1][0] for i in data_ANG['hipAng']]
y15 = [i[1][1] for i in data_ANG['hipAng']]

#y16 is fixed arm_length
#y17 is flex arm_length
y16 = data_COM['dist'] / np.mean(data_ANG['armLen'])
#print("Mean is: ",np.mean(data_ANG['armLen']))
y17 = data_COM['dist'] / data_ANG['armLen']

#initial a size const
sz = 15

plt.figure()

#l1 = plt.plot(x1, y1, 'r-', label='Distance')
#l16 = plt.plot(x1, y16, 'r-', label='Fixed len')
l17 = plt.plot(x1, y17, 'g--', label='COM distance/Arm length')
drawvlines(data_COM, min(y17), max(y17))
plt.text(10,0.2, "Phase 1:\nLift right foot", alpha = 0.6)
plt.text(65,0.2, "Phase 2:\nRaise right\nhand", alpha = 0.6)
plt.text(80,0.2, "Phase 3:\nAdjust climbing\n posture", alpha = 0.6)
plt.text(110,0.2, "Phase 4:\nLift left foot", alpha = 0.6)
plt.text(140,0.2, "Phase 5:\nRaise left hand", alpha = 0.6)
plt.title("COM distance with frame",size=sz)
plt.xlabel("Frame",size=sz)
plt.ylabel("Ratio",size=sz)
plt.xticks(size=sz)
plt.yticks(size=sz)
plt.legend(fontsize="large")


plt.figure()

plt.subplot(121)
l2 = plt.plot(x1, y2, 'r--', label='Left Elbow')
l3 = plt.plot(x1, y3, 'g-', label='Right Elbow')
drawvlines(data_ANG, min(min(y2),min(y3)), max(max(y2), max(y3),146)+3)
plt.hlines(146, min(x1),max(x1), label='Maxmimun', linestyles = 'dashed',colors = 'blue')
plt.title("Elbow angle with frame",size=sz)
plt.xlabel("Frame",size=sz)
plt.ylabel("Angle(°)",size=sz)
plt.xticks(size=sz)
plt.yticks(size=sz)
plt.legend(fontsize="large")


plt.subplot(122)
l4 = plt.plot(x1, y4, 'r--', label='Left Knee')
l5 = plt.plot(x1, y5, 'g-', label='Right Knee')
drawvlines(data_ANG, min(min(y4),min(y5)), max(max(y4), max(y5), 134)+3)
plt.hlines(134, min(x1),max(x1), label='Average range',  linestyles = 'dashed',colors = 'blue')
plt.title("Knee angle with frame",size=sz)
plt.xlabel("Frame",size=sz)
plt.ylabel("Angle(°)",size=sz)
plt.xticks(size=sz)
plt.yticks(size=sz)
plt.legend(fontsize="large")

plt.figure()

l6 = plt.plot(x1, y6, 'r--', label='Abduction angle')
l7 = plt.plot(x1, y7, 'g-', label='Flexion angle')
drawvlines(data_ANG, min(min(y6),min(y7)), max(max(y6), max(y7), 45)+3)
plt.hlines(45, min(x1),max(x1), label='Average flexion range',  linestyles = 'dashed',colors = 'blue')
plt.hlines(35, min(x1),max(x1), label='Average abduction range',  linestyles = 'dashed',colors = 'purple')
plt.title("Spine angle with frame",size=sz)
plt.xlabel("Frame",size=sz)
plt.ylabel("Angle(°)",size=sz)
plt.xticks(size=sz)
plt.yticks(size=sz)
plt.legend(fontsize="large")



plt.figure()

plt.subplot(221)
l8 = plt.plot(x1, y8, 'r--', label='Left Shoulder')
l9 = plt.plot(x1, y9, 'g-', label='Right Shoulder')
drawvlines(data_ANG, min(min(y8),min(y9)), max(max(y8), max(y9), 158)+3)
plt.hlines(158, min(x1),max(x1), label='Average range',  linestyles = 'dashed',colors = 'blue')
plt.title("Shoulder flexion angle with frame",size=sz)
#plt.xlabel("Frame")
plt.ylabel("Angle(°)",size=sz)
plt.xticks(size=sz)
plt.yticks(size=sz)
plt.legend(fontsize="large")

plt.subplot(222)
l10 = plt.plot(x1, y10, 'r--', label='Left Shoulder')
l11 = plt.plot(x1, y11, 'g-', label='Right Shoulder')
drawvlines(data_ANG, min(min(y10),min(y11)), max(max(y10), max(y11), 170)+3)
plt.hlines(170, min(x1),max(x1), label='Average range', linestyles = 'dashed',colors = 'blue')
plt.title("Shoulder abduction angle with frame",size=sz)
#plt.xlabel("Frame")
plt.ylabel("Angle(°)",size=sz)
plt.xticks(size=sz)
plt.yticks(size=sz)
plt.legend(fontsize="large")


plt.subplot(223)
l12 = plt.plot(x1, y12, 'r--', label='Left Hip')
l13 = plt.plot(x1, y13, 'g-', label='Right Hip')
drawvlines(data_ANG, min(min(y12),min(y13))-1, max(max(y12), max(y13), 125)+3)
plt.hlines(125, min(x1),max(x1), label='Average range',  linestyles = 'dashed',colors = 'blue')
plt.title("Hip flexion angle with frame",size=sz)
plt.xlabel("Frame",size=sz)
plt.ylabel("Angle(°)",size=sz)
plt.xticks(size=sz)
plt.yticks(size=sz)
plt.legend(fontsize="large")


plt.subplot(224)
l14 = plt.plot(x1, y14, 'r--', label='Left Hip')
l15 = plt.plot(x1, y15, 'g-', label='Right Hip')
drawvlines(data_ANG, min(min(y14),min(y15))-1, max(max(y14), max(y15), 50)+3)
plt.hlines(50, min(x1),max(x1), label='Average range',  linestyles = 'dashed',colors = 'blue')
plt.title("Hip abduction angle with frame",size=sz)
plt.xlabel("Frame",size=sz)
plt.ylabel("Angle(°)",size=sz)
plt.xticks(size=sz)
plt.yticks(size=sz)
plt.legend(fontsize="large")



#plt.savefig("CU1.jpg")
plt.show()
