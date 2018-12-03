import cv2
import time
import numpy as np
from keras.preprocessing import image
from keras.applications.resnet50 import preprocess_input
import tensorflow as tf
import keras
from keras.models import load_model

char = ['a','b','c','d','e','f','g','h','i','j','k','l',
               'm','n','o','p','q','r','s','t','u','v','w','x','y','z', 'nothing', 'nothing', 'nothing']
def show_webcam(mirror=False):
    model = load_model('modelv2.h5')
    cam = cv2.VideoCapture(0)
    res, score = '', 0.0
    while True:
        ret_val, img = cam.read()
        a = cv2.waitKey(1)
        if mirror: 
            img = cv2.flip(img, 1)
        if ret_val:
            x1, y1, x2, y2 = 100, 100, 500, 500
            img_cropped = img[y1:y2, x1:x2]
            image_data = cv2.imencode('.jpg', img_cropped)[1].tostring()
            #####

            np_img = np.fromstring(image_data, np.uint8)
            img_cropped = cv2.imdecode(np_img, cv2.IMREAD_COLOR)
            img_arr = cv2.resize(img, dsize=(64, 64), interpolation=cv2.INTER_CUBIC)
            #img_arr = image.img_to_array(img)
            x = np.expand_dims(img_arr, axis=0)
            x = preprocess_input(x)
            score = np.amax(model.predict(x, batch_size=1))
            res = char[model.predict_classes(x, batch_size=1)[0]]

            ####
        time.sleep(.05)
        cv2.putText(img, '%s' % (res.upper()), (100,600), cv2.FONT_HERSHEY_SIMPLEX, 4, (255,255,255), 4)
        cv2.putText(img, '(score = %.5f)' % (float(score)), (100,650), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255))
        cv2.rectangle(img, (x1, y1), (x2, y2), (255,0,0), 2)
        cv2.imshow("img", img)
            
        if cv2.waitKey(1) == 27: 
            break  # esc to quit

    cv2.destroyAllWindows()


def main():
    show_webcam(mirror=True)


if __name__ == '__main__':
    main()
