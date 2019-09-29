
def queue_task():
	scheduler.queue_task('demo1', prevent_drift = True, repeats = 5, period = 5)
	
