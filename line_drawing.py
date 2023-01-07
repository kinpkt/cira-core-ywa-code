import cv2
import numpy as np

LINE_COLOR = (0, 255, 255)
POINT_COLOR = (255, 0, 255)

def coslaw(s1, s2, s3):
    costheta = (s1**2+s2**2-s3**2)/(2*s1*s2)
    theta = np.arccos(costheta)
    return theta

def linedis(coor1, coor2):
    distance = np.sqrt((coor1[0]-coor2[0])**2+(coor1[1]-coor2[1])**2)
    return distance

def halfpoint(coor1, coor2):
    half_coor = (int((coor1[0]+coor2[0])/2), int((coor1[1]+coor2[1])/2))
    return half_coor

def drawline(key1, key2):
    if key1 in obj_names:
        parts_in[key1] = True
    if key2 in obj_names:
        parts_in[key2] = True
    try:
        cv2.line(img, coor_dict[key1], coor_dict[key2], LINE_COLOR, 10)
    except:
        pass

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
drawline('Shoulder', 'Butt')
drawline('Butt', 'Knee')
drawline('Knee', 'Foot')

for i in coor_dict:
    cv2.circle(img, coor_dict[i], 15, POINT_COLOR, -1)