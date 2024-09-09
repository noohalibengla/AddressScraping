#Spazer tool for processing web pages
#

from bs4 import BeautifulSoup
import pathlib
import re

#Variables to track the input, output and gained space
space_gained = 0
space_input = 0
space_output = 0

print("Welcome to Spazer\n")

with open('cities.txt', 'r') as f:
	cities = f.read()

cities = cities.split()
cities = [city.lower() for city in cities]

def getcities(text):
	text_s = text.lower()
	cityinds_t = []
	# print(cities[:100])
	for city in cities:
		citylist = re.finditer(r',(.|\n){,10}'+re.escape(city)+r'[^0-9a-zA-Z]', text_s)

		cityinds_t += [l.end(0) for l in citylist]

	if cityinds_t:
		cityinds = [cityinds_t[0]]

		for i in range(1,len(cityinds_t)):
			if cityinds_t[i] - cityinds_t[i-1] > 100:
				cityinds.append(cityinds_t[i])
	else: cityinds = cityinds_t

	return cityinds



	# text_city = text_s.split()
	# text_city = [re.sub(r"[^A-Za-z]+", '', tex) for tex in text_city]
	# text_city = [city for city in text_city if city in cities]




	


keywords = ["address", "contact"]


for x in range(5):
	filename = str(x) + ".html"
	file = pathlib.Path('input/' + filename)
	if (file.exists()):

		#Read each file
		print("Reading " + filename)
		f = open('input/' + filename, 'r', errors="ignore")
		contents = f.read()
		contents_small = contents.lower()   
		
		if '<address>' in contents_small:
			s_ind = contents_small.index('<address>')
			e_ind = contents_small.index('</address>')

			address = contents[s_ind:e_ind]


		#Remove html tags
		soup = BeautifulSoup(contents, 'lxml')		
		output = soup.get_text()



		#Your code begins  ###############################
		
		# print(output)

		add = []

		matchlist = re.finditer(r'[^0-9a-zA-Z][1-9]{1}[0-9]{5}[^0-9a-zA-Z]|[^0-9a-zA-Z][1-9]{1}[0-9]{3}(\s)+[0-9]{3}[^0-9a-zA-Z]', output)

		matchinds = [match.end(0) for match in matchlist]

		for ind in matchinds:
			temp_output = output[max(0, ind-200):min(ind+10, len(output))]
			# temp_ind = temp_output.index("\n\n")
			# print(output[ind-200:ind], '\n\n\nNext Address:')

			add.append(temp_output)
			output = output.replace(temp_output, ' '*(len(temp_output)))

		cityinds = getcities(output)
		# print(len(add))
		# add.append("NEXT PART STARTS \n\n\n\n\n\n")

		for ind in cityinds:
			temp_output = output[max(0, ind-190):min(ind+20, len(output))]
			# temp_ind = temp_output.index("\n\n")
			# print(output[ind-200:ind], '\n\n\nNext Address:')

			add.append(temp_output)
			# print(temp_output)
			# print(''*(len(temp_output))+)
			output = output.replace(temp_output, ' '*(len(temp_output)))

		
		for i in range(len(add)):
			if bool(re.match(r'^\s*$', add[i])):
				add[i] = '\n'
		# print('\n\n\nNext Address:\n\n\n'.join(add))
		# print(len(add))
		# break

		output = '\n'.join(add)


		#Your code ends  #################################			  
		
		#Write the output variable contents to output/ folder.
		print ("Writing reduced " + filename)
		fw = open('output/' + filename, "w")
		fw.write(output)
		fw.close()
		f.close()
		
		#Calculate space savings
		space_input = space_input + len(contents)
		space_output = space_output + len(output)
		
space_gained = round((space_input - space_output) * 100 / space_input, 2)

print("\nTotal Space used by input files = " + str(space_input) + " characters.") 
print("Total Space used by output files = " + str(space_output) + " characters.")
print("Total Space Gained = " + str(space_gained) + "%") 
	   
	

