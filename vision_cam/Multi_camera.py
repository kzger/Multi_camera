import multiprocessing as mp
import cv2

class multiProcess_camera(object):
    """
    data:2022-04-11
    use:採用多線程的方式來讀取攝像頭的視頻，模擬達到實時的效果
    """
    def __init__(self, video_dic):
        self.video_dic = video_dic
        self.processes = []


    def image_put(self, q, camera, name):
        cap = cv2.VideoCapture(camera)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 4000)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 3000)
        cap.set(cv2.CAP_PROP_FPS, 5)
        q_dict = {}
        while True:
            if cap.isOpened():
                if q.qsize() > 1:
                    q.get()
                ret, frame = cap.read()
                if ret:
                    frame = cv2.resize(frame, (2000, 1500))
                    q_dict[name] = frame
                    q.put(q_dict)
            else:
                print(f'camera:{camera}, Disconnected')
                break


    def run_multi_camera(self):          # 啓動服務
        queue_list = []
        for name, camera in self.video_dic.items():
            queue = mp.Queue(maxsize=2)
            # Test daemon
            tmp_p = mp.Process(target=self.image_put, args=(queue, camera, name, ))
            tmp_p.daemon = True
            self.processes.append(tmp_p)
            queue_list.append(queue)
            #[process.join() for process in self.processes]
        [process.start() for process in self.processes]
        return queue_list


    def endprocess(self):
        [process.terminate() for process in self.processes]
        [process.join() for process in self.processes]


def main(video_dic):
    mulp = multiProcess_camera(video_dic)
    q_list = mulp.run_multi_camera()                    # 啓動服務
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



if __name__=="__main__":
    video_dic = {"cam1": 'rtsp://admin:abc12345@10.15.202.186:554',
                 "cam2": 'rtsp://admin:dh123456@10.15.202.177:554/'}
    mp.set_start_method('spawn')
    main(video_dic)
