import  os
class BatchRename():
	def __init__(self):
		self.path = 'trainB'
	def rename(self):
		filelist = os.listdir(self.path)
		total_num = len(filelist)
		i=1

		for item in filelist:
			if item.endswith('.jpg') or item.endswith('.jpeg'):
				src=os.path.join(os.path.abspath(self.path), item)
				#dst=os.path.join(os.path.abspath(self.path), 'name'+str(i) + '.jpeg') 
				dst=os.path.join(os.path.abspath(self.path), str(i) + '.jpeg')
				try:
					os.rename(src, dst)
					i=i+1
				except:
					continue 
		print('total %d to rename & converted %d jpgs' % (total_num, i))
if __name__=='__main__':
	demo = BatchRename()
	demo.rename()