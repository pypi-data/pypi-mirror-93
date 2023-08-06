
import os




def writeToBuffer0(Identifier, Content):
	if(len(Identifier)!= 11):
		size = os.get_terminal_size()
		
		print("-"*size.columns)
		sizeText = int(round(size.columns/2-33,0))
		textSpace = " " * sizeText
		print(textSpace + "ERROR IDENTIFIER NOT RIGHT LENGTH")
		sizeText2 = int(round(size.columns/2-38,0))
		textSpace2 = " " * sizeText2
		print(textSpace2 + "Identifier musst be 11 Digits! It is:" + str(len(Identifier))+ " Digits.")
		print("-"*size.columns)
		exit()
		pass

	spiWrite("0x31") #Adress Identifier

	split_Identifier = []
	n  = 8
	for index in range(0, len(Identifier), n):
		split_Identifier.append(Identifier[index : index + n])
	writeToRegister(hex(49), split_Identifier[0])
	writeToRegister(hex(50), str("00000") + split_Identifier[1])


	split_Content = []
	n  = 8
	for indexa in range(0, len(Content), n):
		split_Content.append(Content[indexa : indexa + n])
	writeToRegister(hex(54), split_Content[0])
	writeToRegister(hex(55), split_Content[1])
	writeToRegister(hex(56), split_Content[2])
	writeToRegister(hex(57), split_Content[3])
	writeToRegister(hex(58), split_Content[4])
	writeToRegister(hex(59), split_Content[5])
	writeToRegister(hex(60), split_Content[6])
	writeToRegister(hex(61), split_Content[7])
	writeToRegister(hex(62), split_Content[8])
pass

def spiWrite(message):
	print("Send to SPI:" + str(message))
	pass

def spiStart():
	print("CS low")
	pass

def spiEnd():
	print("CS high")
	pass

def writeToRegister(Adress:str, Content: str):
	spiStart()
	spiWrite("0x2")  # 0x2 = 00000010 = Write
	spiWrite(Adress)
	spiWrite(Content)
	spiEnd()
	pass
