import os
import optparse
import yaml
from duplicity.path import Path

def menu():
    p = optparse.OptionParser(description='A tool for managing jenkins environments',
                                        prog='jenkex',
                                        version='1.0',
                                        usage= "usage: %prog  ")
    p.add_option('-s' ,'--source' ,action ='store', type="string", dest="source", default="" ,help="base makefile location")
    p.add_option('-d' ,'--debug' ,action ='store_true', dest="debug", default=True ,help="print out debug information ")
    (options,args) = p.parse_args()
    options = options.__dict__
    return options

def find_file(path, search_list):
	"""Generator which will find all files of a given name
	@param         path: path of the file in question 
	@param  search_list: array of searchables
	"""
	for root, dirs, files in os.walk(path):
		for file in files:
			for search in search_list:
				if search in file:
					yield "%s/%s" % (root,file)
				else:
					pass

def find_line(path,search_list,removes_list):
	"""Generator which passes a single line, based on search value
	@param         path: path of the file in question 
	@param  search_list: array of searchables
	@param removes_list: array of chars to take out 
	"""
	with open(path) as makefile:
		for line in makefile:
			for search in search_list:
				if search in line:
					for remove in removes_list:
						line = line.strip().replace(remove,'')
					yield line
				else:
					pass

def make_map(root_path,debug=False):
	""" Builds a nested dictionary as a map
	@param root_path: base of isi directory
	@param debug: will print out debug info 
	"""
	find_make = find_file(root_path,['Makefile'])
	map = {}
	for path in find_make:# get one makefile path
		find_include = find_line(path,['.include'],['.include','<','>','"'])# search makefile for .include string
		includes = []
		for line in find_include:
			includes.append(line)# add all includes
		map[path]={'includes':includes}# add to map
	with open('map.yml', 'w') as yaml_file: # write it to yml file
		yaml.dump(map,yaml_file, default_flow_style=False)
	return map
	
	"""
	with open('map.yml', 'w') as yaml_file:
		yaml.dump(map,yaml_file, default_flow_style=False)
	
	if debug:
		read_map = None
		with open('map.yml', 'r') as yaml_file:
			read_map = yaml.load(yaml_file)
		cnt_mks = 0
		for path,_includes in read_map.iteritems():
			print "%s" % (path)
			cnt_mks +=1
			for key, include in _includes.iteritems():
				for i in include:
					print "       %s" % (i)
		print "\nNumber of Makefiles: %s" % (str(cnt_mks))
	"""
	
	
	

if __name__ == "__main__":
	options = menu()
	make_map(options.get("source"),debug=options.get('debug'))

		
	
	
	
			
			
		