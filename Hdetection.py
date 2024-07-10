import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from traceback import print_exc
import cv2
# import pytesseract
from gspread import service_account
from IPython.display import Image
import webbrowser
import easyocr




class DemoFind():
    def locate(self):
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        driver.get("http://192.168.249.190/")
        text = driver.find_element(By.XPATH, "/html/body/center/p").text
        return text

# sa = service_account()
# sheet = sa.open('ANPR_DB')
# wks = sheet.sheet1

def equalizeHistColor(frame):
    # equalize the histogram of color image
    img = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)  # convert to HSV
    img[:,:,2] = cv2.equalizeHist(img[:,:,2])     # equalize the histogram of the V channel
    return cv2.cvtColor(img, cv2.COLOR_HSV2RGB)

find=DemoFind()
while True:
    var = find.locate()
    if var == "Vehicle Detected":
        webcam = cv2.VideoCapture(0)
        check, frame = webcam.read()
        # sa = service_account()
        # sheet = sa.open('ANPR_DB')
        # wks = sheet.sheet1
        sa = service_account()
        sheet = sa.open('ANPR_DB')
        wks = sheet.sheet1
        wks2 = sa.open("ANPR_DB").get_worksheet(1)
        l=wks2.get_all_values()
        print(l)
        try:
            i = int(wks.get_all_values()[-1][0])+1 
        except:
            i = 1
        while True:
            try:
                check, frame = webcam.read()
                cv2.imshow("Capturing", frame)
                cv2.waitKey(1)
                time.sleep(7) 
                cv2.imwrite(filename='saved_img_'+str(i)+'.png', img=frame)
                webcam.release()
                img_new = cv2.imread('saved_img_'+str(i)+'.png', cv2.IMREAD_GRAYSCALE)
                img = cv2.imread('saved_img_'+str(i)+'.png')
                img = cv2.resize(img, (600, 360))
                # print(pytesseract.image_to_string(img_new))
                cv2.imshow('Result', img_new)
                cv2.waitKey(1)
                img_new = equalizeHistColor(frame)
                img_new = cv2.imshow("Captured Image", img_new)
                # output = pytesseract.image_to_string(img_new)
                # print("".join(output.upper().split()))
                # print(output)
                cv2.waitKey(1)
                cv2.destroyAllWindows()
                print("Processing image...")
                img_ = cv2.imread('saved_img_'+str(i)+'.png', cv2.IMREAD_ANYCOLOR)
                print("Converting RGB image to grayscale...")
                gray = cv2.cvtColor(img_, cv2.COLOR_BGR2GRAY)
                print("Converted RGB image to grayscale...")
                print("Resizing image to 256x256 scale...")
                img_ = cv2.resize(gray,(256,256))
                img_resized = cv2.imwrite(filename='saved_img_'+str(i)+'final'+'.png', img=img_)
                print("Image saved!")
                # output = pytesseract.image_to_string(img_new)
                # print("".join(output.upper().split()))
                # print(output)
                reader=easyocr.Reader(['en'])
                Image('saved_img_'+str(i)+'_final'+'.png')
                output=reader.readtext('saved_img_'+str(i)+'_final'+'.png')
                Allflag = "Vehicle not Authorized"
                for j in l:
                    if "".join(output.upper().split()) in j:
                        Allflag="Vehicle Authorized"
                        webbrowser.open("http://192.`68.249.190/P")
                        break
                    else:
                        Allflag="Vehicle not Authorized"
                print(Allflag)
                print("DETECTED NUMBER PLATE :","".join(output.upper().split())) #output[0][1]
                flag=input("do you want to flag this image? (y/n):")
                wks.append_row((i, 'saved_img_'+str(i)+'_final'+'.png',"".join(output.upper().split()),Allflag,flag)) #output[0][1]
                cv2.destroyAllWindows()
                break  
            except(KeyboardInterrupt):
                print("Turning off camera.")
                webcam.release()
                print("Camera off.")
                print("Program ended.")
                cv2.destroyAllWindows()
                break
    else:
        continue