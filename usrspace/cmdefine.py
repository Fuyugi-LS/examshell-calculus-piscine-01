import fire # type: ignore
from pathlib import Path
import yaml # pyright: ignore[reportMissingModuleSource]
import pendulum # type: ignore
import netloc
import os

class AutoLog:
	passmsg = "Pass"
	failmsg = "Failure"
	conn = "Press Enter to continue (You'll get the same problem if you failed)"
	log_success = "[PASS] Problem #{}: {}"
	log_fail = "[FAIL] Problem #{}: {}"

def penter_tocontinue(text=f"{AutoLog.conn}"):
	input(text)
	return

class StaticVal:
	score = 0
	problem = 0
	history = []
	protest = []

	@staticmethod
	def Get_History():
		if len(StaticVal.history) == 0:
			return "[ - ]"
		else:
				tmp = "\t"
				for item in StaticVal.protest:
					tmp = tmp + "[PROTEST] "
					tmp = tmp + item[0]
					tmp = tmp + '\n\t'
				replic = StaticVal.history
				if len(StaticVal.history) > 2:
					replic = StaticVal.history[-3:]
				for item in replic:
					tmp = tmp + item # type: ignore
					tmp = tmp + "\n"
					tmp = tmp + "\t"
				return tmp # type: ignore

	@staticmethod
	def save_static():
		with open(Meta.stdpath / "static.yaml", "w", encoding="utf-8") as f:
			yaml.safe_dump({
				"score": StaticVal.score,
				"problem": StaticVal.problem,
				"history": StaticVal.history,
				"protest": StaticVal.protest
			}, f)

	@staticmethod
	def add_static():
		with open(Meta.stdpath / "static.yaml", "r", encoding="utf-8") as f:
			bocal = yaml.safe_load(f)
		StaticVal.score = bocal["score"]
		StaticVal.problem = bocal["problem"]
		StaticVal.history = bocal["history"]
		StaticVal.protest = bocal["protest"]

	@staticmethod
	def add_score():
		StaticVal.score += 100 / 125

class Examtime:
	start = None
	deadline = start

	@staticmethod
	def save_time():
		with open(Meta.stdpath / "clock.yaml", "w", encoding="utf-8") as f:
			yaml.safe_dump({
				"start": Examtime.start.to_datetime_string(), #type: ignore
				"deadline": Examtime.deadline.to_datetime_string() #type: ignore
			}, f)
			return

	@staticmethod
	def add_time():
		with open(Meta.stdpath / "clock.yaml", "r", encoding="utf-8") as f:
			tim = yaml.safe_load(f)
			Examtime.start = pendulum.parse(tim["start"])
			Examtime.deadline = pendulum.parse(tim["deadline"])
		return

	@staticmethod
	def left_over_time():
		return Examtime.deadline - pendulum.now() # type: ignore


class Meta:
	data = None
	stdpath = (Path(__file__).parent)
	meta_path = stdpath / "meta.yaml"

	def __init__(self):
		if not Meta.data:	
			with open(Meta.meta_path, "r", encoding="utf8") as f:
				Meta.data = yaml.safe_load(f)


class Cmds:
	def __init__(self):
		Meta()

	def examshell(self):
		StaticVal.save_static()
		Examtime.start = pendulum.now("Asia/Bangkok")
		Examtime.deadline = Examtime.start.add(hours=8)
		Examtime.save_time()
		Cmds.continue_t(0)

	def preloop(self):
		print(Meta.data["header"]) #type: ignore

	@staticmethod
	def continue_t(pid):
		print(f"Started time: {Examtime.start.to_datetime_string()}") #type: ignore
		print(f"Finished time: {Examtime.deadline.to_datetime_string()}") #type: ignore
		print(f"Time left: {Examtime.left_over_time().in_words()}") #type: ignore
		print("========================================================")
		print(f"""
You are doing: [Exam01 Piscine Calculus]
Your current score is: {(StaticVal.score):.2f}
History:
{StaticVal.Get_History()}

Problem #{StaticVal.problem}: {pid}
{netloc.question(pid)}
When ready, type 'grademe' with your code.
""")

	def grademe(self, f=False, p=False, verdict: str = "", description: str = ""):
		StaticVal.add_static()
		Examtime.add_time()
		if p:
			Cmds.protest(self, StaticVal.problem, description) # type: ignore
		probid = StaticVal.problem
		probname = netloc.question(probid)
		if verdict and not f:
			print("!REJECTED. ONLY administrator performed this action")
			StaticVal.save_static()
			return
		elif verdict and f:
			if verdict=="pass":
				print(AutoLog.passmsg)
				StaticVal.history.append(AutoLog.log_success.format(
					probid,
					probname
				))
				StaticVal.problem += 1
				StaticVal.add_score()
				penter_tocontinue()
				Cmds.continue_t((StaticVal.problem)) # type: ignore
				StaticVal.save_static()
				return
			if not verdict=="pass":
				print(AutoLog.failmsg)
				StaticVal.history.append(AutoLog.log_fail.format(
					probid,
					probname
				))
				penter_tocontinue()
				Cmds.continue_t((StaticVal.problem)) # type: ignore
				StaticVal.save_static()
				return
		if not (Meta.stdpath / "rendu").exists():
			print(AutoLog.failmsg)
			print("NOT FOUND DIRECTORY, GRADING STOP")
			StaticVal.history.append(AutoLog.log_fail.format(
					probid,
					probname
				))
			penter_tocontinue()
			Cmds.continue_t((StaticVal.problem)) # type: ignore
			StaticVal.save_static()
			return
		userfile = Meta.stdpath / "rendu" / "answer"
		if not userfile.exists():
			print(AutoLog.failmsg)
			print("NOT FOUND ANSWER, STOP")
			StaticVal.history.append(AutoLog.log_fail.format(
					probid,
					probname
			))
			penter_tocontinue()
			Cmds.continue_t((StaticVal.problem)) # type: ignore
			StaticVal.save_static()
			return
		result, deepthough = netloc.get_grade(probid) #type: ignore
		if result.upper() == "PASS": # type: ignore
			print(AutoLog.passmsg)
			StaticVal.history.append(AutoLog.log_success.format(
				probid,
				probname
			))
			StaticVal.problem += 1
			StaticVal.add_score()
			penter_tocontinue()
			Cmds.continue_t((StaticVal.problem)) # type: ignore
			StaticVal.save_static()
			return
		else:
			print(AutoLog.failmsg)
			StaticVal.history.append(AutoLog.log_fail.format(
				probid,
				probname
			))
			if not (Meta.stdpath / "report").exists():
				os.system(f"mkdir {str((Meta.stdpath / "report").absolute())}")
			with open(Meta.stdpath / "report" / "report01", "w", encoding="utf-8") as f:
				f.write(deepthough) # type: ignore
			penter_tocontinue()
			Cmds.continue_t((StaticVal.problem)) # type: ignor
			StaticVal.save_static()
			return

	def protest(self, pid, description):
		probname = netloc.question(pid)
		text = AutoLog.log_success.format(pid, probname)
		StaticVal.protest.append([text, description])


if __name__ == "__main__":
	Cmds()
	fire.Fire(Cmds)
