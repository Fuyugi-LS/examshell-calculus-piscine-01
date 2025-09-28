# compile the follow code into executable file, in cmder, and run it
import shlex
import cmd2 # type: ignore
import cmdefine
import os

slang = "python cmdefine.py"

class Examshell(cmd2.Cmd):
	isinit = False
	prompt = "> "
	meta = cmdefine.Meta().data #type: ignore

	def preloop(self):
		os.system("clear")
		os.system(f"{slang} preloop")

	def do_examshell(self, _):
		if Examshell.isinit:
			os.system("echo examshell is not a recognized command, alias, or macro.")
			return
		os.system(f"{slang} examshell")	
		Examshell.isinit = True

	def postloop(self):
		print(self.meta["finish"]) #type: ignore

	def do_protest(self, argv):
		if not Examshell.isinit:
			os.system("echo protest is not a recognized command, alias, or macro.")
			return
		argv_safe = shlex.quote(argv) if argv else ""
		os.system(f"{slang} grademe --verdict pass -f -p --description {argv}")

	def do_finish(self, _):
		return True

	def do_grademe(self, argv):
		if not Examshell.isinit:
			os.system("echo grademe is not a recognized command, alias, or macro.")
			return
		os.system(f"{slang} grademe {argv}")


if __name__ == "__main__":
	Examshell().cmdloop()
