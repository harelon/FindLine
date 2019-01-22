import cv2
import numpy
import os
import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='take pictures of line')
    parser.add_argument(
        '--height',
        help='the height of the image taken',
        required=True
    )
    args = parser.parse_args()
    dirName = "output " + str(args.height)
    if not os.path.exists(dirName):
        os.mkdir(dirName)
        print("Directory ", dirName, " Created ")
    else:
        print("Directory ", dirName, " already exists")

    width = 640
    height = 480
    fps = 30
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = None

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    cap.set(cv2.CAP_PROP_FPS, fps)

    picture_counter = 0
    video_counter = 0
    MiddleOfRecording = False
    while True:
        ret, frame = cap.read()
        cv2.imshow("frame", frame)
        char = cv2.waitKey(1) & 0xFF
        if char == ord('p'):
            print("taking a picture")
            cv2.imwrite(
                dirName+os.path.sep + "img" +
                str(picture_counter) + ".jpg", frame
                )
            picture_counter = picture_counter + 1
        if char == ord('v'):
            if not MiddleOfRecording:
                print("started recording video")
                out = cv2.VideoWriter(
                    dirName + os.path.sep + 'output' + str(video_counter) +
                    '.avi', fourcc, fps, (width, height)
                    )
                video_counter = video_counter + 1
                MiddleOfRecording = True
            elif MiddleOfRecording:
                out.release()
                MiddleOfRecording = False
                print("stopped recording video")
        if char == ord('q'):
            print("quitting")
            break
        if MiddleOfRecording:
            out.write(frame)
    cap.release()
    cv2.destroyAllWindows()
