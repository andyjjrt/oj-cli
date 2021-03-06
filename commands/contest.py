import json
import os
from datetime import datetime
from datetime import timedelta

from constants import ASSIGNMENT_MAPPING_PATH, COOKIES_DIR, MY_STATUS_PATH, STATEMENT_PATH
from .status import status
from util.common import get_csrf_token
from util.curl import curl
from util.colors import cyan_wrapper, green_wrapper, purple_wrapper, red_wrapper


def contests_status(assign_name):
	with open(ASSIGNMENT_MAPPING_PATH, "rt") as json_in:
		assign_to_config = json.load(json_in)
	if assign_name not in assign_to_config:
		print("Invalid Assign Number!")
		print("Available names are:")
		for hwmap in assign_to_config:
			print("- " + cyan_wrapper(hwmap + " [" + assign_to_config[hwmap]['contest_name'] + "]"))
		print("If you want to update latest homework assignment, type: [oj update] to update.")
		return
	contest_id, problem_id = (
        assign_to_config[assign_name]["contest_id"],
        assign_to_config[assign_name]["contest_problem_id"],
    )
	endpoint = "contest_submissions?myself=0&contest_id={}&limit=20&problem_id={}".format(
        contest_id,
		assign_name
    )
	result = json.loads(curl("get", endpoint=endpoint, use_x_csrf_token=True))
	if result["error"] == "error":
		print("Error : " + result["data"])
		return
	result = result["data"]["results"]
	status_to_response = {
			-1: red_wrapper("WA(Wrong Answer)"),  # WA
			-2: cyan_wrapper("CE(Compilation Error)"),  # CE
			0: green_wrapper("AC(Accept)"),  # AC
			1: purple_wrapper("TLE(Time Limit Exceeded)"),  # TLE
			2: purple_wrapper("TLE(Time Limit Exceeded)"),  # TLE
			3: purple_wrapper("MLE(Memory Limit Exceeded)"),  # ML 
			4: purple_wrapper("RE(Runtime Error)"),  # RE
			8: cyan_wrapper("PAC(Partial Accepted)")
			}
	print("============================================================================")
	print('|  Problem Name: {:58}|'.format(assign_to_config[assign_name]["contest_problem_id"] + " [" + assign_to_config[assign_name]["contest_name"] + "]"))
	print("============================================================================")
	print('|{:12}|{:27}|   Time|  Mem|               When|'.format("User","Status"))
	for i in result:
		if i["problem"] != assign_to_config[assign_name]["contest_problem_id"]:
			continue
		timestr = i["create_time"].split("T")[0]
		timestr += " " + i["create_time"].split("T")[1].split(".")[0]
		mydatetmp = datetime.strptime(timestr, '%Y-%m-%d %H:%M:%S')
		hours_added = timedelta(hours = 8)
		timestr = mydatetmp + hours_added
		timestr.strftime("%m/%d/%Y, %H:%M:%S")
		if i["result"] != -2:
			try:
				usrname = i["username"].encode('ascii').decode()
			except UnicodeEncodeError:
				usrname = "UCuser"
			print('|{:12}|{:38}|{:5}ms|{:3}MB|{}|'.format(usrname, status_to_response[i["result"]], i["statistic_info"]["time_cost"], (i["statistic_info"]["memory_cost"]/1048576)+1, timestr))
		else:
			try:
				usrname = i["username"].encode('ascii').decode()
			except UnicodeEncodeError:
				usrname = "UCuser"
			print('|{:12}|{:38}|{:5}--|{:3}--|{}|'.format(usrname, status_to_response[i["result"]], "-----", "---", timestr))
	print("============================================================================")

def my_contests_status(assign_name):
	with open(ASSIGNMENT_MAPPING_PATH, "rt") as json_in:
		assign_to_config = json.load(json_in)
	try:
		with open(MY_STATUS_PATH, "rt") as json_in:
			status_config = json.load(json_in)
			if assign_name in status_config:
				status(status_config[assign_name]["id"])
				return
	except:
		pass
	if assign_name not in assign_to_config:
		print("Invalid Assign Number!")
		print("Available names are:")
		for hwmap in assign_to_config:
			print("- " + cyan_wrapper(hwmap + " [" + assign_to_config[hwmap]['contest_name'] + "]"))
		print("If you want to update latest homework assignment, type: [oj update] to update.")
		return
	contest_id, problem_id = (
        assign_to_config[assign_name]["contest_id"],
        assign_to_config[assign_name]["contest_problem_id"],
    )
	endpoint = "contest_submissions?myself=1&contest_id={}&limit=20&problem_id={}".format(
        contest_id,
		assign_name
    )
	result = json.loads(curl("get", endpoint=endpoint, use_x_csrf_token=True))
	if result["error"] == "error":
		print("Error : " + result["data"])
		return
	result = result["data"]["results"]
	status_to_response = {
			-1: red_wrapper("WA(Wrong Answer)"),  # WA
			-2: cyan_wrapper("CE(Compilation Error)"),  # CE
			0: green_wrapper("AC(Accept)"),  # AC
			1: purple_wrapper("TLE(Time Limit Exceeded)"),  # TLE
			2: purple_wrapper("TLE(Time Limit Exceeded)"),  # TLE
			3: purple_wrapper("MLE(Memory Limit Exceeded)"),  # ML 
			4: purple_wrapper("RE(Runtime Error)"),  # RE
			8: cyan_wrapper("PAC(Partial Accepted)")
			}
	print("============================================================================")
	print('|  Problem Name: {:58}|'.format(assign_to_config[assign_name]["contest_problem_id"] + " [" + assign_to_config[assign_name]["contest_name"] + "]"))
	print("============================================================================")
	print('|{:12}|{:27}|   {:4}|  {:3}|               When|'.format("ID  ","Status","Time","Mem"))
	inputstr = '{'
	idx = 0
	for i in result:
		if i["problem"] != assign_to_config[assign_name]["contest_problem_id"]:
			continue
		timestr = i["create_time"].split("T")[0]
		timestr += " " + i["create_time"].split("T")[1].split(".")[0]
		mydatetmp = datetime.strptime(timestr, '%Y-%m-%d %H:%M:%S')
		hours_added = timedelta(hours = 8)
		timestr = mydatetmp + hours_added
		timestr.strftime("%m/%d/%Y, %H:%M:%S")
		if i["result"] != -2:
			print('|ID{:10}|{:38}|{:5}ms|{:3}MB|{}|'.format(idx,status_to_response[i["result"]], i["statistic_info"]["time_cost"], (i["statistic_info"]["memory_cost"]/1048576)+1, timestr))
		else:
			print('|ID{:10}|{:38}|{:5}--|{:3}--|{}|'.format(idx, status_to_response[i["result"]], "-----", "---", timestr))
		if idx != 0:
			inputstr += ','
		inputstr += '"ID' + str(idx) + '":{"id":"' + i["id"] + '"}'
		idx+=1
	print("============================================================================")
	inputstr += '}'
	if not os.path.isdir(STATEMENT_PATH):
		os.mkdir(STATEMENT_PATH)
	f1 = open(MY_STATUS_PATH,'w')
	f1.write(inputstr.encode('utf-8'))
	f1.close

def contests_result(assign_name):
	with open(ASSIGNMENT_MAPPING_PATH, "rt") as json_in:
		assign_to_config = json.load(json_in)
	if assign_name not in assign_to_config:
		print("Invalid Assign Number!")
		print("Available names are:")
		for hwmap in assign_to_config:
			print("- " + cyan_wrapper(hwmap + " [" + assign_to_config[hwmap]['contest_name'] + "]"))
		print("If you want to update latest homework assignment, type: [oj update] to update.")
		return
	contest_id, problem_id = (
        assign_to_config[assign_name]["contest_id"],
        assign_to_config[assign_name]["contest_problem_id"],
    )
	endpoint = "contest_rank?myself=0&contest_id={}&limit=100".format(
        contest_id
    )
	result = json.loads(curl("get", endpoint=endpoint, use_x_csrf_token=True))
	if result["error"] == "error":
		print("Error : " + result["data"])
		return
	endpoint = "contest/problem?contest_id={}&problem_id={}".format(
        contest_id,
		assign_name
    )
	result2 = json.loads(curl("get", endpoint=endpoint, use_x_csrf_token=True))
	if result2["error"] == "error":
		print("Error : " + result2["data"])
		return
	result = result["data"]["results"]
	result2 = result2["data"]
	status_to_response = {
			-1: red_wrapper("WA(Wrong Answer)"),  # WA
			-2: cyan_wrapper("CE(Compilation Error)"),  # CE
			0: green_wrapper("AC(Accept)"),  # AC
			1: purple_wrapper("TLE(Time Limit Exceeded)"),  # TLE
			2: purple_wrapper("TLE(Time Limit Exceeded)"),  # TLE
			3: purple_wrapper("MLE(Memory Limit Exceeded)"),  # ML 
			4: purple_wrapper("RE(Runtime Error)"),  # RE
			8: cyan_wrapper("PAC(Partial Accepted)")
			}
	if result2["my_status"] == None:
		print("Your status of " + assign_to_config[assign_name]["contest_problem_id"] + " : No record")
	else:
		print("Your status of " + assign_to_config[assign_name]['contest_problem_id'] + " : " + status_to_response[result2["my_status"]])
	print("================================================")
	blockstatus=[0,0,0,0,0,0,0,0,0,0]
	for usr in result:
		try:
			problem_index = str(assign_to_config[assign_name]["problem_id"])
			blocks = usr["submission_info"][problem_index]/10
			blocks -= 1
			if blocks <= 0:
				blocks = 0
			blockstatus[blocks] += 1
		except:
			continue
	ic = 0
	for i in blockstatus:
		stastr = ''
		if ic == 0:
			try:
				print(' {:3}~{:3} :{:3}  |  {:35} : {}'.format(ic+1,ic+10,i,status_to_response[0],result2["statistic_info"]["0"]))
			except:
				print(' {:3}~{:3} :{:3}  |  {:35} : {}'.format(ic+1,ic+10,i,status_to_response[0],0))
		elif ic == 10:
			try:
				print(' {:3}~{:3} :{:3}  |  {:35} : {}'.format(ic+1,ic+10,i,status_to_response[4],result2["statistic_info"]["4"]))
			except:
				print(' {:3}~{:3} :{:3}  |  {:35} : {}'.format(ic+1,ic+10,i,status_to_response[4],0))
		elif ic == 20:
			try:
				print(' {:3}~{:3} :{:3}  |  {:35} : {}'.format(ic+1,ic+10,i,status_to_response[8],result2["statistic_info"]["8"]))
			except:
				print(' {:3}~{:3} :{:3}  |  {:35} : {}'.format(ic+1,ic+10,i,status_to_response[8],0))
		elif ic == 30:
			try:
				print(' {:3}~{:3} :{:3}  |  {:35} : {}'.format(ic+1,ic+10,i,status_to_response[-1],result2["statistic_info"]["-1"]))
			except:
				print(' {:3}~{:3} :{:3}  |  {:35} : {}'.format(ic+1,ic+10,i,status_to_response[-1],0))
		elif ic == 40:
			try:
				print(' {:3}~{:3} :{:3}  |  {:35} : {}'.format(ic+1,ic+10,i,status_to_response[-2],result2["statistic_info"]["-2"]))
			except:
				print(' {:3}~{:3} :{:3}  |  {:35} : {}'.format(ic+1,ic+10,i,status_to_response[-2],0))
		elif ic == 50:
			try:
				print(' {:3}~{:3} :{:3}  |  {:35} : {}'.format(ic+1,ic+10,i,status_to_response[1],result2["statistic_info"]["1"] + result2["statistic_info"]["2"]))
			except:
				try:
					print(' {:3}~{:3} :{:3}  |  {:35} : {}'.format(ic+1,ic+10,i,status_to_response[1],result2["statistic_info"]["2"]))
				except:
					try:
						print(' {:3}~{:3} :{:3}  |  {:35} : {}'.format(ic+1,ic+10,i,status_to_response[1],result2["statistic_info"]["1"]))
					except:
						print(' {:3}~{:3} :{:3}  |  {:35} : {}'.format(ic+1,ic+10,i,status_to_response[1],0))
		elif ic == 60:
			print(' {:3}~{:3} :{:3}  |--------------------------------'.format(ic+1,ic+10,i))
		elif ic == 70:
			print(' {:3}~{:3} :{:3}  |  {:24} : {}'.format(ic+1,ic+10,i,"Total submissions",result2["submission_number"]))
		else:
			print(' {:3}~{:3} :{:3}  |'.format(ic+1,ic+10,i))
		ic += 10
	print("================================================\nFor real time score ranking, please go to the website.")
