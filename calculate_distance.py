import cv2
import time
from selenium import webdriver
import time

cd='C:\\Users\\theja\\Downloads\\chromedriver_win32\\chromedriver.exe'
driver=webdriver.Chrome(cd)


email = ""
password = ""

driver.get("https://www.tinkercad.com/dashboard")
time.sleep(2)

google = driver.find_element_by_xpath('//*[@id="content"]/div/main/ng-component/main/section/div/div/div/div/div[1]/a[2]/span[2]')
google.click()

driver.find_element_by_xpath('//*[@id="userName"]').send_keys(email)
user_next=driver.find_element_by_xpath('//*[@id="verify_user_btn"]')
user_next.click()  
time.sleep(2)

driver.find_element_by_xpath('//*[@id="password"]').send_keys(password)
pwd_next = driver.find_element_by_xpath('//*[@id="btnSubmit"]')
pwd_next.click()
time.sleep(5)

driver.get('https://www.tinkercad.com/things/h0l1AzcnbCn')
time.sleep(1)

#Tinker this
driver.find_element_by_xpath('//button[@class="btn btn-lg btn-primary"]').click()
time.sleep(2)

#Code
driver.find_element_by_id('CODE_EDITOR_ID').click()
time.sleep(2)

#Serial Monitor
driver.find_element_by_id('SERIAL_MONITOR_ID').click()
time.sleep(2)

#Simulate
driver.find_element_by_id('SIMULATION_ID').click()


# data
distance_cam_face =25 # in centimeters
face_length =18 #in centimeters

face_detector = cv2.CascadeClassifier(r'haarcascade_frontalface_default.xml') # changed path for face detector xml file

def get_focal_length(distance_cam_face, face_length, face_length_image):
    # finding focal length
    focal_length = (face_length_image* distance_cam_face)/face_length
    return focal_length

def get_distance(face_length, focal_Length, face_length_image):
   distance= (face_length * focal_Length)/face_length_image 
   return distance 


def get_face_length_in_image(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(gray_image, 1.3, 5)
    for face in faces:
        x=face[0]
        y=face[1]
        w=face[2]
        h=face[3]
        cv2.rectangle(image, (x,y), (x+w, y+h), (255,255,255), 5)
        f_length = h
        return f_length, image
reference_image =cv2.imread(r"C:\\Users\\theja\\Pictures\\Camera Roll\\WIN_20210902_09_10_55_Pro.jpg") # changed the ref image path
face_length_image, image = get_face_length_in_image(reference_image)
print("Face length in pixel is:", face_length_image)
cv2.imshow('reference_image',image)
cv2.waitKey(0)
cv2.destroyAllWindows()


focal_length =get_focal_length(distance_cam_face, face_length, face_length_image)
print("Focal length is:", focal_length)


cam = cv2.VideoCapture(0)
while True:
    retval, frame = cam.read()
    height, width, dim = frame.shape
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(gray, 1.3, 5)
    for face in faces:
        x=face[0]
        y=face[1]
        w=face[2]
        h=face[3]
        cv2.rectangle(frame, (x,y), (x+w, y+h), (255,255,255), 5)
        distance =get_distance(face_length, focal_length, h)
        print(distance)
        if distance <=50:
            #danger
            serial_input = driver.find_element_by_xpath('//div[@class="code_panel__serial__bottom js-code_panel__serial__bottom js-code_editor__serial-monitor__bottom clearfix"]/input')
            serial_input.send_keys(1) #  input high
            send = driver.find_element_by_xpath('//div[@class="code_panel__serial__bottom js-code_panel__serial__bottom js-code_editor__serial-monitor__bottom clearfix"]/div/a/div').click()
            time.sleep(0.5)
        else:
            #danger
            serial_input = driver.find_element_by_xpath('//div[@class="code_panel__serial__bottom js-code_panel__serial__bottom js-code_editor__serial-monitor__bottom clearfix"]/input')
            serial_input.send_keys(0) # input low
            send = driver.find_element_by_xpath('//div[@class="code_panel__serial__bottom js-code_panel__serial__bottom js-code_editor__serial-monitor__bottom clearfix"]/div/a/div').click()
            time.sleep(0.5)
        cv2.putText(frame, f" Distance = {distance}", (30,30),cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 3)

    frame_size = cv2.resize(frame,(100,100))
    cv2.imshow('frame', frame)

    if cv2.waitKey(1)==27:
        break
cam.release()
cv2.destroyAllWindows()
