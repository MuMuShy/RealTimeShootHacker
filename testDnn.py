import numpy as np
import cv2
import time
from windowcapture import WindowCapture
print("[INFO] loading model...")
net = cv2.dnn.readNetFromCaffe("./models/face/pose_deploy.prototxt", "./models/face/pose_iter_116000.caffemodel")
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
# initialize the video stream and allow the cammera sensor to warmup

print(cv2.cuda.getCudaEnabledDeviceCount())
wincap = WindowCapture('Apex Legends')
while (True):
    # Capture frame-by-frame
    img = wincap.get_screenshot()
    print("start...")
    start = time.time()

    blob = cv2.dnn.blobFromImage(img)
    net.setInput(blob)
    detections = net.forward()
    end = time.time()
    seconds = end - start
    print("Time taken : {0} seconds".format(seconds))
    # Calculate frames per second
    fps = 1 / seconds;
    print("Estimated frames per second : {0}".format(fps));

    # loop over the detections
    for i in range(0, detections.shape[2]):
        # extract the confidence (i.e., probability) associated with the
        # prediction
        confidence = detections[0, 0, i, 2]

        # filter out weak detections by ensuring the `confidence` is
        # greater than the minimum confidence
        if confidence < 0.5:
            continue
        # compute the (x, y)-coordinates of the bounding box for the
        # object
        box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
        (startX, startY, endX, endY) = box.astype("int")

        # draw the bounding box of the face along with the associated
        # probability
        text = "{:.2f}%".format(confidence * 100)
        y = startY - 10 if startY - 10 > 10 else startY + 10
        cv2.rectangle(img, (startX, startY), (endX, endY),
                      (0, 0, 255), 2)
        cv2.putText(img, text, (startX, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)

    # Display the resulting frame
    cv2.imshow("Frame", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()