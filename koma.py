import  pygame 
import util


class Koma(object):
          
	def __init__(self,front_img_lst,dir_lst,pos,name,owner):
  
		
		self.name = name
		self.owner = owner

		self.dir_lst = dir_lst 

		self.width = 80
		self.height = 100

		self.nariFlag = False

		img = pygame.image.load(front_img_lst["player"])
		player_img = pygame.transform.scale(img,(self.width,self.height)) 

		img = pygame.image.load(front_img_lst["cpu"])
		cpu_img = pygame.transform.scale(img,(self.width,self.height)) 

		self.image_lst = {"player":player_img,"cpu":cpu_img}
		self.front_image = self.image_lst[self.owner]

		self.image = self.front_image

		self.posX = pos[0]
		self.posY = pos[1]

		self.rect = self.image.get_rect() 
		self.rect.x = 280+(self.posX-1) * self.width
		self.rect.y = (self.posY-1) * self.height
	
	def ownerChange(self,owner_name):
		self.owner = owner_name
		self.imageSwitch()
		
	def imageSwitch(self):
		self.front_image = self.image_lst[self.owner]
		self.image = self.front_image

	def getPos(self):	
		return [self.posX,self.posY]

	def posInit(self):	
		self.posX = -1		
		self.posY = -1		
		self.rect.x = -1
		self.rect.y = -1
	
	def posUpdate(self,pos):
		self.posX = pos[0]
		self.posY = pos[1]

		self.rect.x = 280+(self.posX - 1) * self.width
		self.rect.y = (self.posY - 1) * self.height

class Ou(Koma):
	def __init__(self,front_img_lst,dir_lst,pos,name,owner):
		Koma.__init__(self,front_img_lst,dir_lst,pos,name,owner)
class Fu(Koma):
	def __init__(self,front_img_lst,nari_img_lst,special_dir_lst,nari_dir_lst,pos,name,owner):
		self.special_dir_lst = special_dir_lst
		dir_lst = self.special_dir_lst[owner]

		Koma.__init__(self,front_img_lst,dir_lst,pos,name,owner)
		self.nari_dir_lst = nari_dir_lst

		img = pygame.image.load(nari_img_lst["player"])
		player_nari_img = pygame.transform.scale(img,(self.width,self.height)) 

		img = pygame.image.load(nari_img_lst["cpu"])
		cpu_nari_img = pygame.transform.scale(img,(self.width,self.height)) 

		self.nari_image_lst = {"player":player_nari_img,"cpu":cpu_nari_img}
		
		self.nari_image = self.nari_image_lst[self.owner]
		
	def turn(self):
		if self.image == self.front_image:
			self.image = self.nari_image
               	else: self.image = self.front_image
	
	def nari(self):
		self.nariFlag = True
		self.turn()
		self.dir_lst = self.nari_dir_lst
		
	def imageSwitch(self):
		self.front_image = self.image_lst[self.owner]
		self.image = self.front_image

		self.nari_image = self.nari_image_lst[self.owner] 

	def dirChange(self):
		self.dir_lst = self.special_dir_lst[self.owner]

	def ownerChange(self,owner_name):
		self.owner = owner_name
		self.imageSwitch()
		self.dirChange()
		self.nariFlag = False

