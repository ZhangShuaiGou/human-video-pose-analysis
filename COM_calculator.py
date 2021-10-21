import numpy as np
import sys
import csv
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def COM_calculator(_path, _num, _threepts, _showfig):
	#load .npy file
	#total_data=np.load(sys.argv[1])
	#data=total_data[int(sys.argv[2])-1]
	
	total_data = np.load(_path)
	data = total_data[_num]

	
	#rotate the data
	deg = -70*np.pi/180
	#-43 for CU1
	#-110 for CU2
	#-70 for CU3
	for idx, val in enumerate(data):
		tmp = val[1]
		val[1]=np.cos(deg)*val[1] - np.sin(deg)*val[2]
		val[2]=np.sin(deg)*tmp + np.cos(deg)*val[2]
	print("Data has been rotated by 90 deg")
	
	
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

	#calculate the CM
	CM=(HEAD*8.26	\
		+THORAX*20.1	\
		+SPINE*13.1	\
		+HIP*13.7	\
		+(R_WRIST+R_ELBOW)/2*2.52	\
		+(R_ELBOW+R_SHOULDER)/2*3.25	\
		+(L_WRIST+L_ELBOW)/2*2.52	\
		+(L_ELBOW+L_SHOULDER)/2*3.25	\
		+(R_HIP+R_KNEE)/2*10.5	\
		+(R_KNEE+R_FOOT)/2*6.18	\
		+(L_HIP+L_KNEE)/2*10.5	\
		+(L_KNEE+L_FOOT)/2*6.18)	\
		/100

	#To deal with the blank cell in CSV output
	new_CM = [CM[0],CM[1],CM[2]]
	#print("The position of COM is: ",new_CM)


	#create four planes
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
			
		return Ax, By, Cz, D, N

	def threepts_set(threepts, n):
		threepts = np.asarray(threepts)
		new_threepts = np.delete(threepts, np.argwhere(threepts==n))
		return new_threepts

	#load all the hands and feet
	threepts = [3, 6, 13, 16]

	#delete the limb is leasing
	#threepts = threepts_set(threepts, int(sys.argv[3]))
	threepts = threepts_set(threepts, _threepts)

	# draw the surface plane
	Ax, By, Cz, D, N = define_plane(data[threepts[0]],data[threepts[1]], data[threepts[2]])

	#calculate the distance to four planes
	mod_d = Ax*CM[0] + By*CM[1] + Cz*CM[2] - D
	mod_plane = np.sqrt(np.sum(np.square([Ax,By,Cz])))
	d = abs(mod_d) / mod_plane

	#find the project point of COM
	t = mod_d / np.sum(np.square([Ax,By,Cz]))
	p_CM0 = CM[0]-Ax*t
	p_CM1 = CM[1]-By*t
	p_CM2 = CM[2]-Cz*t
	

	if _showfig == 1:
		#show the points in 3D
		fig=plt.figure(1)
		ax2=fig.gca(projection='3d')
		ax=fig.gca(projection='3d')

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

		for i in black_stick_define:
			ax.plot(data[i,0], data[i,1], data[i,2], c='black')			
			#ax.plot(data[i,2], data[i,1], data[i,0], c='r')

		ax.scatter(CM[0], CM[1], CM[2], c='y', label="COM position")
		ax.plot([p_CM0,CM[0]], [p_CM1,CM[1]], [p_CM2,CM[2]], c='purple', label="COM distance", ls='--')
		
		#show the surface plane
		Z,X = np.meshgrid(np.arange(-0.7,0.5,0.05),np.arange(-0.6,0.8,0.05))
		Y = (D-N[0,2]*Z - N[0,0]*X)*1./N[0,1]

		c = ax2.plot_surface(X,Y,Z, label="Climbing surface", alpha=0.3)

		c._facecolors2d=c._facecolors3d
		c._edgecolors2d=c._edgecolors3d
		ax2.legend(loc = 'best',fontsize='small')


		#print("The COM distance to the structure is: ",d)

		#adjust the figure
		x_major_locator=plt.MultipleLocator(0.3)	#change the unit of X axis
		y_major_locator=plt.MultipleLocator(0.3)
		z_major_locator=plt.MultipleLocator(0.3)

		ax.xaxis.set_major_locator(x_major_locator)
		ax.yaxis.set_major_locator(y_major_locator)
		ax.zaxis.set_major_locator(z_major_locator)


		#ax.view_init(elev=-90,azim=-50)

		plt.xlim(-1,1)	#change the range of axis
		plt.ylim(-1,1)


		#plt.xlabel("X")
		#plt.ylabel("Y")
		
		plt.show()
	
	return new_CM, d
	

