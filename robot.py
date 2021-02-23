from bs4 import BeautifulSoup
import requests
import time
import re

idname = "xxxxxx"
passwd = "xxxxxx"

def login():
    url = "https://kiki.ccu.edu.tw/~ccmisp06/cgi-bin/class_new/bookmark.php"
    params = {'id':idname,'password':passwd}
    res = requests.post(url,params)
    #print(res.text)
    session_id = re.findall('session_id=(.*)">',res.text)[0]
    return session_id

def searchCourse(session_id,dept,grade,cge_cate,cge_subcate,course_page,course_tr):
    url = "https://kiki.ccu.edu.tw/~ccmisp06/cgi-bin/class_new/Add_Course01.cgi"
    params = {
        'session_id' : session_id,
        'dept' : dept,
        'grade' : grade,
        'cge_cate' : cge_cate,
        'cge_subcate': cge_subcate,
        'page' : course_page
    }
    res = requests.post(url,params)
    text = BeautifulSoup(res.text, 'html.parser')
    course_tr = text.findAll('table')[1].findAll('tr')[course_tr]
    remaining = course_tr.findAll('th')[2].text
    print(remaining)
    return int(remaining)

##cge_cate:1 basis :2 bouya
def selectCourse(session_id,dept,grade,cge_cate,cge_subcate,course_id,course_cate):
    url = "https://kiki.ccu.edu.tw/~ccmisp06/cgi-bin/class_new/Add_Course01.cgi"
    params = {
        'session_id' : session_id,
        'dept' : dept,
        'grade' : grade,
        'cge_cate' : cge_cate,
        'cge_subcate' : cge_subcate,
        'course' : course_id,
        course_id : course_cate,
        'SelectTag' : '1'
    }
    res = requests.post(url,params)
    #print(res.text)

if __name__ == "__main__":
    
    course_ids = ["7500022_01","7506007_01"]
    course_page = ["1","2"]
    course_tr = [9,6]
    '''
    steps
    1. login to access session_id
    2. search courses to see whether the course remains or not
    3. select the remaining course
    4. Got it
    '''

    while(1):
        #Login
        session_id = login()

        ##params
        dept = 'I001'
        grade = '1'
        cge_cate = '2'
        cge_subcate = '2'
        course_cate = '3'

        #SearchCourse & SelectCourse
        for index in range(len(course_ids)):
            remaining = searchCourse(session_id,dept,grade,cge_cate,cge_subcate,course_page[index],course_tr[index])
            if remaining == 0:
                selectCourse(session_id,dept,grade,cge_cate,cge_subcate,course_ids[index],course_cate)
                print('Have selected ' + course_ids[index])
                course_ids.remove(course_ids[index])
                course_page.remove(course_page[index])
                course_tr.remove(course_tr[index])
                break
        
        if len(course_ids) == 0:
            print("All courses are be selected!!!Congratulation!!!")
            break

        time.sleep(5)
