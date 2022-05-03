from Multi_camera import multiProcessone_camera
import multiprocessing as mp
import cv2

def main(video_dic):
    mulp = multiProcessone_camera(video_dic)
    q_list = mulp.run_multi_camera()
    frame_list = []
    while True:
        for q in q_list:
            if q.qsize != 0:
                frame = q.get()
                frame_list.append(frame)
        for camera_frame in frame_list:
            for name, image in camera_frame.items():
                cv2.imshow(f'{name}', image)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    mulp.endprocess()


if __name__ == "__main__":
    video_dic = {"cam1": 'rtsp://admin:abc12345@10.15.202.186:554',
                 "cam2": 'rtsp://admin:dh123456@10.15.202.177:554/'}
    mp.set_start_method('spawn')
    main(video_dic)