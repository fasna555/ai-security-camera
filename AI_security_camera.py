# Goal
#
# Monitor webcam feed.
#
# If a person is detected:
#
# Person Detected!
#
# Save a snapshot automatically.

import cv2
from ultralytics import YOLO
from datetime import datetime


cap=cv2.VideoCapture(0)
model=YOLO('yolov8n.pt')

count=1
saved=False

while True:
    success,frame=cap.read()
    if not success:
        break
    results=model(frame)
    annotated=results[0].plot()

    person_detected=False
    for box in results[0].boxes:
        class_id = int(box.cls)
        name = model.names[class_id]
        if name == "person":
            person_detected=True
    if person_detected:
        print("person detected")
        current_time = datetime.now().strftime("%H:%M:%S")
        cv2.putText(annotated,"person detected",(50,100),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)
        cv2.putText(annotated,current_time,(50,150),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)

        if not saved:
            filename=f"person_{count}.jpg"
            cv2.imwrite(filename,annotated)
            print(filename,"saved")
            count+=1
            saved=True
    else:
        saved=False

    cv2.imshow("AI security camera",annotated)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
