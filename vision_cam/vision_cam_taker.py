from Multi_camera import multiProcess_camera
import multiprocessing as mp
import cv2, time
from Socket_io import socket_io
import atexit

image_path = "/home/vision/models/research/object_detection/Detected_images/"

#def exit_handler():
#    mulp.endprocess()
#atexit.register(exit_handler)


def video_process(q_list, frame_dict):
    for q in q_list:
        if q.qsize != 0:
            frame = q.get()
            for name, image in frame.items():
                frame_dict[name] = image
    return frame_dict


def image_saver(frame_dict):
    for name, image in frame_dict.items():
        image_name = '{}{}_{}.png'.format(image_path, name,
                                          time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime()))
        cv2.imwrite(image_name, image)
        print(f"Image Save to {image_name}")



def new_main(video_dic):
    mulp = multiProcess_camera(video_dic)
    socketp = socket_io()
    socket_q = socketp.run_socket()
    image_q = mulp.run_multi_camera()
    frame_dict = {}
    save_flag = False
    time.sleep(5)
    while True:
        if socket_q.qsize() != 0:
            data = socket_q.get()
            if str(data) == '1':
                print(f"Receive data: {data}")
                save_flag = True
        if save_flag:
            frame_dict = video_process(image_q, frame_dict)
            if len(frame_dict) == len(video_dic):
                image_saver(frame_dict)
                frame_dict.clear()
                save_flag = False

def main(video_dic):
    mulp = multiProcess_camera(video_dic)
    q_list = mulp.run_multi_camera()
    frame_list = []
    take_times = 0
    time.sleep(5)
    while True:
        if take_times < 5 :
            for q in q_list:
                if q.qsize != 0:
                    frame = q.get()
                    frame_list.append(frame)
            for camera_frame in frame_list:
                for name, image in camera_frame.items():
                    print(f"image:{image}")
                    image_name = '{}{}_{}.png'.format(image_path, name,
                                                      time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime()))
                    cv2.imwrite(image_name, image)
                    print(f"Image Save to {image_name}")
                take_times += 1
        else:
            break

    mulp.endprocess()


if __name__ == "__main__":
    cam_list = []
    video_dic = {}
    for cameras in range(11):
        cap = cv2.VideoCapture(cameras)
        #time.sleep(2)
        if cap.isOpened():
            cam_list.append(cameras)
            cap.release()
    for cam in cam_list:
        video_dic[f'cam{cam}'] = f"/dev/video{cam}"
    #video_dic = {"cam1": 'rtsp://admin:abc12345@10.15.202.186:554',
    #              "cam2": 'rtsp://admin:dh123456@10.15.202.177:554/'}
    print(f"cam_list:{cam_list}")
    mp.set_start_method('spawn')
    new_main(video_dic)
