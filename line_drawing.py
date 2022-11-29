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

obj_list = payload['DeepDetect']['objects']
obj_names = [obj_list[i]['name'] for i in range(obj_count)]

coor_dict = {}

hand_in = None
foot_in = None
bottom_in = None
head_in = None
knee_in = None
shoulder_in = None

if 'Hand' in obj_list: 
    hand_in = True
    hand_index = obj_names.index('Hand')
    coor_dict['Hand'] = (obj_list[hand_index]['x'], obj_list[hand_index]['y'])
    cv2.circle(img,hand_coor, 20, POINT_COLOR, -1)
if 'Foot' in obj_list:
    foot_in = True
    foot_index = obj_names.index('Foot')
    coor_dict['Foot'] = (obj_list[foot_index]['x'], obj_list[foot_index]['y'])
    cv2.circle(img, foot_coor, 20, POINT_COLOR, -1)
if 'Bottom' in obj_list:
    bottom_in = True
    bottom_index = obj_names.index('Bottom')
    coor_dict['Bottom'] = (obj_list[bottom_index]['x'], obj_list[bottom_index]['y'])
if 'Head' in obj_list:
    head_in = True
    head_index = obj_names.index('Head')
    coor_dict['Head'] = (obj_list[neck_index]['x'], obj_list[neck_index]['y'])
    cv2.circle(img, head_coor, 20, POINT_COLOR, -1)
if 'Knee' in obj_list:
    knee_in = True
    knee_index = obj_names.index('Bottom')
    coor_dict['Knee'] = (obj_list[knee_index]['x'], obj_list[knee_index]['y'])
    cv2.circle(img, knee_coor, 20, POINT_COLOR, -1)
if 'Shoulder' in obj_list:
    shoulder_in = True
    shoulder_index = obj_names.index('Shoulder')
    coor_dict['Shoulder'] = (obj_list[shoulder_index]['x'], obj_list[shoulder_index]['y'])
    cv2.circle(img, shoulder_coor, 20, POINT_COLOR, -1)

if head_in and knee_in:
    half = halfpoint(coor_dict['Head'], coor_dict['Knee'])
    quad = halfpoint(coor_dict['Head'], half)

    cv2.line(img, coor_dict['Head'], coor_dict['Knee'], LINE_COLOR, 10)

    if hand_in:
        cv2.line(img, quad, coor_dict['Hand'], LINE_COLOR, 10)

if knee_in and foot_in:
    cv2.line(img, coor_dict['Knee'], coor_dict['Foot'], LINE_COLOR, 10)