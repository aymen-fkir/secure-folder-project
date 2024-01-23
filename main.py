import os
import sys
import face_recognition
import cv2
import os
from supabase import create_client
from dotenv import load_dotenv
import numpy as np
import json

class secure_folder:

    def __init__(self,folder_path: str,key: str,url: str) -> None:
        self.folder_path = folder_path
        self.key = key
        self.url = url
    
    #add a user to access the folder
    def AddUsers(self,username:str,extention:str)->list:
        supabase = create_client(self.url, self.key)
        cuurent_path = os.getcwd().replace('\\','/')
        full_fpath = f"{cuurent_path}/images/{username}.{extention}"
        image = face_recognition.load_image_file(full_fpath)
        face_encoding = face_recognition.face_encodings(image)
        arrays_dict = {f'arr_{i}': arr.tolist() for i, arr in enumerate(face_encoding)}
        json_object = json.dumps(arrays_dict,indent=4)
        responce = supabase.from_("encoded_images").insert({"username":username,"encoding":[json_object]}).execute()
        os.remove(full_fpath)
        return responce
    

    #download the npz from the data base
    def Getimage(self,user:str)-> json:
        supabase = create_client(self.url, self.key)
        data = supabase.from_("encoded_images").select("encoding").match({"username":user}).execute()
        return data
    
    #load the npz file
    #remove
    def loadencoded(self,username : str)->list:
        loaded_data = self.Getimage(username)
        data = loaded_data.data[0]
        encoded_image = json.loads(data["encoding"][0])
        
        loaded_list_of_arrays = [encoded_image[key] for key in encoded_image.keys()]
        loaded_list_of_arrays = [np.array(arr) for arr in loaded_list_of_arrays]        
        return loaded_list_of_arrays
    
    
    def take_pic(self) ->bool:
        cam = cv2.VideoCapture(0)
        result,image = cam.read()
        if result:
            cv2.imwrite("detected_pic.png",image)
        return result
            
    # detect if it the right user
    def detect_face(self,username) ->bool:
        result = self.take_pic()
        if result:
            face_encoding = self.loadencoded(username)
            unknown_image = face_recognition.load_image_file("detected_pic.png")

            try:
                unknown_face_encoding = face_recognition.face_encodings(unknown_image)[0]
            except IndexError:
                print("I wasn't able to locate any faces in at least one of the images. Check the image files. Aborting...")
                quit()

            results = face_recognition.compare_faces([face_encoding[0]], unknown_face_encoding)
            return results[0]
    
        else:
            return 401
        
    #check if user is allowed to folder
    def action(self,username:str) -> None:
        res = self.detect_face(username)
        if res != 401:
            if res:
                os.chdir(self.folder_path)
                if not os.path.exists("Locker"):
                    if not os.path.exists("Locker.{645ff040-5081-101b-9f08-00aa002f954e}"):
                        os.mkdir("Locker")
                    #unlock
                    else:
                        os.popen('attrib -h Locker.{645ff040-5081-101b-9f08-00aa002f954e}')
                        os.rename('Locker.{645ff040-5081-101b-9f08-00aa002f954e}',"Locker")
                        sys.exit()
                else:
                    #lock
                    os.rename("Locker",'Locker.{645ff040-5081-101b-9f08-00aa002f954e}')
                    os.popen('attrib +h Locker.{645ff040-5081-101b-9f08-00aa002f954e}')
                    sys.exit()
                print("Done")
            else:
                print("wrong password")
        else:
            print("There is no image been taken")
        return
        



load_dotenv()
url: str = os.getenv("project_url")
key: str = os.getenv("secret_key")
client = secure_folder("./",key,url)
client.action("USERNAME")

