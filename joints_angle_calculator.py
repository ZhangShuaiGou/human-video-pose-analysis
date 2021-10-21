import numpy as np
import sys
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

#Create a plane 
def define_plane(p1, p2, p3):
	p1 = np.asarray(p1)
	p2 = np.asarray(p2)
	p3 = np.asarray(p3)
	AB = np.asmatrix(p2-p1)
	AC = np.asmatrix(p3-p1)
	N = np.cross(AB,AC)
		
	Ax = N[0][0]
	By = N[0][1]
	Cz = N[0][2]
	D = Ax * p1[0]+By*p1[1]+Cz*p1[2]
			
	return D, N


#Return the actual angle of two planes
def ang_ptop(n1,n2):
	n1 = np.asarray(n1)
	n2 = np.asarray(n2)
	
	n1_n2 = np.multiply(np.sqrt(np.sum(np.square(n1))),np.sqrt(np.sum(np.square(n2))))
	angle = (np.arccos(n1.dot(n2)/n1_n2))*180/np.pi
	
	if angle > 90:
		angle = 180 - angle
	
	return angle




#Flexion calculation
#Elbow and Knee only contain flexion. Let's start from them
def vtov_cal(p1,p2,p3):
	p1 = np.asarray(p1)
	p2 = np.asarray(p2)
	p3 = np.asarray(p3)
	u = [p2[0]-p1[0], p2[1]-p1[1], p2[2]-p1[2]]
	#v = [p3[0]-p1[0], p3[1]-p1[1], p3[2]-p1[2]]
	v = [p3[0]-p2[0], p3[1]-p2[1], p3[2]-p2[2]]
	N = np.dot(u,v)
	u_v = np.multiply(np.sqrt(np.sum(np.square(u))),np.sqrt(np.sum(np.square(v))))
	angle = (np.arccos(N/u_v))*180/np.pi
		
	return angle

#Test for the flexion_cal
#print(flexion_cal([0,0,0],[1,1,0],[-1,0,0]))


#project the vector to the plane
def vtop(p1, p2, n):
	p1 = np.asarray(p1)
	p2 = np.asarray(p2)
	
	u = np.asmatrix(p2-p1)
	N = np.dot(u, n)
	p = u - N/(np.sqrt(np.sum(np.square(n)))**2)*n
				
	return p


#calculate the angle between vector to plane
#for calculate the angle of shoulder and hip
#n_p is the normal vector of the projected plane
#nc is the normal vector of the calculate plane 
#sa is flag to decide whether angle is a supplementary angle

def vtop_cal(p1, p2, n_p, nc, sa):
	if sa == 1:
		#Create a horizontal plane to verify whether the angle greater than 90 deg
		pv_D,pv_N = define_plane(p1, p1+n_p, p1+nc)
		Zv = (pv_D-pv_N[0,0]*p2[0] - pv_N[0,1]*p2[1])*1./pv_N[0,2]
		
		if Zv > p2[2]: 
			sa = 0
			
	p = vtop(p1,p2,n_p)		
	Nc = np.dot(p,nc)
	#print("Nc is: ", Nc)
	#print("p is: ", p)
	#print("N is: ", nc)
	
	p_n = np.multiply(np.sqrt(np.sum(np.square(p))),np.sqrt(np.sum(np.square(nc))))
	angle = (abs(np.arcsin(Nc/p_n)))*180/np.pi
		
	if sa==1:
		angle = 180 - angle

	return angle


def joints_angle_calculator(_path, _num, _showfig):
	#load .npy file
	#total_data=np.load(sys.argv[1])
	#data=total_data[int(sys.argv[2])-1]

	total_data=np.load(_path)
	data=total_data[_num]

	
	#rotate the data
	deg = -90*np.pi/180
	#-43 for CU1
	#-110 for CU2
	# -70 for CU3
	for idx, val in enumerate(data):
		tmp = val[1]
		val[1]=np.cos(deg)*val[1] - np.sin(deg)*val[2]
		val[2]=np.sin(deg)*tmp + np.cos(deg)*val[2]
	#print("Data has been rotated by 90 deg")


	def switch_feet(data):
		tmp = np.copy(data[3])
		tmp2 = np.copy(data[6])
		data[3] = tmp2
		data[6] = tmp
		return data
	
	if "CU2" in _path and 267 <= _num+1 <= 487:	#_num+1 = frame number	
		data = switch_feet(data) 
		print("Feet switched!")	
	

	#recognize the joints name
	HIP = data[0]
	R_HIP = data[1]
	R_KNEE = data[2]
	R_FOOT = data[3]
	L_HIP = data[4]
	L_KNEE = data[5]
	L_FOOT = data[6]
	SPINE = data[7]
	THORAX = data[8]
	NOSE = data[9]
	HEAD = data[10]
	L_SHOULDER = data[11]
	L_ELBOW = data[12]
	L_WRIST = data[13]
	R_SHOULDER = data[14]
	R_ELBOW = data[15]
	R_WRIST = data[16]

	#Record the length of arm
	arm_len = np.linalg.norm(R_WRIST - R_ELBOW) + np.linalg.norm(R_ELBOW - R_SHOULDER)

	#Create an upper frontal plane
	ufp_D,ufp_N = define_plane(SPINE,L_SHOULDER,R_SHOULDER)
	#Create an upper median plane
	uforward_spine = SPINE + ufp_N[0]
	ump_D,ump_N = define_plane(SPINE,uforward_spine,THORAX)
	
	#print("The Upper angle is: ", ang_ptop(ump_N[0], ufp_N[0]))

	#Create an lower frontal plane
	lfp_D,lfp_N = define_plane(SPINE,L_HIP,R_HIP)
	#Create an lower median plane
	lforward_spine = SPINE + lfp_N[0]
	lmp_D,lmp_N = define_plane(SPINE,lforward_spine,HIP)

	#print("The Lower angle is: ", ang_ptop(lmp_N[0], lfp_N[0]))


	#store spine angle 
	#spine_ang[0] is the angle in frontal plane(Left-Right swing angle)
	#spine_ang[1] is the angle in median plane(Back-Front swing angle)
	spine_ang = np.array([ang_ptop(ump_N[0], lmp_N[0]), ang_ptop(ufp_N[0], lfp_N[0])])
	
	#verify
	#print("The spine angle is: ", spine_ang)
	
	
	#here is test of frontal plane and median plane angle
	#print(ang_ptop(ufp_N[0],ump_N[0]))
	#print(ang_ptop(lfp_N[0],lmp_N[0]))

	'''
	print("The flexion angle of Left elbow is:")
	print(vtov_cal(L_ELBOW,L_WRIST,L_SHOULDER))
	print("The flexion angle of Right elbow is:")
	print(vtov_cal(R_ELBOW,R_SHOULDER,R_WRIST))
	print("The flexion angle of Left knee is:")
	print(vtov_cal(L_KNEE,L_HIP,L_FOOT))
	print("The flexion angle of Right knee is:")
	print(vtov_cal(R_KNEE,R_HIP,R_FOOT))
	'''
	#here are elbow and knee angle, the only have flexion angle
	#xx_angle[0] is Left side,  xx_angle[1] is Right side
	#elbow_ang = np.array([vtov_cal(L_ELBOW,L_WRIST,L_SHOULDER),vtov_cal(R_ELBOW,R_SHOULDER,R_WRIST)])
	#knee_ang = np.array([vtov_cal(L_KNEE,L_HIP,L_FOOT), vtov_cal(R_KNEE,R_HIP,R_FOOT)])
	#20/12/2020
	elbow_ang = np.array([vtov_cal(L_WRIST,L_ELBOW,L_SHOULDER),vtov_cal(R_WRIST,R_ELBOW,R_SHOULDER)])
	knee_ang = np.array([vtov_cal(L_FOOT,L_KNEE,L_HIP), vtov_cal(R_FOOT,R_KNEE,R_HIP)])
	
	#verify
	#print("The elbow angle is: ", elbow_ang)
	#print("The knee angle is: ", knee_ang)
	

	'''
	print("The abduction of Left shoulder is:\n", vtop_cal(L_SHOULDER, L_ELBOW, ufp_N[0], ump_N[0], 0))
	print("The abduction of Right shoulder \n", vtop_cal(R_SHOULDER, R_ELBOW, ufp_N[0], ump_N[0], 0))

	print("The abduction of Left Hip is:\n", vtop_cal(L_HIP, L_KNEE, lfp_N[0], lmp_N[0], 0))
	print("The abduction of Right Hip is:\n", vtop_cal(R_HIP, R_KNEE, lfp_N[0], lmp_N[0], 0))

	print("The flexion of Left shoulder is:\n", vtop_cal(L_SHOULDER, L_ELBOW, ump_N[0], ufp_N[0], 1))
	print("The flexion of Right shoulder is:\n", vtop_cal(R_SHOULDER, R_ELBOW, ump_N[0], ufp_N[0], 1))

	print("The flexion of Left hip is:\n", vtop_cal(L_HIP, L_KNEE, lmp_N[0], lfp_N[0], 1))
	print("The flexion of Right hip is:\n", vtop_cal(R_HIP, R_KNEE, lmp_N[0], lfp_N[0], 1))
	'''
	
	#here are should and hip angle.they have flexion and abdcutution
	#[0][] is Flexion; [1][] is Abduction
	
	shoulder_ang = np.array([[float(vtop_cal(L_SHOULDER, L_ELBOW, ump_N[0], ufp_N[0], 1)), float(vtop_cal(R_SHOULDER, R_ELBOW, ump_N[0], ufp_N[0], 1))],
	[float(vtop_cal(L_SHOULDER, L_ELBOW, ufp_N[0], ump_N[0], 0)), float(vtop_cal(R_SHOULDER, R_ELBOW, ufp_N[0], ump_N[0], 0))]])
		
	hip_ang = np.array([[float(vtop_cal(L_HIP, L_KNEE, lmp_N[0], lfp_N[0], 1)), float(vtop_cal(R_HIP, R_KNEE, lmp_N[0], lfp_N[0], 1))],
	[float(vtop_cal(L_HIP, L_KNEE, lfp_N[0], lmp_N[0], 0)), float(vtop_cal(R_HIP, R_KNEE, lfp_N[0], lmp_N[0], 0))]])

	#verify
	print("The shoulder flexions are: ", shoulder_ang[0])
	print("The shoulder abductions are: ", shoulder_ang[1])
	print("The hip flexions are: ", hip_ang[0])
	print("The hip abductions are: ", hip_ang[1])
	
	#to show the figure
	if _showfig == 1:
		#show the points in 3D
		fig=plt.figure(1)
		ax=fig.gca(projection='3d')
		ax2=fig.gca(projection='3d')


		#draw the planes
		X,Z = np.meshgrid(np.arange(-0.7,0.5,0.05),np.arange(-0.6,0.8,0.05))
		Y1 = (ufp_D-ufp_N[0,0]*X - ufp_N[0,2]*Z)*1./ufp_N[0,1]
		Y2 = (ump_D-ump_N[0,0]*X - ump_N[0,2]*Z)*1./ump_N[0,1]
		Y3 = (lfp_D-lfp_N[0,0]*X - lfp_N[0,2]*Z)*1./lfp_N[0,1]
		Y4 = (lmp_D-lmp_N[0,0]*X - lmp_N[0,2]*Z)*1./lmp_N[0,1]

		#print("N1 dot N2: ",p1_N[0].dot(p2_N[0]))

		'''
		#show the spine joint
		ax2.scatter(SPINE[0], SPINE[1], SPINE[2], c='b', s=6, label="Spine joint")
		
		c1 = ax2.plot_surface(X,Y1,Z, label="Upper Frontal Plane", alpha=0.3)
		c2 = ax2.plot_surface(X,Y2,Z, label="Upper Median Plane", alpha=0.3)
		c3 = ax2.plot_surface(X,Y3,Z, label="Lower Frontal Plane", alpha=0.3)
		c4 = ax2.plot_surface(X,Y4,Z, label="Lower Median Plane", alpha=0.3)

		c1._facecolors2d=c1._facecolors3d
		c1._edgecolors2d=c1._edgecolors3d

		c2._facecolors2d=c2._facecolors3d
		c2._edgecolors2d=c2._edgecolors3d

		c3._facecolors2d=c3._facecolors3d
		c3._edgecolors2d=c3._edgecolors3d

		c4._facecolors2d=c4._facecolors3d
		c4._edgecolors2d=c4._edgecolors3d


		ax2.legend(loc = 'best',fontsize='small')
		'''
		
		'''
		stick_define=[
			(0,1),
			(1,2),
			(2,3),
			(0,4),
			(4,5),
			(5,6),
			(0,7),
			(7,8),
			(8,9),
			(9,10),
			(8,11),
			(11,12),
			(12,13),
			(8,14),
			(14,15),
			(15,16)
		]

		figure=[ax.plot(data[i,0], data[i,1], data[i,2], c='r') for i in stick_define]
		'''		
		
		#create a skeleton
		red_stick_define=[
			(0,1),
			(1,2),
			(2,3),
			(8,14),
			(14,15),
			(15,16)
		]
		
		black_stick_define=[		
			(0,4),
			(4,5),
			(5,6),
			(0,7),
			(7,8),
			(8,9),
			(9,10),
			(8,11),
			(11,12),
			(12,13)
		]
		
		for i in red_stick_define:
			ax.plot(data[i,0], data[i,1], data[i,2], c='r')
			ax.scatter(data[i,0], data[i,1], data[i,2], c='b', s=6)

		for i in black_stick_define:
			ax.plot(data[i,0], data[i,1], data[i,2], c='black')	
			ax.scatter(data[i,0], data[i,1], data[i,2], c='b', s=6)		
			#ax.plot(data[i,2], data[i,1], data[i,0], c='r')
		
		ax.scatter(SPINE[0], SPINE[1], SPINE[2], c='b', s=6, label="Spine joint")


		#adjust the figure
		x_major_locator=plt.MultipleLocator(0.3)	#change the unit of X axis
		y_major_locator=plt.MultipleLocator(0.3)
		z_major_locator=plt.MultipleLocator(0.3)

		ax.xaxis.set_major_locator(x_major_locator)
		ax.yaxis.set_major_locator(y_major_locator)
		ax.zaxis.set_major_locator(z_major_locator)
		'''
		ax.set_xlim3d(xmin=-0.5, xmax=0.5)
		ax.set_ylim3d(ymin=-0.5, ymax=0.5)
		ax.set_zlim3d(zmin=-0.5, zmax=0.5)
		'''
		
		plt.xlim(-1,1)	#change the range of axis
		plt.ylim(-1,1)

		#plt.xlabel("X")
		#plt.ylabel("Y")


		plt.show()
	
	return arm_len, spine_ang, elbow_ang, knee_ang, shoulder_ang, hip_ang

