(Most opp) นี่คือตัวอย่างโปรแกรมสำหรับการเรียน OOP
==================================================

วิธีติดตั้ง
~~~~~~~~~~~

เปิด CMD / Terminal

.. code:: python

    pip install mostoop

วิธีใช้
~~~~~~~

[STEP 1] - เปิด IDLE ขึ้นมาแล้วพิมพ์...

.. code:: python

    from mostoop import student,special_student,tesla,teacher
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

พัฒนาโดย: Thanapat Wichiankanyarat FB:
https://www.facebook.com/thanapat.wichiankanyarat/
