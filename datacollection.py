import cv2
import os

cap = cv2.VideoCapture(0)  # open camera
counter = 0
folder = "Data"
os.makedirs(folder, exist_ok=True)

while True:   # <-- loop starts here
    success, img = cap.read()
    if not success:
        break

    cv2.imshow("Image", img)

    key = cv2.waitKey(1) & 0xFF  # listen for key press

    if key == ord('s'):   # save image
        counter += 1
        filename = os.path.join(folder, f"Image_{counter:04d}.jpg")
        cv2.imwrite(filename, img)
        print(f"✅ Saved: {filename}")

    elif key == ord('q'):  # quit loop
        print("🛑 Quitting...")
        break              # <-- inside while loop, so valid

# cleanup
cap.release()
cv2.destroyAllWindows()
cv2.waitKey(1)
