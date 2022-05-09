import multiprocessing as mp
import cv2
import time

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
                    #frame = cv2.resize(frame, (2000, 1500))
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
    q_list = mulp.run_multi_camera()
    time.sleep(5)
    name_list = []
    for name, item in video_dic.items():
        name_list.append(name)
    frame_list = []
    choice = 0
    while True:
        for q in q_list:
            if q.qsize != 0:
                frame = q.get()
                #frame_list.append(frame)
                for name, image in frame.items():
                    if name == name_list[choice]:
                        image = cv2.resize(image, (640, 480))
                        cv2.imshow("windows", image)
                key = cv2.waitKey(10)
                if key & 0xFF == ord('q'):
                    break
                # Hsu Edited
                elif key & 0xFF == ord('n'):
                    if choice < len(name_list)-1:
                        choice += 1
                    else: choice = 0
                    print(f"Switch to Camera {name_list[choice]}")
                elif key & 0xFF == ord('1'):
                   cv2.destroyAllWindows()
                   choice = 0
                elif key & 0xFF == ord('2'):
                   cv2.destroyAllWindows()
                   choice = 1
                elif key & 0xFF == ord('3'):
                   cv2.destroyAllWindows()
                   choice = 2
                elif key & 0xFF == ord('4'):
                   cv2.destroyAllWindows()
                   choice = 3
                elif key & 0xFF == ord('5'):
                   cv2.destroyAllWindows()
                   choice = 4


    mulp.endprocess()



if __name__=="__main__":
    cam_list = []
    video_dic = {}
    for cameras in range(5):
        cap = cv2.VideoCapture(cameras)
        if cap.isOpened():
            cam_list.append(cameras)
            cap.release()
    for cam in cam_list:
        video_dic[f'cam{cam}'] = f"/dev/video{cam}"
    print(f"cam_list:{cam_list}")
    mp.set_start_method('spawn')
    main(video_dic)
