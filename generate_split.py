import os 
import argparse
import math
import sys

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-total', type=float, default=1.)
    parser.add_argument('-train', type=float, default=.8)
    parser.add_argument('-offset', type=float, default=0.)
    parser.add_argument('-save_dir', type=str, default='/home/ryangreen/projects/breakfast_splits')
    parser.add_argument('-root', type=str, default='/home/ryangreen/projects/BreakfastII_15fps_qvga_sync')
    parser.add_argument('-verbose', type=bool, default=True)
    
    args = parser.parse_args()
    print("Generating Split for " + args.root)
    print("Total {}, Train {}, Offset {}".format(args.total, args.train, args.offset))

    video_list = find_videos(args.root, args.root)
    video_list = sorted(unique(video_list))

    train, test = gen_lists(video_list, args.total, args.offset, args.train)
    
    name = 'split_{}_{}_{}'.format(per(args.train), per(args.total), per(args.offset))
    save_list(train, args.save_dir, name, 'train')
    save_list(test, args.save_dir, name, 'test')
    print("Finished")
      
def unique(list1): 
    # insert the list to the set 
    list_set = set(list1) 
    # convert the set to the list 
    return (list(list_set))

def per(num):
    return str(int(num * 100))

def gen_lists(master, total, offset, train):
    n_videos = math.floor(len(master) * total)
    start = math.floor(len(master) * offset)
    n_train = round(n_videos * train)

    tr = []
    tst = []
    idx = start
    for i in range(n_train):
        idx = idx % len(master)
        tr.append(master[idx])
        idx += 1
    for i in range(n_videos - n_train):
        idx = idx % len(master)
        tst.append(master[idx])
        idx += 1
    
    assert len(unique(tr + tst)) == n_videos
    return tr, tst


def save_list(my_list, path, name, ext):
    with open(os.path.join(path, name + '.' + ext), 'w') as f:
        for item in my_list:
            f.write("%s\n" % item)

def find_videos(dir_path, root):
    videos_subdirs = []
    videos_here = []
    for filename in os.listdir(dir_path):
        filepath = os.path.join(dir_path, filename)
        if os.path.isdir(filepath) and not filepath.endswith('_flow') and not os.path.exists(filepath + '.avi'):
            videos_subdirs = videos_subdirs + find_videos(filepath, root)
        elif filename.endswith('.avi'):
            videos_here.append(os.path.relpath(filepath[:-4], root))
    return videos_here + videos_subdirs


if __name__ == "__main__":
    main()