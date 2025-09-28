from xmlrpc.server import SimpleXMLRPCServer
import questions
import lynette

def ping():
	return "examsystd v.1.5"

def get_grade(file, id):
	result = ""
	verdict = lynette.get_verdict(id, file)
	deepthought = lynette.deepthought()
	if verdict == "OK":
		result = "PASS"
	else:
		result = "FAIL"
	return result, deepthought

def get_question(id):
	return questions.get_question(id)

server = SimpleXMLRPCServer(("127.0.0.1", 12509), allow_none=True)
reg = [[ping, "ping"], [get_grade, "get_grade"], [get_question, "get_question"]]
for item in reg:
	server.register_function(item[0], item[1])
print("OKOK")
server.serve_forever()
