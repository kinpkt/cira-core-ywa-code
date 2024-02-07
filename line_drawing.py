import cv2
import numpy as np

LINE_COLOR = (0, 255, 255)
POINT_COLOR = (255, 0, 255)
ESTIMATED_COLOR = (0, 255, 0)

T_LINE = 5.5
T_POINT = 12.5

def length(coor1, coor2):
    distance = np.sqrt((coor1[0]-coor2[0])**2+(coor1[1]-coor2[1])**2)
    return distance

def slope(coor1, coor2):
    rise = coor2[1] - coor1[1]
    run = coor2[0] - coor1[0]
    return rise/run

def drawline(key1, key2):
    if 'ywa_trace_lengths' not in payload:
        payload['ywa_trace_lengths'] = {}
    if 'ywa_segment_coor' not in payload:
        payload['ywa_segment_coor'] = {}
    if 'ywa_slopes' not in payload:
        payload['ywa_slopes'] = {}
    if key1 in obj_names:
        parts_in[key1] = True
    if key2 in obj_names:
        parts_in[key2] = True
    try:
        cv2.line(img, coor_dict[key1], coor_dict[key2], LINE_COLOR, LINE_SIZE)
        payload['ywa_trace_lengths'][f'{key1}_{key2}'] = length(coor_dict[key1], coor_dict[key2])
        payload['ywa_segment_coor'][f'{key1}_{key2}'] = (coor_dict[key1], coor_dict[key2])
        payload['ywa_slopes'][f'{key1}_{key2}'] = slope(coor_dict[key1], coor_dict[key2])
    except:
        pass

def draw_estimated(key1, key2):
    if 'ywa_estimated' not in payload:
        payload['ywa_estimated'] = {}
    if 'ywa_segment_coor' not in payload:
        payload['ywa_segment_coor'] = {}
    try:
        k1x, k1y = coor_dict[key1]
        k2x, k2y = coor_dict[key2]
        y_dest = 0
        m = 1
        if key1 == 'Shoulder' and key2 == 'Hand':
            payload['ywa_slopes']['estimated_Shoulder_Hand'] = payload['ywa_slopes']['Shoulder_Hand']
            return cv2.line(img, coor_dict[key1], (k1x, k2y), ESTIMATED_COLOR, LINE_SIZE)
        elif key1 == 'Shoulder' and key2 == 'Knee':
            m = 0.5
            c = 75.3952
        elif key1 == 'Knee' and key2 == 'Foot':
            m = 1
            c = 169.538
        y_dest = int(np.round(m * k1x + c))
        cv2.line(img, coor_dict[key1], (k2x, y_dest), ESTIMATED_COLOR, LINE_SIZE)
        payload['ywa_estimated'][f'{key1}_{key2}'] = (k2x, y_dest)
        payload['ywa_segment_coor'][f'estimated_{key1}_{key2}'] = (coor_dict[key1], coor_dict[key2])
        payload['ywa_slopes'][f'estimated_{key1}_{key2}'] = m
    except:
        pass

def calculate_angles():
    if 'ywa_calculate' not in payload:
        payload['ywa_calculate'] = {}
    key_points = ['Shoulder_Butt', 'Butt_Knee', 'Shoulder_Knee']
    if all(item in payload['ywa_trace_lengths'] for item in key_points):
        s1 = payload['ywa_trace_lengths']['Shoulder_Butt']
        s2 = payload['ywa_trace_lengths']['Butt_Knee']
        s3 = payload['ywa_trace_lengths']['Shoulder_Knee']
        payload['ywa_calculate']['real_theta'] = coslaw(s1, s2, s3)
    else:
        payload['ywa_calculate'] = None

def analyze_warning():
    key_points = ['Shoulder_Hand', 'Shoulder_Knee', 'Knee_Foot']
    if 'ywa_label' not in payload:
        payload['ywa_label'] = {'no_parts': []}
        for key in key_points:
            payload['ywa_label'][f'pass_{key}'] = None
    for part in parts_in:
        if not parts_in[part]:
            payload['ywa_label']['no_parts'].append(part)  
    for key in key_points:
        if key in payload['ywa_slopes'] and f'estimated_{key}' in payload['ywa_slopes']:
            real = payload['ywa_slopes'][key]
            estimate = payload['ywa_slopes'][f'estimated_{key}']
            lower = estimate - 0.2 * estimate
            upper = estimate + 0.2 * estimate
            payload['ywa_label'][f'pass_{key}'] = lower <= real or real <= upper or real == estimate

obj_count = payload['DeepDetect']['count']
obj_list = [d for d in payload['DeepDetect']['objects']]
obj_names = list(set([obj['name'] for obj in obj_list]))

coor_dict = {}
w_arr = []
h_arr = []

parts_in = {'Hand': False, 'Foot': False, 'Head': False, 'Knee': False, 'Shoulder': False}

for i in obj_list:
    coor_dict[i['name']] = (i['x'], i['y'])
    w_arr.append(i['w'])
    h_arr.append(i['h'])

LINE_SIZE = int(np.round(((sum(h_arr)/len(coor_dict))/(sum(w_arr)/len(coor_dict)) * T_LINE)))
POINT_SIZE = int(np.round(((sum(h_arr)/len(coor_dict))/(sum(w_arr)/len(coor_dict)) * T_POINT)))
   
drawline('Head', 'Shoulder')
drawline('Hand', 'Elbow')
drawline('Shoulder', 'Knee')
drawline('Shoulder', 'Butt')
drawline('Shoulder', 'Hand')
drawline('Butt', 'Knee')
drawline('Knee', 'Foot')

calculate_angles()

draw_estimated('Shoulder', 'Hand')
draw_estimated('Shoulder', 'Knee')
draw_estimated('Knee', 'Foot')

analyze_warning()

for i in coor_dict:
    cv2.circle(img, coor_dict[i], POINT_SIZE, POINT_COLOR, -1)