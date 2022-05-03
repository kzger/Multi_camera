from Multi_camera import multiProcessone_camera
import multiprocessing as mp
import cv2, time

image_path = "/home/vision/models/research/object_detection/Detected_images/"

def main(video_dic):
    mulp = multiProcessone_camera(video_dic)
    q_list = mulp.run_multi_camera()
    frame_list = []
    take_times = 0
    while True:
        if take_times < 5 :
            for q in q_list:
                if q.qsize != 0:
                    frame = q.get()
                    frame_list.append(frame)
            for camera_frame in frame_list:
                for name, image in camera_frame.items():
                    image_name = '{}{}_{}.png'.format(image_path, name,
                                                      time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime()))
                    cv2.imwrite(image_name, frame)
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
        if cap.isOpened():
            cam_list.append(cameras)
    for cam in cam_list:
        video_dic[f'cam{cam}'] = f"/dev/video{cam}"
    # video_dic = {"cam1": 'rtsp://admin:abc12345@10.15.202.186:554',
    #              "cam2": 'rtsp://admin:dh123456@10.15.202.177:554/'}
    mp.set_start_method('spawn')
    main(video_dic)