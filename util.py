
def isZero(val):
	return isinstance(val,int)

def collectKoma(ban,owner_name):
		koma_lst = []
		for vlst in ban.field:
			for koma in vlst:
				if koma!=0 and koma.owner == owner_name:
					koma_lst.append(koma)
		return koma_lst

def collectPos(ban,fn):
	pos_lst = []

	for j,vlst in enumerate(ban.field):
		for i,val in enumerate(vlst):
			if i>=1 and i<=3 and j>=1 and j <=4:
				if fn(val):
					pos_lst.append((i,j))
	return pos_lst

def isRegal(ban,pos,owner_name):
	posX = pos[0]
	posY = pos[1]

	val = ban.field[posY][posX] 
	if posX>=1 and posX<=3 and posY>=1 and posY<=4:
		if isinstance(val,int):
			if val == 0:
				return True
		elif val.owner != owner_name:
			return True
		else: return False
	#over field
	else: return False

#different point -> elif val.owner != owner_name;.....
def isRegal2(ban,pos,owner_name):
	posX = pos[0]
	posY = pos[1]

	val = ban.field[posY][posX] 
	if posX>=1 and posX<=3 and posY>=1 and posY<=4:
		return True
	#over field
	else: return False

		

def collectMoveablePos(ban,koma,owner_name):
	pos_lst = []
	for dir in koma.dir_lst:
		posX = koma.posX + dir[0]
		posY = koma.posY + dir[1] 

		if isRegal(ban,(posX,posY),owner_name):
			pos_lst.append((posX,posY))

	return pos_lst

def collectCommandingPos(ban,koma,owner_name):
	pos_lst = []
	for dir in koma.dir_lst:
		posX = koma.posX + dir[0]
		posY = koma.posY + dir[1] 

		if isRegal2(ban,(posX,posY),owner_name):
			pos_lst.append((posX,posY))

	return pos_lst


def infoDict(koma,pos,motigoma_flag):	
	return {"koma":koma,"pos":pos,"motigoma_flag":motigoma_flag}

def isEqual(pos1,pos2):
	if pos1[0] == pos2[0] and pos1[1] == pos2[1]:
		return True
	else:return False
