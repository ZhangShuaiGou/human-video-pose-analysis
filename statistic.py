import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

COMnpz = "912_COM.npz"
ANGnpz = "2012_Ang.npz"


#COM data structure is: frameNum = all_frames, moveLimb = limb_str, pos = COM_pos, dist = COM_dist
data_COM = np.load(COMnpz)

#ANG data structure is: frameNum = all_frames, moveLimb = limb_str, armLen = arm_len, spineAng = spine_ang, elbowAng = elbow_ang, kneeAng = knee_ang, shoulderAng = shoulder_ang, hipAng = hip_ang
data_ANG = np.load(ANGnpz)

#load the data to pd frame
pd_frameNum = pd.DataFrame(data_ANG['frameNum'])
pd_moveLimb = pd.DataFrame(data_ANG['moveLimb'])
pd_spineAng = pd.DataFrame(data_ANG['spineAng'], columns=['FP', 'MP'])
pd_elbowAng = pd.DataFrame(data_ANG['elbowAng'], columns=['Left', 'Right'])
pd_kneeAng = pd.DataFrame(data_ANG['kneeAng'], columns=['Left', 'Right'])

pd_shoulderFlexion = pd.DataFrame([i[0] for i in data_ANG['shoulderAng']], columns=['Left', 'Right'])
pd_shoulderAbduction = pd.DataFrame([i[1] for i in data_ANG['shoulderAng']], columns=['Left', 'Right'])

pd_hipFlexion = pd.DataFrame([i[0] for i in data_ANG['hipAng']], columns=['Left', 'Right'])
pd_hipFlexion = pd_hipFlexion[(pd_hipFlexion < 125).all(1)]
pd_hipAbduction = pd.DataFrame([i[1] for i in data_ANG['hipAng']], columns=['Left', 'Right'])
pd_hipAbduction = pd_hipAbduction[(pd_hipAbduction < 50).all(1)]



def _statistic(_target, _name):
		
	gcut = pd.cut(_target, bins=5, right = False)
	_max = _target.max()
	_min = _target.min()

	#cut the range
	gcut_count = gcut.value_counts(sort=False)
	#count the frequency
	gcut_frequency = gcut_count/gcut_count.sum()
	#count the Cumulative frequency
	gcut_frequency_sum = (gcut_count/gcut_count.sum()).cumsum()

	re = pd.DataFrame(gcut_count)
	re.rename(columns = {gcut_count.name:'Count'}, inplace=True)
	re['Frequency'] = gcut_frequency
	re['Cumulative_Frequency'] = gcut_frequency_sum
	re['Max'] = _max.round(3)
	re['Min'] = _min.round(3)
	re['Mean'] = _target.mean().round(3)
	re['SD'] = _target.std().round(3)
	print(re)
	print('\n')

	
	print("The mean of angles of " + _name + " is: %.2f" % _target.mean())
	print("The SD of angles of " + _name + " is: %.2f" % _target.std())			
	print("The min angle  of " + _name + " is %.2f" % _target.min())
	print("The max angle of " + _name + " is  %.2f" % _target.max())
	
	
	#re.to_csv('data collection/' + _name + '.csv')
	



#0-59 is RF
#60-77 is RH
#78-105 is Adjust
#106-130 is LF
#131-158 is LH

'''
_statistic(pd_elbowAng['Left'][0:59],'L_Elbow_RF')
_statistic(pd_elbowAng['Left'][60:77],'L_Elbow_RH')
_statistic(pd_elbowAng['Left'][78:105],'L_Elbow_AS')
_statistic(pd_elbowAng['Left'][106:130],'L_Elbow_LF')
_statistic(pd_elbowAng['Left'][131:158],'L_Elbow_LH')

_statistic(pd_elbowAng['Right'][0:59],'R_Elbow_RF')
_statistic(pd_elbowAng['Right'][60:77],'R_Elbow_RH')
_statistic(pd_elbowAng['Right'][78:105],'R_Elbow_AS')
_statistic(pd_elbowAng['Right'][106:130],'R_Elbow_LF')
_statistic(pd_elbowAng['Right'][131:158],'R_Elbow_LH')
print("elbow statistic finished!")


_statistic(pd_kneeAng['Left'][0:59],'L_Knee_RF')
_statistic(pd_kneeAng['Left'][60:77],'L_Knee_RH')
_statistic(pd_kneeAng['Left'][78:105],'L_Knee_AS')
_statistic(pd_kneeAng['Left'][106:130],'L_Knee_LF')
_statistic(pd_kneeAng['Left'][131:158],'L_Knee_LH')

_statistic(pd_kneeAng['Right'][0:59],'R_Knee_RF')
_statistic(pd_kneeAng['Right'][60:77],'R_Knee_RH')
_statistic(pd_kneeAng['Right'][78:105],'R_Knee_AS')
_statistic(pd_kneeAng['Right'][106:130],'R_Knee_LF')
_statistic(pd_kneeAng['Right'][131:158],'R_Knee_LH')
print("knee statistic finished!")



_statistic(pd_shoulderFlexion['Left'][0:59],'L_ShouF_RF')
_statistic(pd_shoulderFlexion['Left'][60:77],'L_ShouF_RH')
_statistic(pd_shoulderFlexion['Left'][78:105],'L_ShouF_AS')
_statistic(pd_shoulderFlexion['Left'][106:130],'L_ShouF_LF')
_statistic(pd_shoulderFlexion['Left'][131:158],'L_ShouF_LH')

_statistic(pd_shoulderFlexion['Right'][0:59],'R_ShouF_RF')
_statistic(pd_shoulderFlexion['Right'][60:77],'R_ShouF_RH')
_statistic(pd_shoulderFlexion['Right'][78:105],'R_ShouF_AS')
_statistic(pd_shoulderFlexion['Right'][106:130],'R_ShouF_LF')
_statistic(pd_shoulderFlexion['Right'][131:158],'R_ShouF_LH')
print("shoulder flexion statistic finished!")

_statistic(pd_shoulderAbduction['Left'][0:59],'L_ShouA_RF')
_statistic(pd_shoulderAbduction['Left'][60:77],'L_ShouA_RH')
_statistic(pd_shoulderAbduction['Left'][78:105],'L_ShouA_AS')
_statistic(pd_shoulderAbduction['Left'][106:130],'L_ShouA_LF')
_statistic(pd_shoulderAbduction['Left'][131:158],'L_ShouA_LH')

_statistic(pd_shoulderAbduction['Right'][0:59],'R_ShouA_RF')
_statistic(pd_shoulderAbduction['Right'][60:77],'R_ShouA_RH')
_statistic(pd_shoulderAbduction['Right'][78:105],'R_ShouA_AS')
_statistic(pd_shoulderAbduction['Right'][106:130],'R_ShouA_LF')
_statistic(pd_shoulderAbduction['Right'][131:158],'R_ShouA_LH')
print("shoulder abduction statistic finished!")
'''

_statistic(pd_hipFlexion['Left'][0:59],'L_HipF_RF')
_statistic(pd_hipFlexion['Left'][60:77],'L_HipF_RH')
_statistic(pd_hipFlexion['Left'][78:105],'L_HipF_AS')
_statistic(pd_hipFlexion['Left'][106:130],'L_HipF_LF')
_statistic(pd_hipFlexion['Left'][131:158],'L_HipF_LH')

_statistic(pd_hipFlexion['Right'][0:59],'R_HipF_RF')
_statistic(pd_hipFlexion['Right'][60:77],'R_HipF_RH')
_statistic(pd_hipFlexion['Right'][78:105],'R_HipF_AS')
_statistic(pd_hipFlexion['Right'][106:130],'R_HipF_LF')
_statistic(pd_hipFlexion['Right'][131:158],'R_HipF_LH')
print("Hip flexion statistic finished!")


_statistic(pd_hipAbduction['Left'][0:59],'L_HipA_RF')
_statistic(pd_hipAbduction['Left'][60:77],'L_HipA_RH')
_statistic(pd_hipAbduction['Left'][78:105],'L_HipA_AS')
_statistic(pd_hipAbduction['Left'][106:130],'L_HipA_LF')
_statistic(pd_hipAbduction['Left'][131:158],'L_HipA_LH')

_statistic(pd_hipAbduction['Right'][0:59],'R_HipA_RF')
_statistic(pd_hipAbduction['Right'][60:77],'R_HipA_RH')
_statistic(pd_hipAbduction['Right'][78:105],'R_HipA_AS')
_statistic(pd_hipAbduction['Right'][106:130],'R_HipA_LF')
_statistic(pd_hipAbduction['Right'][131:158],'R_HipA_LH')
print("Hip abduction statistic finished!")

'''

_statistic(pd_spineAng['FP'][0:59],'F_Spine_RF')
_statistic(pd_spineAng['FP'][60:77],'F_Spine_RH')
_statistic(pd_spineAng['FP'][78:105],'F_Spine_AS')
_statistic(pd_spineAng['FP'][106:130],'F_Spine_LF')
_statistic(pd_spineAng['FP'][131:158],'F_Spine_LH')

_statistic(pd_spineAng['MP'][0:59],'M_Spine_RF')
_statistic(pd_spineAng['MP'][60:77],'M_Spine_RH')
_statistic(pd_spineAng['MP'][78:105],'M_Spine_AS')
_statistic(pd_spineAng['MP'][106:130],'M_Spine_LF')
_statistic(pd_spineAng['MP'][131:158],'M_Spine_LH')
print("Spine statistic finished!")
'''









'''

_statistic(pd_elbowAng['Left'],'L_Elbow')


_statistic(pd_elbowAng['Right'],'R_Elbow')

print("elbow statistic finished!")


_statistic(pd_kneeAng['Left'],'L_Knee')


_statistic(pd_kneeAng['Right'],'R_Knee')

print("knee statistic finished!")
'''

'''
_statistic(pd_shoulderFlexion['Left'],'L_ShouF')


_statistic(pd_shoulderFlexion['Right'],'R_ShouF')

print("shoulder flexion statistic finished!")

_statistic(pd_shoulderAbduction['Left'],'L_ShouA')


_statistic(pd_shoulderAbduction['Right'],'R_ShouA')

print("shoulder abduction statistic finished!")


_statistic(pd_hipFlexion['Left'],'L_HipF')


_statistic(pd_hipFlexion['Right'],'R_HipF')

print("Hip flexion statistic finished!")


_statistic(pd_hipAbduction['Left'],'L_HipA')


_statistic(pd_hipAbduction['Right'],'R_HipA')

print("Hip abduction statistic finished!")


_statistic(pd_spineAng['FP'],'F_Spine')


_statistic(pd_spineAng['MP'],'M_Spine')

print("Spine statistic finished!")

'''

