# -*- coding: utf-8 -*-
#school.py
class student:
    def __init__(self,name,lastname):
        self.name = name
        self.lastname = lastname
        self.exp = 0
        self.lesson = 0
        self.vehicle = 'รถเมลล์'
    @property#ใส่เพื่อไม่ต้องใส่วงเล็บเปิดปิด   
    def fullname(self):
        return '{} {}'.format(self.name,self.lastname)
    def Codeing(self):
        '''นี้คือคลาดสเรียนวิชาเขียนโปรแกรม'''
        self.addxp()
        print('{} กำลังเรียนเขียนโปรแกรม...'.format(self.fullname))
    def showxp(self):
        print('{} ได้คะแนน {} exp (เรียนไป {} ครั้ง)'.format(self.name,self.exp,self.lesson))
    def addxp(self):
        self.exp+=10
        self.lesson+=1
    def __str__(self):#แสดงผลที่อยู่ภายใน
        return self.fullname
    def __repr__(self):#ค่าในlistเห็นก้อนๆไป
        return self.fullname
    def __add__(self,other):
        return self.exp + other.exp

class special_student(student):
    def __init__(self,name,lastname,farther):
        super().__init__(name,lastname)
        self.father= farther
        self.vehicle= tesla()
        print('รู้ไหมฉันลูกใคร?.....!พ่อฉันชื่อ {}'.format(self.father))
    def addxp(self):#overwrite เฉพาะ super class
        self.exp+=30
        self.lesson+=2

class tesla:
    def __init__(self):
        self.model = 'Tesla Model S'
    def selfdriving(self,st):
        print('ระบบขับอัตโนมัติกำลังทำงาน....กำลังพาคุณ {} กลับบ้าน'.format(st.name))
    def __str__(self):
        return self.model
class teacher:
    def __init__(self,fullname):
        self.fullname = fullname
        self.student = []
    def checkstudent(self):
        print('-----------นักเรียนของ {}------------'.format(self.fullname))
        for i,st in enumerate(self.student):
           
            print('{} ---> {} [{} exp][เรียนไป {} ครั้ง]'.format(i+1,st.fullname,st.exp,st.lesson))
    def add_student(self,st):
        self.student.append(st)
    
# print('File:',__name__)
if __name__ == '__main__':
    
    #day0
    allstudent=[]
    teacher1 = teacher('Ada Lovelace')
    teacher2 = teacher('Bill Gates')
    print(teacher1.student)
    #day 1
    print('--------Day1------')
    st1 = student('Albert','Einstein')
    allstudent.append(st1)#สมัครเก็บไว้ในlist
    teacher1.add_student(st1)
    print(st1.fullname)


    #day2
    print('--------Day2------')
    st2= student('Thanapat','Wichiankanyarat')
    allstudent.append(st2)
    teacher2.add_student(st2)
    print(st2.fullname)

    #day3
    print('--------Day3------')
    for i in range(3):
        st1.Codeing()
    st2.Codeing()
    st1.showxp()
    st2.showxp()
    #day4
    print('--------Day4------')

    stp1 = special_student('Thomas','Edison','Hitler')
    allstudent.append(stp1)
    teacher1.add_student(stp1)
    print(stp1.fullname)
    print('คุณครูครับ ขอคะแนนฟรี 20 คะแนน')
    stp1.exp=20 #แก้ไขค่าในclass
    stp1.Codeing()
    stp1.showxp()

    print('--------Day5------')
    print('นักเรียนกลับบ้านยังไง?')
    print(allstudent)
    for st in allstudent:
        print('{} กลับบ้านด้วย {}'.format(st.name,st.vehicle))
        if isinstance(st,special_student):#isinstance เป็นการcheckว่า st อยู่ในคลาส special_student รึเปปล่า
            st.vehicle.selfdriving(st)#st.vechicle มาจาก class student self.vehicle ตัวselfคือ st ส่วน selfของ selfdriving คือ st.vehicle

    #day 6
    print('-----------Day6---------')
    teacher1.checkstudent()
    teacher2.checkstudent()
    print('รวมพลัง 2 คน {}'.format(st1+st2))

