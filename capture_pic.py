import cv2
from matplotlib import pyplot as plt
import configparser


class CapturePic:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('settings.ini')
        self.camera_picker = int(config['Camera']['camera_picker'])

        self.imageWidth = int(config['Camera']['image_width'])
        self.imageHeight = int(config['Camera']['image_height'])

        # CAP_PROP_EXPOSURE Exposure Time
        # -4       80 ms
        # -5       40 ms
        # -6       20 ms
        self.exposureTime = -5
        # self.focus = 5  # min: 0, max: 255, increment:5

    def capture_pic(self):
        # zero is usually the built in webcam, 1 is the external cam
        camera = cv2.VideoCapture(self.camera_picker, cv2.CAP_DSHOW)
        camera.set(cv2.CAP_PROP_EXPOSURE, self.exposureTime)
        camera.set(cv2.CAP_PROP_FRAME_WIDTH, self.imageWidth)
        camera.set(cv2.CAP_PROP_FRAME_HEIGHT, self.imageHeight)
        # camera.set(cv2.CAP_PROP_AUTOFOCUS, 0)
        # camera.set(cv2.CAP_PROP_FOCUS, self.focus)
        # camera.set(cv2.CAP_PROP_SETTINGS, 1)
        # time.sleep(10)
        return_value, image = camera.read()
        camera.release()
        cv2.destroyAllWindows()
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        return rgb_image

    def save_pic(self, image, filename):
        cv2.imwrite(filename, cv2.cvtColor(image, cv2.COLOR_RGB2BGR))

    def display_pics(self, pics, titles):
        for i in range(len(pics)):
            plt.subplot(1, len(pics), i + 1), plt.imshow(pics[i])
            plt.title(titles[i]), plt.xticks([]), plt.yticks([])
        plt.show()

    # Use this function to find your camera's max resolution
    # https://en.wikipedia.org/wiki/List_of_common_resolutions
    def set_res(self, x, y):
        cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, int(x))
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, int(y))
        print(
            str(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) + " " +
            str(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
        return_value, image = cap.read()
        cap.release()
        cv2.destroyAllWindows()
        cv2.imshow("Image", image)
        cv2.waitKey(0)
        return str(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), str(
            cap.get(cv2.CAP_PROP_FRAME_HEIGHT))


if __name__ == '__main__':
    cp = CapturePic()
    # cp.set_res(3000, 2100)
    image = cp.capture_pic()
    cp.display_pics([image, ], ['Image', ])
    cp.save_pic(image, 'image.png')
