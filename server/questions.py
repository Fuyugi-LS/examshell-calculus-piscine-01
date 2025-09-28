import sqlite3
import yaml # type: ignore
from pathlib import Path

root = (Path(__file__).parent).absolute()

def get_question(id):
	with open(root / "query.yaml", "r", encoding="utf-8") as f:
		query = yaml.safe_load(f)
	conn = sqlite3.connect(root / "questions.db")
	curr = conn.cursor()
	curr.execute(query["get_question"], (id,))
	question = curr.fetchone()
	conn.close()
	return question[0]

def get_answer(id):
	with open(root / "query.yaml", "r", encoding="utf-8") as f:
		query = yaml.safe_load(f)
	conn = sqlite3.connect(root / "questions.db")
	curr = conn.cursor()
	curr.execute(query["get_answer"], (id,))
	question = curr.fetchone()
	conn.close()
	return question[0]

def dumpshitalllist(dict_t):
	with open(root / "query.yaml", "r", encoding="utf-8") as f:
		query = yaml.safe_load(f)
	conn = sqlite3.connect(root / "questions.db")
	curr = conn.cursor()
	for item in dict_t:
		curr.execute(query["dumpshitalllist"], (item["id"], item["question"], item["answer"]))
	conn.commit()
	conn.close()

if __name__ == "__main__":
	print(get_question(125))
	print(get_answer(0))
