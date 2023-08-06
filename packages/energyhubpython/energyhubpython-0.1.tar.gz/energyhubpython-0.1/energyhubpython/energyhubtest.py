class Student:
	def __init__(self,name):
		self.name = name
		self.exp = 0
		self.lesson = 0
		#self.AddEXP(10) # Call function แค่สมัครเข้า class ก็ได้ exp = 10
 
	def Hello(self):
		print('สวัสดีจ้า...ผมชื่อ{}'.format(self.name))

	def Coding(self):
		print('{}: กำลังเขียนโปรแกรม...'.format(self.name))
		self.exp += 5
		self.lesson += 1

	def ShowEXP(self):
		print('--- {} มีประสบการณ์ {} EXP'.format(self.name,self.exp))
		print('--- เรียนไป {} ครั้งแล้ว'.format(self.lesson))

	def AddEXP(self,score):
		self.exp += score # self.exp = self.exp + 10
		self.lesson += 1

class SpecialScore:
	def __int__(self):
		self.score = 500

class SpecialStudent(Student):
	def __init__(self,name,father):
		super().__init__(name)
		self.father = father
		mafia = ['Bill Gates','Steve Job','Thomas Edison']
		if father in mafia:
			self.exp += 100
	def AddEXP(self,score):
		self.exp += (score*3) 
		self.lesson += 1
	def AskEXP(self,score=10):
		print ('--- ครู!!! ขอคะแนนพิเศษให้ผมหน่อยสิ {} EXP'.format(score))		
		self.AddEXP(score) 

if __name__ == '__main__': #ใช้สำหรับตรวจสอบว่าอยู่ในไฟล์ main หรือเปล่า ?

	print('=======2021, 1 Jan=======')
	student0 = SpecialStudent('Mark Zuckerberg','Bill Gates')
	student0.AskEXP()
	student0.ShowEXP()

	student1 = Student('Albert')
	print(student1.name)
	student1.Hello()
	print('----------------------')

	student2 = Student('Steve')
	print(student2.name)
	student2.Hello()
	print('----------------------')

	print('ตอนนี้ exp ของแต่ละคนได้เท่าไหร่กันแล้ว')
	student1.ShowEXP()
	student2.ShowEXP()

	print('=======2021, 2 Jan=======')
	print('---ใครอยากเรียนโค้ดดิ้ง ?---+10 exp---')
	student1.AddEXP(10)
	print('ตอนนี้ exp ของแต่ละคนได้เท่าไหร่กันแล้ว')
	student1.ShowEXP()
	student2.ShowEXP()

	print('=======2021, 3 Jan=======')
	print('ตอนนี้ exp ของแต่ละคนได้เท่าไหร่กันแล้ว')
	student1.ShowEXP()
	student2.ShowEXP()

	print('=======2021, 4 Jan=======')
	for i in range (5):
		student2.Coding()

	print('ตอนนี้ exp ของแต่ละคนได้เท่าไหร่กันแล้ว')
	student1.ShowEXP()
	student2.ShowEXP()