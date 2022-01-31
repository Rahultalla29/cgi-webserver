################################################################################
# INFO1112 - ASSIGNMENT 2 - CGI WEBSERVER
# The Following Is The Implementaion Of Simple CGI Web-Server 
# Created By : Rahul Talla
# Date : 22/11/2020
#################################################################################

import socket, os, sys, gzip

# Role - Config Parser 
# Handles errors in config, if successful returns list of tuple mapped to field
def read_Config(cmd_Line_Args) :
	try :
		if len(cmd_Line_Args) != 2:
			exit("Missing Configuration Argument")

		config_File = cmd_Line_Args[1]
		c_File = open(config_File,"r")
		ls_Of_Fields =[]
		required_Fields = ["staticfiles","cgibin","port","exec"]
		fields_Already_Checked = []
		count = 0
		
		for line in c_File:
			value = tuple(line.strip("\n").split("="))

			if (value[0] in required_Fields) and (not value[0] in fields_Already_Checked) :
				count +=1
				fields_Already_Checked.append(value[0])
				ls_Of_Fields.append(value)
			else :
				exit("Missing Field From Configuration File")
		
		c_File.close()

		if count < 4:
			exit("Missing Field From Configuration File")

		
		return ls_Of_Fields    #[(f1,"param 1"),(f2,"param 2"),....(fk,"param k")]

	except FileNotFoundError as e:
		("Unable To Load Configuration File")

# Role - Map header to data 
# Retreives respective header and its data. Returns list of tuples with header and data
def extract_header_data(client_data):

	content_type_found = False
	headers = ["Accept: ","Host: ","User-Agent: ","Accept-Encoding: ","Content-Type: ","Content-Length: "]
	content_type = [ (".txt","text/plain") ,(".html","text/html"),( ".js","application/javascript"),
				(".css","text/css"),(".png","image/png"),(".jpg","image/jpeg"),(".jpeg","image/jpeg"),(".xml","text/xml")]
	header_data = []

	for header in headers: #Check if header in client data match with header in headers
		for elem in client_data:
			if header in elem: 
				if header == "Content-Type: ": # Map content-type to expected cases
						content_type_found = True
						for type in content_type:
							if type[0] in client_data[0]:
								header_data.append((header,type[1]))

				# Format and append tuple to list
				else :
					format_elem = elem.replace(header,'')
					format_elem = format_elem.strip("\r")
					header_data.append((header,format_elem))
	
	if not content_type_found:
		for type in content_type:
			if type[0] in client_data[0]:
				header_data.append(("Content-Type: ",type[1]))

	return header_data

# Role - Extract and map query string to its data 
# Retreives respectives varaibels from Get header string in client_data and handles expected cases
# Set enivronment variable if found , else return None
def extract_query_string(client_data):
	get_method = "GET "
	for elem in client_data: 
		if (get_method in elem) and ("?" in elem): 
			get_data,variables = elem.split("?")
			variables = variables.split("&")
			last_variable,http_protocol = variables[len(variables)-1].split(" ")
			variables[len(variables)-1] = last_variable
			os.environ["QUERY_STRING"] = "&".join(variables)
			return variables
	return None

# Role - Extract and map file-type to its address
# Determine what type of file request from client and return tuple (type,addr), else return None
def is_file_or_cgi(config_formatted,client_formatted):

	cgi_dist= ""
	files_dist = ""
	for elem in config_formatted:
		if elem[0] == "staticfiles":
			files_dist = elem[1]
		elif elem[0] == "cgibin":
			cgi_dist = elem[1]

	if cgi_dist != "" and (cgi_dist.strip("./") in client_formatted[0]):
		return ("cgi",cgi_dist)
	
	elif files_dist != ""  and (files_dist.strip("./") in client_formatted[0]):
		return ("file",files_dist)

	else :
		return ("file",files_dist)

# Role - Extract and map file type to its destination
# Determine file-type and send environment variables, successful return tuple (type,dest)
def retrieve_file(destination,client_formatted):
	
	get_method_ls = client_formatted[0].split(" ")
	http_method = get_method_ls[0]
	os.environ["REQUEST_METHOD"] = http_method

	if (destination[0]) == "cgi":
		file = client_formatted[0].strip(http_method  + " ")
		if "?" in file:
			addr,other_data = file.split("?")  # If variables exist
		else :
			addr,http_protocol = file.split(" ")  # If no variables exist
		os.environ["REQUEST_URI"] = addr
		return ("cgi",addr)

	elif (destination[0]) == "file":
		file = client_formatted[0].strip(http_method  + " ")
		if "?" in file:
			addr,other_data = file.split("?")
		else :
			addr,http_protocol = file.split(" ")
		if not (destination[1].strip("./") in addr) :  # No file given, point to index.html
			if addr == "/":
				addr = destination[1] + "/index.html"
			else:
				addr = destination[1] + addr
			return ("file",addr)

		return ("file",addr)

# Role - Determine if file exists
def file_exists(type_addr):
	try :
		file_name = type_addr[1].strip("./")
		f = open(file_name)
		f.close()
		return True
	except IOError:
		return False

# Role - Receive data from client, return formatted data and client
def get_client_data(server):
	client,addr = server.accept()
	os.environ["REMOTE_ADDRESS"] = addr[0] ## client ip addr
	os.environ["REMOTE_PORT"] = str(addr[1]) ## client port
	data = client.recv(1024).decode("utf-8")
	formatted = data.split("\n")	
	return formatted,client

# Role - Retrieve HTTP protocol
def get_http_type(header_data,formatted) :
	content_type = None
	http = None
	for header in header_data:
		if header[0] == "Content-Type: ":
			content_type = header[1]
	list = formatted[0].split(" ")
	http = list[len(list)-1].strip("\r")
	
	return (http,content_type)

# Role - Getter method, returns server port
def get_port(config):

	if config == None:
		exit("Unable To Load Configuration File")
		
	for field in config :
		if field[0] == "port":
			return int(field[1])

# Role - Getter method, returns executable path
def get_exec_path(config):

	for field in config :
		if field[0] == "exec":
			return field[1]

# Role - Setter method, sets all initial environment variables found
def set_environ_var(header_data):

	for elem in header_data:
		if elem[0] == "Accept: ":
			os.environ["HTTP_ACCEPT"]  = elem[1]
		elif elem[0] == "Host: ":
			os.environ["HTTP_HOST"]  = elem[1]
		elif elem[0] == "User-Agent: ":
			os.environ["HTTP_USER_AGENT"]  = elem[1]
		elif elem[0] == "Accept-Encoding: ":
			os.environ["HTTP_ACCEPT_ENCODING"]  = elem[1]
		elif elem[0] == "Content-Length: ":
			os.environ["CONTENT_LENGTH"]  = elem[1]

# Role - Determine if compressed data sending is required
def compress_file(header_data):
	for elem in header_data :
		if  "gzip" in elem[1]: 
			return True
	return False
# Role - Generalised list contains method
def value_in_list(value,list) :
	for elem in list:
		if value in elem:
			return True
	return False

# Role - Static file handler
# Handles all cases of static file request and sends to client
def static_file_handler(client,http_content,type_addr,header_data,success_msg,content_type_msg):

	client.send(success_msg.encode())
	if (http_content[1] != None):
		client.send(content_type_msg.encode())
	elif "index" in type_addr[1]:
		os.environ["CONTENT_TYPE"] = "text/html"  # Set new content-type
		client.send("Content-Type: {}\n\n".format("text/html").encode())
	if (".png" in type_addr[1]):
		lines = open(type_addr[1].strip("./"),'rb').read()
		client.send(lines)
		
	elif compress_file(header_data):    # Extension - Send compressed content mode
		raw_data = open(type_addr[1].strip("./"),"rb").read()
		output = gzip.GzipFile(type_addr[1].strip("./") + ".gz", 'wb') # Open gzip file and write compressed content
		output.write(raw_data)
		output.close()
		compressed_lines = open(type_addr[1].strip("./") + ".gz", 'rb').read()
		client.send(compressed_lines) # send compressed content of gzip file to client 
	else:
		lines = open(type_addr[1].strip("./")).read()
		client.send(lines.encode())

	client.close()

# Role - CGI program handler
# Handles all cases of CGI program request and sends output to client
def cgi_handler(client,exec_path,type_addr,http_content,header_data):

	r2,w2  = os.pipe() # Create new pipe for the current process
	pid2 = os.fork() # Create child for each process, concurrently

	if pid2 == 0: # Child
		
		os.close(r2)
		os.dup2(w2,1) # Create duplicate file descriptor to redirect stdout to parent
		os.execv(exec_path,[exec_path,type_addr[1].strip("./")])

	# Parent
	else:
		
		os.close(w2)
		r2 = os.fdopen(r2)  # Read redirected stdout
		contents = r2.read()
		value = os.wait()
		content_ls = list(contents.split("\n"))

		if value[1] != 0: # Error Case: exit code / pid not zero
			client.send("{} 500 Internal Server Error\n".format(http_content[0]).encode()) 
		elif (value[1] == 0) and value_in_list("Status-Code: ",content_ls) : # Built-in Status Code Case
			
			for elem in content_ls:
				if "Status-Code: " in elem :
					new_code = elem.replace("Status-Code: ","")
					http_reponse = "{} {}\n".format(http_content[0],new_code).encode()
					client.send(http_reponse)
				elif elem == "":
					client.send("\n".encode())
				else :
					client.send(elem.encode())
			
		elif ("Content-Type" in contents) and (not ("HTTP" in contents)): # Built-in Content Type Case
			client.send("{} 200 OK\n".format(http_content[0]).encode())
			client.send(contents.encode())
			
		elif compress_file(header_data):    # Extension - Send compressed content mode
			raw_data =  str.encode(contents)
			output = gzip.GzipFile(type_addr[1].strip("./") + ".gz", 'wb') # Open gzip file and write compressed content
			output.write(raw_data)
			output.close()
			compressed_lines = open(type_addr[1].strip("./") + ".gz", 'rb').read()
			client.send(compressed_lines) # send compressed content of gzip file to client 

		else :
			client.send("{} 200 OK\n\n".format(http_content[0]).encode())
			client.send(contents.encode())

		client.close()


# Role - Main Function - Brings together all aspects of the program function
def main():

	config = read_Config(sys.argv)
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
	server.bind(("127.0.0.1",get_port(config)))
	server.listen()
	os.environ["SERVER_ADDR"] = "127.0.0.1"
	os.environ["SERVER_PORT"] = str(get_port(config))

	while True:
		formatted,client = get_client_data(server)
		header_data = extract_header_data(formatted)
		set_environ_var(header_data)
		variables = extract_query_string(formatted)
		destination = is_file_or_cgi(config,formatted)
		type_addr = retrieve_file(destination,formatted)
		http_content = get_http_type(header_data,formatted)
		exec_path = get_exec_path(config)
		error_html = '<html>\n<head>\n\t<title>404 Not Found</title>\n</head>\n<body bgcolor="white">\n<center>\n\t<h1>404 Not Found</h1>\n</center>\n</body>\n</html>\n'
		success_msg = "{} 200 OK\n".format(http_content[0])
		content_type_msg = "Content-Type: {}\n\n".format(http_content[1])
		error_msg = "{} 404 File not found\n\n".format(http_content[0])

		pid = os.fork()

		# Child Process
		if pid == 0:

			if type_addr[0] == "file" and file_exists(type_addr):

				static_file_handler(client,http_content,type_addr,header_data,success_msg,content_type_msg)

			elif type_addr[0] == "file" and (not file_exists(type_addr)) :

				client.send(error_msg.encode())
				client.send(error_html.encode())
				client.close()
			
			elif type_addr[0] == "cgi" and file_exists(type_addr):

				cgi_handler(client,exec_path,type_addr,http_content,header_data)

			elif type_addr[0] == "cgi" and (not file_exists(type_addr)) :
				client.send(error_msg.encode())
				client.send(error_html.encode())
				client.close()
		
		# Parent Process
		else :

			client.close()

if __name__ == '__main__':
	main()
