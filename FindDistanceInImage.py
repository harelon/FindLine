import cv2
import numpy
import argparse
import math


PixToDegree = 12.2


def mark_rectangle(event, x, y, flags, param):
    global orig_image
    global image
    global mark
    if event == cv2.EVENT_LBUTTONDOWN:
        if not mark:
            image = orig_image.copy()
            # clear the image from the rectangle
            mark = True
            # next time mark the rectangle
            return
        image = cv2.rectangle(
            image, (image_half_x, image_half_y),
            (x, y), (0, 255, 0), 1
            )
        # put rectangle on cloned image
        mark = False
        # next time remove the rectangle
        line_latitude_angle_to_camera = (y - image_half_y) / PixToDegree
        # the line latitude angle is the y of its middle
        # divided by the pixels to degree ratio
        # because the camera center is parallel to the floor
        # it is the same angle as the line middle y of the center
        # to the camera
        line_latitude_angle_to_camera = math.radians(
            line_latitude_angle_to_camera
            )
        # the tangens function in python
        # returns value as if the angle was in radians
        # so we need to convert it to radians to get valid results
        height_to_distance_ratio = math.tan(line_latitude_angle_to_camera)
        # this is the ratio between the height to the distance to the line
        distance = float(height) / height_to_distance_ratio
        # the distance equals the height
        # divided to the ratio of the height to distance
        print(distance)
        # show the distance calculated


def setup():
    global orig_image
    global image
    global image_half_y
    global image_half_x
    global mark
    orig_image = cv2.imread(argparser())
    # instantiate the original image
    image = orig_image.copy()
    # instantiate the image rectangles will be printed on
    image_half_y = int(orig_image.shape[0]/2)
    # the middle row of the image
    image_half_x = int(orig_image.shape[1]/2)
    # the middle column of the image
    mark = True
    # next time mark on the picture


def argparser():
    global height
    parser = argparse.ArgumentParser(
            description='An image white line will be detected in'
            )
    # we need a parser
    # to run the program from command line and select one of the photos we took

    parser.add_argument(
            'image',
            help='the path of the image'
        )
    # we need an image path argument to know on what to apply the program
    parser.add_argument(
            'height',
            help='the height to base the distance on'
        )
    args = parser.parse_args()
    # convert the arguments into something we can use

    image_path = args.image
    # reads the args image paramater into image_path
    height = args.height
    # reads the height the image was taken from
    return image_path


if __name__ == "__main__":
    global image
    setup()
    # setup variables
    cv2.namedWindow("image")
    # create a constant window the image will be showed on
    cv2.setMouseCallback("image", mark_rectangle)
    # create on click handling function
    while True:
        # constantly show image
        cv2.imshow("image", image)
        # show image
        if cv2.waitKey(1) == ord('q'):
            break
            # wait for q press to exit code
