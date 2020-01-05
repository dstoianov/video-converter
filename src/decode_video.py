import os
import subprocess

from pymediainfo import MediaInfo

vcodec = "libx264"
crf = 23  # 23 default value, (lover better)
frame = 24

path = '/Users/dstoianov/Documents/convert-video'


def cmd(command):
    print(command)
    p = subprocess.Popen(command, shell=True)
    p.communicate()


def media_info(line_name):
    media_info = MediaInfo.parse(line_name)
    return media_info.tracks[1]


def main():
    root = path
    # root = os.path.dirname(os.path.abspath(__file__))
    # files = ["{}/{}".format(root, f) for f in os.listdir(path) if f.endswith('.mp4')]
    files = [f for f in os.listdir(root) if f.endswith('.mp4') and not f.endswith('-23.mp4')]
    for file in files:
        fps = float(media_info(path + '/' + file).frame_rate)
        if fps > 31:
            out = "{}_ffmpeg_{}_fps-{}.avi".format(file, vcodec, frame)
            print("{} is more than 31, will decode audio".format(fps))
            cmd("ffmpeg -i {} -hide_banner -c:v {} -preset slow -crf {} -r {} -c:a libmp3lame -aq 2 {}"
                .format(file, vcodec, crf, frame, out))
        else:
            out = "{}_ffmpeg_{}.avi".format(file, vcodec)
            print("{} is less than 31, will full copy audio".format(fps))
            # cmd("ffmpeg -i {}/{} -hide_banner -c:v {} -preset slow -crf {} -c:a copy {}/{}"
            cmd("ffmpeg -i {}/{} -hide_banner -c:v {} -preset slow -crf {} -codec:a aac -vbr 5 {}/{}"
                .format(root, file, vcodec, crf, root, out))

        before = media_info("{}/{}".format(root, file))
        after = media_info("{}/{}".format(root, out))
        print("Size was decreased in {} times".format(str(round(before.stream_size / after.stream_size, 1))))


if __name__ == "__main__":
    main()
    print("DONE!")
