class Command(object):
	def __init__(self, cmd,input_file=''):
		self.cmd = cmd
		self.process = None
		self.input_file = input_file
		self.output = None
		self.status = None
		self.error = None
	def run(self, timeout):
		def target():
			#print 'Thread started'
			print self.cmd
			self.process = Popen(self.cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE)
			stream=None
			if self.input_file != '':
				a = open(self.input_file)
				stream  = a.read()
				a.close()
			[self.output,self.error] = self.process.communicate(input=stream)
			#print 'Thread finished'

		thread = threading.Thread(target=target)
		thread.start()

		thread.join(timeout)
		if thread.is_alive():
			self.process.terminate()
			thread.join()
			self.status =-1
		return  [self.process.returncode,self.output,self.error]

