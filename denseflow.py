import cv2
import numpy as np
import cv2 
import os

base_dir = '/home/ryangreen/projects/BreakfastII_15fps_qvga_sync'
test_dir = '/home/ryangreen/projects/BreakfastII_15fps_qvga_sync/P03/cam01'
test_vid = 'P03_cereals.avi'

def main():
    # extract_flow(test_dir, test_vid)
    find_videos(base_dir)
    
def find_videos(dir_path):
    for filename in os.listdir(dir_path):
        filepath = os.path.join(dir_path, filename)
        if os.path.isdir(filepath):
            find_videos(filepath)
        elif filename.endswith('.avi'):
            extract_flow(dir_path,filename)

    # cv2.destroyAllWindows()


def extract_flow(parent_path, video_name):
    video_path = os.path.join(parent_path, video_name)
    cap = cv2.VideoCapture(video_path)
    ret, frame1 = cap.read()

    if not ret:
        print('Could not read {}'.format(video_path))
        return
    frame_folder = os.path.join(parent_path, "{}_flow".format(video_name[:-4]))
    if not os.path.exists(frame_folder):
        os.mkdir(frame_folder)
    else:
        print("Skipping {}".format(frame_folder))
        return
    print(frame_folder)

    prvs = cv2.cvtColor(frame1,cv2.COLOR_BGR2GRAY)
    hsv = np.zeros_like(frame1)
    # hsv[...,1] = 255

    count = 0
    frame2 = frame1

    while(ret):
        # convert to grayscale
        next = cv2.cvtColor(frame2,cv2.COLOR_BGR2GRAY)
        # compute flow
        flow = cv2.calcOpticalFlowFarneback(prvs,next, None, 0.5, 3, 15, 3, 5, 1.2, 0)
        flow = np.clip(flow, -20, 20) / 20

        # mag, ang = cv2.cartToPolar(flow[...,0], flow[...,1])
        # hsv[...,0] = ang*180/np.pi/2
        # hsv[...,2] = cv2.normalize(mag,None,0,255,cv2.NORM_MINMAX)
        # rgb = cv2.cvtColor(hsv,cv2.COLOR_HSV2BGR)

        # hsv[..., 0] = flow[...,0]
        # hsv[..., 1] = flow[...,1]

        # frame_name = "{}_{}_flow.jpg".format(video_name[:-4], str(count).zfill(6))
        # cv2.imwrite(os.path.join(frame_folder, frame_name), hsv)

        frame_name = "{}_{}_flow.npy".format(video_name[:-4], str(count).zfill(6))
        np.save(os.path.join(frame_folder, frame_name), flow)
        
        prvs = next
        ret, frame2 = cap.read()
        count += 1

    cap.release()


if __name__ == "__main__":
    main()
