#!/usr/bin/python3
import mysql.connector
from mysql.connector import errorcode
import sys
import datetime
import json
import mysqlConnector as sql
import analytics
# import # logger
#import query
import logging

logging.basicConfig(
        filename='railApplication.log',
        format='%(asctime)s.%(msecs)-3d:%(filename)s:%(funcName)s:%(levelname)s:%(lineno)d:%(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        level=logging.DEBUG
    )

# logger =  # logger.logIt(__file__)

class main:
	'''
	1)GET A BETTER NAME FOR THE CLASS
	2)WRITE BETTER DOCUMENTATION AS YOU GO
	3)PLAN BEFORE YOU WRITE THE ACTUAL CODE
	4)PLEASE MAKE SURE YOU PASS 'null' AND NOT AN EMPTY LIST OR A DICTIONARY
	'''
	def __init__(self,jsonData,levelNumber):		#Constructor which decodes the incoming json data
		try:	#Checking if the input data is of string type
			logging.debug("Input data is of string type, converting into dict format")
			self.jsonString = json.loads(str(jsonData))
		except:	#Checking of the input data is of dict type, this happens only when the class create an instance of itself
			logging.debug("Input data is of dict type, no changes made")
			self.jsonString = jsonData
		# logger.log(str(json.dumps(self.jsonString)))
		logging.info("Input data is:"+str(json.dumps(self.jsonString)))

		self.levelNumber = levelNumber

		self.header = self.jsonString["HEADER"]			#Gets the header
		self.database = self.header["DATABASE"]			#database name within header
		self.table = self.header["TABLE_NAME"]			#table name name within header
		self.requestType = self.header["REQUEST_TYPE"]	#request type name within header

		self.data = self.jsonString["DATA"]				#Gets the data
		self.fields = self.data["FIELDS"]				#fields name within header
		self.setClause = self.data["SET"]				#setClause name within header
		self.whereClause = self.data["WHERE"]			#whereClause name within header

		self.footer = self.jsonString["FOOTER"]			#Gets the footer
		self.updateList = self.footer["UPDATE"]			#update name within header
		self.conditionList = self.footer["DEP"]			#dep name within header
		try:
			self.runCondition = self.footer["CONDITION"]	#Run analytics
			self.analyticsArguments = self.data["FIELDS"]
		except:
			logging.warning("Change 'DATA ABOUT THE REQUEST' to 'CONDITION'")
		'''
		WRITE THE CODE HERE TO GET DATA ABOUT THE REQUEST AND THE COMMENT FROM THE FOOTER SECTION
		'''


	#def showData(self):
	#	print("jsonString",self.jsonString)
	#	print("header			:",self.header)
	#	print("---database			:",self.database)
	#	print("---table name		:",self.table)
	#	print("---request type		:",self.requestType)
	#	print("data				:",self.data)
	#	print("---fields			:",self.fields)
	#	print("---set				:",self.setClause)
	#	print("---where				:",self.whereClause)
	#	print("footer			:",self.footer)
	#	print("---update			:",self.updateData)
	#	print("---dependency		:",self.conditionList)

	def getDatabase(self):
		return self.database

	def getTable(self):
		return self.table

	def setConnection(self):	#Establishes a connection between the script and the mysql database
		logging.info("Connecting to the database")
		self.mysqlConnection = sql.mysqlConnector(option_files=".config/mysql.cnf",database=self.database)
		#self.cursor = self.mysqlConnection.cursor(dictionary=True)
		logging.info("Connection successful")
		return
		#return self.cursor
		# # logger.log("Starting connection stage")
		"""
		logging.info("Connecting to the database")
		with open(".config/database.json") as cnfFile:
			data 	 = json.load(cnfFile)
			host 	 = data["host"]
			user 	 = data["user"]
			password = data["password"]
			try:
				self.mysqlConnection = mysql.connector.connect(
					host		=	host,		#CREATE A SEPARATE CONFIG FILE(FOR SECURITY PURPOSES) FOR THIS AND GET DATA FROM IT.
					user		=	user, 		#CREATE A SEPARATE CONFIG FILE(FOR SECURITY PURPOSES) FOR THIS AND GET DATA FROM IT.
					passwd		=	password, 	#CREATE A SEPARATE CONFIG FILE(FOR SECURITY PURPOSES) FOR THIS AND GET DATA FROM IT.
					database	=	self.getDatabase()
				)
				self.cursor = self.mysqlConnection.cursor(dictionary=True)
				# # logger.log("Successful creation of the cursor")
				logging.info("Connection successful")
				return self.cursor
			except mysql.connector.Error as err:
				# # logger.log(("An error occurred. ERROR NO: %d" % (err.errno)),True)
				logging.critical("Mysql connector error Error No:%4d:%s" % (err.errno,str(err.msg)))
				if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
					# logger.log("Access was denied.",True)
					logging.critical("Access was denied.")
				elif err.errno == errorcode.ER_BAD_DB_ERROR:
					# logger.log("Database does not exist",True)
					logging.critical("Database does not exist.")
				elif err.errno == errorcode.ER_BAD_FIELD_ERROR:
					# logger.log(("Invalid field : %s" % (err.msg)),True)
					logging.critical("Invalid field.")
				elif err.errno == errorcode.ER_BAD_TABLE_ERROR:
					# logger.log("Table does not exist",True)
					logging.critical("Table does not exist.")
				else:
					# logger.log(str(err),True)
					logging.critical(str(err.msg))
			else:
				# logger.log("Closing abruptly at connection stage")
				logging.critical("Closing abruptly at connection stage ... exiting program")
				exit(1)
		"""

	"""
	IM PLANNING ON SHIFTING ALL OF THE QUERIES INTO ANOTHER MODULE AS IT WILL BE REUSABLE.
	"""

	"""

	def insertData(self,insDict):
		# logger.log("Generating CREATE query(%s) ..." % (self.getTable()))
		logging.info("Generating CREATE query(%s) ..." % (self.getTable()))
		finalQuery = ("INSERT INTO %s(" % (self.getTable()))
		key = list(insDict.keys())
		value = list(insDict.values())
		length = len(key)
		finalQuery = finalQuery + "`" + key[0] + "`"
		for index in range(length - 1):
			finalQuery = finalQuery + "," + "`" + key[index + 1] + "`"
		finalQuery = finalQuery + ") VALUES("
		finalQuery = finalQuery + "'" + str(value[0]) + "'"
		for index in range(length - 1):
			if(value[index + 1] == "null"): #THE BLOCK BELOW GENERATES ",null"
				finalQuery = finalQuery + "," + str(value[index + 1])
				continue
			finalQuery = finalQuery + "," + "'" + str(value[index + 1]).replace("'",r"\'") + "'" #THE BLOCK BELOW GENERATES ",'val'"
		finalQuery = finalQuery + ");"
		# logger.log(finalQuery)
		logging.debug(finalQuery)
		self.cursor.execute(finalQuery)

	def deleteData(self,delDict,whereDict):
		# logger.log("Generating DELETE query(%s) ..." % (self.getTable()))
		logging.info("Generating DELETE query(%s) ..." % (self.getTable()))
		finalQuery = ("DELETE FROM " + self.getTable() + " WHERE ")
		key = list(whereDict.keys())
		value = list(whereDict.values())
		length = len(key)
		finalQuery = finalQuery + key[0] + "=" + "'" + str(value[0]) + "'"
		for index in range(length - 1):
			finalQuery = finalQuery + " AND " + key[index + 1] + "=" + "'" + str(value[index + 1]) + "'"
		finalQuery = finalQuery + ";"
		# logger.log(finalQuery)
		logging.debug(finalQuery)
		self.cursor.execute(finalQuery)


	def updateData(self,setDict,whereDict):
		# logger.log("Generating UPDATE query(%s) ..." % (self.getTable()))
		logging.info("Generating UPDATE query(%s) ..." % (self.getTable()))
		finalQuery = ("UPDATE %s SET " % (self.getTable()))
		key = list(setDict.keys())
		value = list(setDict.values())
		length = len(key)
		finalQuery = finalQuery + key[0] + "=" + "'" + value[0] + "'"
		for index in range(length - 1):
			finalQuery = finalQuery + "," + key[index + 1] + "=" + "'" + value[index + 1] + "'"
		finalQuery = finalQuery + " WHERE "
		key = list(whereDict.keys())
		value = list(whereDict.values())
		length = len(key)
		finalQuery = finalQuery + key[0] + "=" + "'" + value[0] + "'"
		for index in range(length - 1):
			if(value[index + 1].upper()	 == "NULL"):
				finalQuery = finalQuery + " AND " + key[index + 1] + " IS NULL"
				continue
			finalQuery = finalQuery + " AND " + key[index + 1] + "=" + "'" + value[index + 1] + "'"
		finalQuery = finalQuery + ";"
		# logger.log(finalQuery)
		logging.debug(finalQuery)
		#print("Query ready")
		self.cursor.execute(finalQuery)
		#print("Query excuted")

	def selectData(self,dataList,whereDict = None):
		# logger.log("Generating SELECT query(%s)" % (self.getTable()))
		logging.info("Generating SELECT query(%s)" % (self.getTable()))
		finalQuery = ("SELECT `" + dataList[0] + "`")
		length = len(dataList)
		for index in range(length - 1):
			finalQuery = finalQuery + ",`" + dataList[index + 1] + "`"
		finalQuery = finalQuery + " FROM " + self.getTable()
		if(whereDict != None):
			finalQuery = finalQuery + " WHERE "
			key = list(whereDict.keys())
			length = len(key)
			finalQuery = finalQuery + key[0] + "=" + "'" + whereDict[key[0]] + "'"
			for index in range((length - 1)):
				finalQuery = finalQuery + " AND " + key[index + 1] + "=" + "'" + whereDict[key[index + 1]] + "'"
			finalQuery = finalQuery + ";"
		# logger.log(finalQuery)
		self.cursor.execute(finalQuery)
		response = self.cursor.fetchall()
		logging.debug(response)
		return response

	def alterTable(self):
		print(" Alter table does not work")
		logging.critical("alterTable is not yet functional")
		return

	"""

	def validateData(self):
		# logger.log("Validating the incoming data")
		logging.info("Validating the incoming data")
		flag = False
		keys = None
		curObj = None
		for index in range(0,3):
			if(index == 0):
				if(self.fields == None):
					# logger.log("Fields:No data to validate")
					logging.info("Fields:No data to validate")
					continue
				keys = self.fields.keys()
				curObj = self.fields
			elif(index == 1):
				if(self.setClause == None):
					# logger.log("Set:No data to validate")
					logging.info("Set:No data to validate")
					continue
				keys = self.setClause.keys()
				curObj = self.setClause
			elif(index == 2):
				if(self.whereClause == None):
					# logger.log("Where:No data to validate")
					logging.info("Where:No data to validate")
					return
				keys = self.whereClause.keys()
				curObj = self.whereClause
			for aKey in keys:
				if(aKey == 'rail_id'):
					if(not(curObj[aKey].startswith("RSK"))):
						# logger.log("The rail id in invalid!")
						logging.info("The rail id in invalid!")
						flag = True
				elif(aKey == 'gender'):
					if((curObj[aKey].upper() not in ['M','F'])):
						# logger.log("The gender is invalid :"+curObj[aKey])
						logging.info("The gender is invalid :"+curObj[aKey])
						flag = True
				elif(aKey == 'date_of_birth'):
					# splitData = curObj[aKey].rsplit('-')				#Validates the date only if it is seperated by a "-"
					####################################
					"""WRITING CODE TO VALIDATE WHEN IT IS SEPERATED BY EITHER '-' OR '/'"""
					if("-" in curObj[aKey]):
						splitData = curObj[aKey].rsplit('-')
					elif("/" in curObj[aKey]):
						splitData = curObj[aKey].rsplit('/')
					else:
						logging.info("Dates must be seperated by either '-' or '/'")
						flag = True
					####################################
					if(len(splitData[0]) != 4 and not(splitData[0].isdigit())):
						# logger.log("The year is entered incorrectly")
						logging.info("The year is entered incorrectly")
						flag = True
					if(len(splitData[1]) != 2 and not(splitData[1].isdigit()) and (int(splitData[1])>0 and int(splitData[1])<=12)):
						# logger.log("The month is entered incorrectly")
						logging.info("The month is entered incorrectly")
						flag = True
					if(len(splitData[2]) != 2 and not(splitData[2].isdigit()) and (int(splitData[1])>0 and int(splitData[1])<=31)):
						# logger.log("The date is entered incorrectly")
						logging.info("The date is entered incorrectly")
						flag = True
				elif(aKey == 'phone_number'):
					if(len(curObj[aKey]) != 10):
						# logger.log("Phone number error")
						logging.info("Phone number error")
						flag = True
				elif(aKey == 'branch'):
					if((curObj[aKey] not in ['CS','EC','TX','CV'])):
						# logger.log("Branch invalid")
						logging.info("Branch invalid")
						flag = True
				elif(aKey == 'login_status'):
					if((curObj[aKey] not in ['YES','NO'])):
						# logger.log("login_status invalid")
						logging.info("login_status invalid")
						flag = True
				elif(aKey == 'component_status'):
					if((curObj[aKey] not in ['YES','NO'])):
						# logger.log("component_status invalid")
						logging.info("component_status invalid")
						flag = True
				elif(aKey == 'usn'):								#You need to change this if this is given to somone else
					if(not(curObj[aKey].startswith('1SK'))):
						# logger.log("USN is invalid")
						logging.info("USN is invalid")
						flag = True
				elif(aKey == 'current_highest_role'):
					if((curObj[aKey].lower() not in ['member','team lead'])):
						# logger.log("Role if student is not supported")
						logging.info("Role if student is not supported")
						flag = True
				if(flag == True):
					print("FailedOperation : Error in data entered, check the logs!")
					exit(0)

	def processRequest(self):
		# logger.log("Start of process request")
		logging.info("Processing request")
		self.conditionFlag  = False
		if(self.conditionList != None): #cannot test for len(self.conditionList) == 0 i.e when there is a empty list passed, raises TypeError
			for element in self.conditionList:
				logging.info("LevelNumber: {} - Creating a new sub process with:".format(self.levelNumber)+str(element))
				subProcess = main(element,self.levelNumber + 1)
				subProcess.setConnection()
				if subProcess.processRequest():			#Ok, I have forgotten what this statement is supposed to mean
					# logger.log("The condition flag is being set to True")
					logging.debug("The condition flag is being set to True")
					self.conditionFlag = True
				else:
					# logger.log("The condition flag is being set to False")
					logging.debug("The condition flag is being set to False")
					self.conditionFlag = False
					break
		else:
			# logger.log("condition list is null")
			logging.debug("conditionList is null")
		if(self.conditionList == None or self.conditionFlag == True): #cannot test for len(self.conditionList) == 0 i.e when there is a empty list passed, raises TypeError
			'''
			KIMS THAT WHEN A SELECT IS USED IT RETURNS DATA AND CANNOT BE USED TO UPDATE ANOTHER TABLE.
			I NEED TO RESTRUCTURE IT TO BE ABLE TO RETURN AS WELL AS RUN AN UPDATE.
			'''
			if(self.requestType == "insert"):
				# logger.log("The insert condition is being run")
				# self.insertData(self.fields)
				#if(self.getTable == "attendance"):
				#	print("Need to update the current_students table")
				self.mysqlConnection.insert(self.getTable(),self.fields)
			elif(self.requestType == "delete"):
				# self.deleteData(self.fields,self.whereClause)
				self.mysqlConnection.delete(self.getTable(),self.fields,self.whereClause)
			elif(self.requestType == "update"):
				# self.updateData(self.setClause,self.whereClause)
				self.mysqlConnection.update(self.getTable(),self.setClause,self.whereClause)
			elif(self.requestType == "select"):
				#print(type(self.fields))
				# return self.selectData(self.fields,self.whereClause)
				return self.mysqlConnection.select([self.getTable()],self.fields,self.whereClause)
			elif(self.requestType == "alter"):
				# self.alterTable()
				self.mysqlConnection.alter()
			try:
				for anObject in self.updateList:
					#print("Start of a sub process.")
					#print(anObject)
					logging.info("LevelNumber: {} - Creating a new sub process with:".format(self.levelNumber)+str(anObject))
					subProcess = main(anObject,self.levelNumber + 1)
					subProcess.setConnection()
					#subProcess.showData()
					subProcess.processRequest()
					#print("End of the sub process.")
			except TypeError:
				pass
			except BaseException as e:
				# logger.log("Exception Raised:"+str(e),True)
				logging.info("Exception Raised:"+str(e))
				exit(0)
			# self.mysqlConnection.commit()
			self.mysqlConnection.commitChanges()

	def findValueOfKey(self,toBeSearched):
		if(self.fields != None):
			if(toBeSearched in self.fields.keys()):
				return self.fields[toBeSearched]
		elif(self.whereClause != None):
			if(toBeSearched in self.whereClause.keys()):
				return self.whereClause[toBeSearched]
		else:
			# logger.log("findValueOfKey:Error could not find the string.")
			logging.error("findValueOfKey:Error could not find the string.")


	def generateAnalytics(self):		#Write # logger function for this
		if(self.conditionFlag == False):
			return
		else:
			analytics.analytics(self.mysqlConnection,**self.analyticsArguments)
			analytics.generateAnalytics(self.runCondition)
		return
		# logger.log("To generate analytics:"+str(self.requestType)+str(self.footer["DATA ABOUT THE REQUEST"]))
		if(self.requestType.lower() == 'update' and self.footer["DATA ABOUT THE REQUEST"].lower() == 'logout'):	#This is for attendance
			# logger.log("Running LOGOUT condition")
			rail_id = self.findValueOfKey('rail_id')
			self.cursor.execute("SELECT time_in,time_out from attendance where rail_id='"+ rail_id +"' ORDER BY time_out DESC;")
			mysqlData =  self.cursor.fetchall()
			loginTime = mysqlData[0]['time_in']
			logoutTime = mysqlData[0]['time_out']
			timeSpent = logoutTime - loginTime
			self.cursor.execute("UPDATE attendance SET time_spent='"+ str(timeSpent) +"' where time_in='"+ loginTime.strftime("%Y-%m-%d %H:%M:%S") +"';")
			self.cursor.execute("SELECT time_in_rail FROM cur_studs WHERE rail_id='"+ rail_id +"';")
			mysqlData = self.cursor.fetchall()
			totalTime = mysqlData[0]['time_in_rail']
			if(totalTime != None):
				timeInStringFormat = totalTime.split(":")
				timeInTimeFormat = datetime.time(int(timeInStringFormat[0]),int(timeInStringFormat[1]),int(timeInStringFormat[2]))
				timeInTimeFormat = (datetime.datetime.combine(datetime.date.today(),timeInTimeFormat) + timeSpent).time()
				self.cursor.execute("UPDATE cur_studs SET time_in_rail='"+ str(timeInTimeFormat) +"' WHERE rail_id='"+rail_id+"';")
			else:
				self.cursor.execute("UPDATE cur_studs SET time_in_rail='"+ str(timeSpent) +"' WHERE rail_id='"+rail_id+"';")
		elif(self.requestType.lower() == 'insert' and self.footer["DATA ABOUT THE REQUEST"].lower() == 'login'):	#This is for attendance
			# logger.log("Running LOGIN condition")
			rail_id = self.findValueOfKey('rail_id')
			self.cursor.execute("SELECT time_in FROM attendance where rail_id='" + self.findValueOfKey("rail_id") + "' AND time_out is null;")
			data = self.cursor.fetchall()
			time_in = data[0]["time_in"]
			self.cursor.execute("UPDATE cur_studs SET most_recent_login='"+ time_in.strftime("%Y-%m-%d %H:%M:%S") +"' WHERE rail_id = '"+ rail_id +"';")
		elif(self.requestType.lower() == 'update' and self.footer["DATA ABOUT THE REQUEST"].lower() == 'ret_comp'):	#This is for component
			# logger.log("Running ret_comp condition")
			rail_id = self.findValueOfKey("issued_to")
			comp_id = self.findValueOfKey("component_id")
			self.cursor.execute("SELECT time_of_issue,time_of_return FROM iss_compnts WHERE issued_to='" + rail_id +"' ORDER BY time_of_return DESC;")
			mysqlData = self.cursor.fetchall()
			issTime = mysqlData[0]["time_of_issue"]
			retTime = mysqlData[0]["time_of_return"]
			timeOfUse = retTime - issTime
			self.cursor.execute("UPDATE iss_compnts SET time_of_use='"+ str(timeOfUse) +"' where time_of_issue='"+ issTime.strftime("%Y-%m-%d %H:%M:%S") +"';")
			print("SELECT total_time_of_use FROM components WHERE component_id='" + comp_id + "';")
			self.cursor.execute("SELECT total_time_of_use FROM components WHERE component_id='" + comp_id + "';")
			mysqlData = self.cursor.fetchall()
			print(mysqlData)
			totalTime = mysqlData[0]["total_time_of_use"]
			if(totalTime != None):
				timeInStringFormat = totalTime.split(":")
				timeInTimeFormat = datetime.time(int(timeInStringFormat[0]),int(timeInStringFormat[1]),int(timeInStringFormat[2]))
				timeInTimeFormat = (datetime.datetime.combine(datetime.date.today(),timeInTimeFormat) + timeOfUse).time()
				self.cursor.execute("UPDATE components SET total_time_of_use='"+ str(timeInTimeFormat) +"' WHERE component_id='"+comp_id+"';")
			else:
				self.cursor.execute("UPDATE components SET total_time_of_use='"+ str(timeOfUse) +"' WHERE component_id='"+comp_id+"';")
			#
			# TO UPDATE THE COMPOENET STATUS TO NO WHEN HE RETURNS ALL THE COMPONENTS
			#
			self.cursor.execute("SELECT component_id FROM iss_compnts where issued_to='" + rail_id + "' AND time_of_return is NULL")
			mysqlData = self.cursor.fetchall()
			if(not(mysqlData)):
				self.cursor.execute("UPDATE cur_studs SET component_status = 'NO' where rail_id = '" + rail_id + "';")
		elif(self.requestType.lower() == 'insert' and self.footer["DATA ABOUT THE REQUEST"].lower() == 'req_comp'):	#This is for component
			# logger.log("Running req_comp condition")
			comp_id = self.findValueOfKey('component_id')
			self.cursor.execute("SELECT time_of_issue FROM iss_compnts where component_id='" + comp_id + "' AND time_of_return is null;")
			data = self.cursor.fetchall()
			time_iss = data[0]["time_of_issue"]
			self.cursor.execute("UPDATE components SET most_recent_issue='"+ time_iss.strftime("%Y-%m-%d %H:%M:%S") +"' WHERE component_id = '"+ comp_id +"';")
		else:
			pass
		self.mysqlConnection.commit()



"""
class analytics:
	def __init__(self,connection,cursor):
		#Write code here to load the data
		self.connection = connection
		self.cursor = cursor
		print("Constructor")
		try:
			with open(".config/extraData.json") as cnfFile:
				self.jsonData = json.load(cnfFile)
		except FileNotFoundError:
			ans = input("File does not exit, do you want to create it?(y/n)")
			if(ans == 'y' or ans == 'Y'):
				print("Write code to create a new file.")
				exit(0)
		except:
			print("Unhandeled Error...exitting...")
			exit()

	def showData(self):
		print("json data:",self.jsonData)

	def run(self,tableName):
		self.tableName = tableName
		if(tableName == ""):
			print("break")
		elif(tableName == ""):
			print("break")
		else:
			print("break")

	def updatedAttendace(self):
		print('updatedAttendace')

	def updatedStudents(self):
		print("updatedStudents")
"""

if __name__ == '__main__':
	# logger.log("Start of database.py")
	logging.info("Start of database.py")
	process = main(sys.argv[1],0)
	process.validateData()
	process.setConnection()
	process.processRequest()
	process.generateAnalytics()
	logging.info("End of database.py")
	# logger.log("End of database.py")
else:
	print("This code does not support being imported as a module")
	exit(0)