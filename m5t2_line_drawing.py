import cv2
import numpy as np

LINE_COLOR = (0, 255, 255)
POINT_COLOR = (255, 0, 255)

def coslaw(s1, s2, s3):
    costheta = (s1**2+s2**2-s3**2)/(2*s1*s2)
    theta_rad = np.arccos(costheta)
    theta_deg = np.abs(theta_rad * 180 / np.pi)
    
    if theta_deg > 180:
        theta_deg -= 360

    return theta_deg

def length(coor1, coor2):
    distance = np.sqrt((coor1[0]-coor2[0])**2+(coor1[1]-coor2[1])**2)
    return distance

def halfpoint(coor1, coor2):
    half_coor = (int((coor1[0]+coor2[0])/2), int((coor1[1]+coor2[1])/2))
    return half_coor

def drawline(key1, key2):
    if 'ywa_trace_lengths' not in payload:
        payload['ywa_trace_lengths'] = {}
    if key1 in obj_names:
        parts_in[key1] = True
    if key2 in obj_names:
        parts_in[key2] = True
    try:
        cv2.line(img, coor_dict[key1], coor_dict[key2], LINE_COLOR, 10)
        payload['ywa_trace_lengths'][f'{key1}_{key2}'] = length(coor_dict[key1], coor_dict[key2])
    except:
        pass

def draw_estimated(key1, key2, theta_param):
    if 'ywa_estimated' not in payload:
        payload['ywa_trace_lengths'] = {}
    try:
        k1x = coor_dict[key1][0]
        k2x, k2y = coor_dict[key2]
        y_dest = 0
        if theta_param == 90:
            y_dest = k2y
        elif k2x < k1x:
            y_dest = k2x * -np.tan(theta_param * np.pi/180)
        elif k2x > k1x:
            y_dest = k2x * np.tan(theta_param * np.pi/180)
        cv2.line(img, coor_dict[key1], (k2x, round(y_dest)), (0, 255, 0), 10)
        payload['ywa_estimated'][f'{key1}_{key2}'] = (k2x, y_dest)
    except:
        pass

def calculate_angles():
    key_points = ['Shoulder_Butt', 'Butt_Knee', 'Shoulder_Knee']
    if all(item in payload['ywa_trace_lengths'] for item in key_points):
        s1 = payload['ywa_trace_lengths']['Shoulder_Butt']
        s2 = payload['ywa_trace_lengths']['Butt_Knee']
        s3 = payload['ywa_trace_lengths']['Shoulder_Knee']
        payload['ywa_pushup_angle'] = coslaw(s1, s2, s3)
    else:
        payload['ywa_pushup_angle'] = None

obj_count = payload['DeepDetect']['count']
obj_list = [d for d in payload['DeepDetect']['objects']]
obj_names = payload['DeepDetect']['obj_count_str'].split(' : 1,')

obj_names.pop()

coor_dict = {}

parts_in = {'Hand': False, 'Foot': False, 'Butt': False, 'Head': False, 'Knee': False, 'Shoulder': False}

for i in obj_list:
    coor_dict[i['name']] = (i['x'], i['y'])
   
drawline('Head', 'Shoulder')
drawline('Hand', 'Elbow')
drawline('Shoulder', 'Knee')
drawline('Shoulder', 'Butt')
drawline('Shoulder', 'Hand')
drawline('Butt', 'Knee')
drawline('Knee', 'Foot')

calculate_angles()

draw_estimated('Shoulder', 'Hand', 90)
draw_estimated('Shoulder', 'Knee', 35)
draw_estimated('Knee', 'Foot', 30)

for i in coor_dict:
    cv2.circle(img, coor_dict[i], 15, POINT_COLOR, -1)