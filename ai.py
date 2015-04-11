import random 
import copy
import util 
import koma as syougi_koma 

def testPrint():
	print "it is si module"

class AI(object):
	def __init__(self,cpu):
		self.cpu = cpu
		self.motigoma = self.cpu.motigoma

		self.name = self.cpu.name
		self.enemyName = "player"

	def searchOu(self,ban,fn):
		for vlst in ban.field:
			for val in vlst:
				if not(util.isZero(val)):
					#king?
					if isinstance(val,syougi_koma.Ou) and fn(val):
						return val
		return False

	def searchEnemyOu(self,ban):	
		return self.searchOu(ban,lambda val:val.owner != self.name)

	def searchSelfOu(self,ban):	
		return self.searchOu(ban,lambda val:val.owner == self.name)

	def collectSelfKoma(self,ban):
		koma_lst = util.collectKoma(ban,self.name)	
		return koma_lst

	def collectEnemyKoma(self,ban):
		koma_lst = util.collectKoma(ban,self.enemyName)	
		return koma_lst
	
	def eachMoveablePos(self,ban,koma_lst,owner_name):
		each_lst = []
		for koma in koma_lst:
			 pos_lst = util.collectMoveablePos(ban,koma,owner_name)
			 each_lst.append({"koma":koma,"pos_lst":pos_lst})

	 	return each_lst

	def eachCommandingPos(self,ban,koma_lst,owner_name):
		each_lst = []
		for koma in koma_lst:
			 pos_lst = util.collectCommandingPos(ban,koma,owner_name)
			 each_lst.append({"koma":koma,"pos_lst":pos_lst})

	 	return each_lst

	def canKillOu(self,ban):
		ou = self.searchEnemyOu(ban)
		ou_posX = ou.posX
		ou_posY = ou.posY
		koma_lst = self.collectSelfKoma(ban)
		each_lst = self.eachMoveablePos(ban,koma_lst,self.name)
	
		for dict in each_lst:
			koma = dict["koma"]
			pos_lst = dict["pos_lst"]
			for pos in pos_lst:		
				if pos[0] == ou.posX and pos[1] == ou.posY:
					return util.infoDict(koma,pos,False)
		return False	

	def canTry(self,ban):
		ou = self.searchSelfOu(ban)
		pos_lst = util.collectMoveablePos(ban,ou,self.name)
		for pos in pos_lst:
			if pos[1] == self.cpu.nari_posY:
				return util.infoDict(ou,pos,False)
		return False

	def isChecked(self,ban,ou,each_lst):
		for komaDict in each_lst:
			enemyMoveablePos_lst = komaDict["pos_lst"]
			enemyKoma = komaDict["koma"]
			for enemyMoveablepos in enemyMoveablePos_lst:		
				if enemyMoveablepos[0] == ou.posX and enemyMoveablepos[1] == ou.posY:
					return enemyKoma
		return False

	def has(self,pos_lst,checkPos):
		for pos in pos_lst:
			if util.isEqual(pos,checkPos):
				return True
		return False

	def removeDengerusPos(self,pos_lst,ban):
		enemy_koma_lst = self.collectEnemyKoma(ban)
		enemy_each_lst = self.eachCommandingPos(ban,enemy_koma_lst,self.enemyName)
		enemy_commanding_lst = self.appendEachMoveablePos(ban,enemy_each_lst) 
		print 'commanding pos'
		print enemy_commanding_lst

		temp_pos_lst =copy.deepcopy(pos_lst);
		print 'temp_pos_lst'
		print temp_pos_lst

		for pos in pos_lst:
			for enemy_commanding_pos in enemy_commanding_lst:
				if util.isEqual(pos,enemy_commanding_pos):	
					temp_pos_lst.remove(pos)
					break
		print 'new pos_lst'
		print temp_pos_lst
		return temp_pos_lst

	def getEscapLst(self,ban,ou,each_lst,ou_moveable_lst):
		ou_posX = ou.posX
		ou_posY = ou.posY

		for dict in each_lst:
			pos_lst = dict["pos_lst"]
			for pos in pos_lst:		
				if self.has(ou_moveable_lst,pos):
					ou_moveable_lst.remove(pos)
		return ou_moveable_lst

	def escapeOu(self,ban):
		ou = self.searchSelfOu(ban)

		koma_lst = self.collectEnemyKoma(ban)
		each_lst = self.eachMoveablePos(ban,koma_lst,self.enemyName)
		ou_moveable_lst = util.collectMoveablePos(ban,ou,self.name)

		if self.isChecked(ban,ou,each_lst):
			#escape_lst = self.getEscapLst(ban,ou,each_lst,ou_moveable_lst)
			escape_lst = self.removeDengerusPos(ou_moveable_lst,ban)
			if escape_lst != []:
			        rand_num = random.randint(0,len(escape_lst)-1)	
				return util.infoDict(ou,escape_lst[rand_num],False)
			else: return False
	        else:return False

	def searchKillable(self,targetKoma,each_lst):
		killable_lst = []
		for dict in each_lst:
			pos_lst = dict["pos_lst"]
			koma = dict["koma"]
			for pos in pos_lst:
				if pos[0] == targetKoma.posX and pos[1] == targetKoma.posY:
					killable_lst.append({"koma":koma,"pos":pos})
					break
		return killable_lst

	def hasOu(self,killable_lst):
		for dict in killable_lst:
			pos = dict["pos"]
			koma = dict["koma"]
			if isinstance(koma,syougi_koma.Ou):
				return dict
		return False

	def isCommandedKoma(self,ban,targetKoma):
		enemy_koma_lst = self.collectEnemyKoma(ban)
		enemy_each_lst = self.eachCommandingPos(ban,enemy_koma_lst,self.enemyName)
		enemy_commanding_lst = self.appendEachMoveablePos(ban,enemy_each_lst) 
		for commanding_pos in enemy_commanding_lst:
			#commanding?
			if(util.isEqual(commanding_pos,(targetKoma.posX,targetKoma.posY))):
				return True
		#don't commanding
		return False

	def isCommandedPos(self,ban,targetPos):
		enemy_koma_lst = self.collectEnemyKoma(ban)
		enemy_each_lst = self.eachCommandingPos(ban,enemy_koma_lst,self.enemyName)
		enemy_commanding_lst = self.appendEachMoveablePos(ban,enemy_each_lst) 
		for commanding_pos in enemy_commanding_lst:
			#commanding?
			if(util.isEqual(commanding_pos,targetPos)):
				return True
		#don't commanding
		return False


	#kill checking koma
	def killChecker(self,ban):
		ou = self.searchSelfOu(ban)

		enemy_koma_lst = self.collectEnemyKoma(ban)
		self_koma_lst = self.collectSelfKoma(ban)

		enemy_each_lst = self.eachMoveablePos(ban,enemy_koma_lst,self.enemyName)
		self_each_lst = self.eachMoveablePos(ban,self_koma_lst,self.name)

		ou_moveable_lst = util.collectMoveablePos(ban,ou,self.name)

		checking_koma = self.isChecked(ban,ou,enemy_each_lst)
		if checking_koma:
			killable_lst = self.searchKillable(checking_koma,self_each_lst)
			killableOuDict = self.hasOu(killable_lst)
			
			#commanded checking_koma's pos?
			if(self.isCommandedKoma(ban,checking_koma)):
				#ou cant't kill cheker,so remove ou killable dict 
				print "ou can't kill cheker"
				killable_lst.remove(killableOuDict)

			if killable_lst != []:
				#if killable more than 1 remove ou
				#if killableOuDict and len(killable_lst)>1:
			        rand_num = random.randint(0,len(killable_lst)-1)	

				killable_dict = killable_lst[rand_num]
				killable_koma = killable_dict["koma"]
				killable_pos = killable_dict["pos"]

				return util.infoDict(killable_koma,killable_pos,False)
			else: return False
	        else:return False
	        
	def selectFromBan(self,ban):	
		koma_lst = util.collectKoma(ban,"cpu")
		rand_num = random.randint(0,len(koma_lst)-1)

		return koma_lst[rand_num]
	
	def selectFromMotigoma(self):	
		koma_lst = self.motigoma.koma_lst
		rand_num = random.randint(0,len(koma_lst)-1)

		return koma_lst[rand_num]

	def selectKoma(self,ban):
		if self.motigoma.koma_lst == []:
			koma =	self.selectFromBan(ban)
		else:
			rand_num = random.randint(0,1)
			if rand_num == 0:
				koma =	self.selectFromBan(ban)
			else:	koma =	self.selectFromMotigoma()

		return koma

	def selectField(self,ban,koma,motigoma_flag):
		if motigoma_flag == False:
			#collect pos that empty or cpu's koma excists
			pos_lst = util.collectMoveablePos(ban,koma,"cpu")
		else:	
			#collect pos that empty
			pos_lst = util.collectPos(ban,lambda val:val == 0)
		
		if pos_lst == []:
			return False
		else:
			rand_num = random.randint(0,len(pos_lst)-1)
			return pos_lst[rand_num]

	def appendEachMoveablePos(self,ban,enemy_each_lst):
		appended_lst = []
		for dict in enemy_each_lst:
				pos_lst = dict["pos_lst"]
				for pos in pos_lst:
					appended_lst.append(pos)
		return appended_lst
		
	
	def selectSafetyField(self,ban,koma,motigoma_flag):
		if motigoma_flag == False:
			#collect pos that empty or cpu's koma excists
			pos_lst = util.collectMoveablePos(ban,koma,"cpu")
		else:	
			#collect pos that empty
			pos_lst = util.collectPos(ban,lambda val:val == 0)

		if pos_lst == []:
			return False
		pos_lst = self.removeDengerusPos(pos_lst,ban)

		if pos_lst == []:
			return False
		else:
			rand_num = random.randint(0,len(pos_lst)-1)
			return pos_lst[rand_num]
			
	def randomSelect(self,ban):
		while 1:
			koma = self.selectKoma(ban)
	
			if self.motigoma.is_excist(koma):
				motigoma_flag = True
			else:   motigoma_flag = False

			pos = self.selectField(ban,koma,motigoma_flag)
			#if dengerous action of ou,retry selecting
			if isinstance(koma,syougi_koma.Ou) and self.isCommandedPos(ban,pos):
				continue

			if pos != False:
				break
	        
		return util.infoDict(koma,pos,motigoma_flag)

	def safetyRandomSelect(self,ban):
		for koma in self.collectSelfKoma(ban):
	
			if self.motigoma.is_excist(koma):
				motigoma_flag = True
			else:   motigoma_flag = False

			pos = self.selectSafetyField(ban,koma,motigoma_flag)
			#if pos excists,return info	
			if pos != False:
				return util.infoDict(koma,pos,motigoma_flag)

	def think(self,ban):
		info = False
		if self.canKillOu(ban):
			print "kill ou"
			return self.canKillOu(ban)
		elif self.canTry(ban): 
			print "try ou"
			return self.canTry(ban)
		elif self.killChecker(ban): 
			print "kill chekcer"
			return self.killChecker(ban)
		elif self.escapeOu(ban): 
			print "escape ou"
			return self.escapeOu(ban)

		elif self.safetyRandomSelect(ban):
			print "safetyRandomSelect"
			return self.safetyRandomSelect(ban)
		else:
			print "random"
			return self.randomSelect(ban)
				
			
		
