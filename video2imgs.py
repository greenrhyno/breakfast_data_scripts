import cv2 
import os

base_dir = '/home/ryangreen/projects/BreakfastII_15fps_qvga_sync'

def main():
    find_videos(base_dir)
    # delete_imgs(base_dir)

def find_videos(dir_path):
    for filename in os.listdir(dir_path):
        filepath = os.path.join(dir_path, filename)
        if os.path.isdir(filepath):
            find_videos(filepath)
        elif filename.endswith('.avi'):
            video2imgs(dir_path,filename)


def delete_imgs(dir_path):
    for filename in os.listdir(dir_path):
        filepath = os.path.join(dir_path, filename)
        if os.path.isdir(filepath):
            delete_imgs(filepath)
        elif filename.endswith('.jpg'):
            os.remove(filepath)


def video2imgs(parent_path, video_name):
    video_path = os.path.join(parent_path, video_name)
    vidcap = cv2.VideoCapture(video_path)
    success,image = vidcap.read()
    if not success:
        print('Could not read {}'.format(video_path))
        return
    frame_folder = os.path.join(parent_path, video_name[:-4])
    if not os.path.exists(frame_folder):
        os.mkdir(frame_folder)
    print(frame_folder)
    count = 0
    while success:
        frame_name = "{}_{}.jpg".format(video_name[:-4], str(count).zfill(6))
        cv2.imwrite(os.path.join(frame_folder, frame_name), image)     # save frame as JPEG file      
        success,image = vidcap.read()
        count += 1

if __name__ == "__main__":
    main()