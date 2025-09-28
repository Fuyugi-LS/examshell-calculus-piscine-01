import xmlrpc.client
import pathlib

proxy = xmlrpc.client.ServerProxy("http://127.0.0.1:12509/")

def question(id):
	return proxy.get_question(id)

def get_grade(id):
	path = pathlib.Path("rendu/answer")
	with open(path, "r", encoding="utf-8") as f:
		usrans = f.read()
		return proxy.get_grade(usrans, 0)

if __name__ == "__main__":
	print(question(1))
	print(get_grade(0))
