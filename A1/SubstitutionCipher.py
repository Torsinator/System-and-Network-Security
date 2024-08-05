# SENG2050 A1
# Coded by: Tors Webster c3376513
# 02/08/2024

import string
import re

def createLetterMap() -> dict:
	"""Creates the initial letter map

	Returns:
		dict: Dictionary of each ascii lowercase letter to itself
	"""
	letter_map = {}
	for letter in string.ascii_lowercase:
		letter_map[letter] = letter
	return letter_map

def searchDictionary(partial_word: str):
	"""Prints potential word matches given a partially deciphered string

	Args:
		partial_word (str): String to search for
	"""
	# Open word list file (Using Moby Words II public domain)
	# https://digital.library.upenn.edu/webbin/gutbook/lookup?num=3201
	file_obj = open('wordList.txt', 'r')
	dictionary = file_obj.read().splitlines()	# Create our dictionary of words
	matches = []	# list to store matches
	regex = ''	# regex, replacing each lowercase letter (cipher) with a '.' wildcard
	for letter in partial_word:
		if letter in string.ascii_lowercase:
			regex += '.'	# Add wildcard
		else:
			regex += letter.lower()	# Add the letter
	for word in dictionary:
		if len(word) == len(partial_word) and re.search(regex, word):
			matches.append(word)
	print('Matches for {}: {}'.format(partial_word, matches))

def printText(ciphertext: str, letter_map: dict) -> str:
	"""Replaces each letter in the ciphertext using the letter_map

	Args:
		ciphertext (str): Text to be replaced
		letter_map (dict): Letter mapping dictionary

	Returns:
		string: _description_
	"""
	translated = ciphertext.translate(str.maketrans(letter_map))
	print(translated)
	return translated

def main():
	"""Shows the steps in the deciphering process
	"""
	# Ciphertext to be deciphered
	# Any lowercase denotes ciphertext, UPPERCASE is plaintext
	ciphertext = 'wep umpp rgmusfp br znj rwmpwfepk ngw wn s qsmyp powpzw agw sffnmkbzy wnngm srrgvcwbnz wep vswpmbsqr grpk smp cpmupfwqt rwmpwfesaqp'
	letter_map = createLetterMap()
	# After discovering t, h, e using frequencies
	letter_map['w'] = 'T'
	letter_map['e'] = 'H'
	letter_map['p'] = 'E'
	printText(ciphertext, letter_map)
	# Now we have: THE umEE rgmusfE br znj rTmETfHEk ngT Tn s qsmyE EoTEzT agT sffnmkbzy Tnngm srrgvcTbnz THE vsTEmbsqr grEk smE cEmuEfTqt rTmETfHsaqE

	# After an educated guess at s --> A
	letter_map['s'] = 'A'
	printText(ciphertext, letter_map)
	# Now we have: THE umEE rgmuAfE br znj rTmETfHEk ngT Tn A qAmyE EoTEzT agT Affnmkbzy Tnngm ArrgvcTbnz THE vATEmbAqr grEk AmE cEmuEfTqt rTmETfHAaqE

	# Search for possible matches for 'Tn'
	searchDictionary('Tn')
	# Returns ['t.', 'ta', 'ti', 'to']
	# 'to' is most likely so n --> O
	letter_map['n'] = 'O'
	printText(ciphertext, letter_map)
	# Now we have: THE umEE rgmuAfE br zOj rTmETfHEk OgT TO A qAmyE EoTEzT agT AffOmkbzy TOOgm ArrgvcTbOz THE vATEmbAqr grEk AmE cEmuEfTqt rTmETfHAaqE

	# Search for possible matches for 'umEE'
	searchDictionary('umEE')
	# Returns ['Cree', 'Klee', 'Rhee', 'Tree', 'agee', 'akee', 'alee', 'bree', 'dree', 'flee', 'free', 'ghee', 'glee', 'gree', 'knee', 'ogee', 'thee', 'tree']

	# 'free' is most likely as t is already found so words such as tree cannot be valid
	letter_map['m'] = 'R'
	letter_map['u'] = 'F'
	printText(ciphertext, letter_map)
	# Now we have: THE FREE rgRFAfE br zOj rTRETfHEk OgT TO A qARyE EoTEzT agT AffORkbzy TOOgR ArrgvcTbOz THE vATERbAqr grEk ARE cERFEfTqt rTRETfHAaqE

	# Search for possible matches for 'rgRFAfE'
	searchDictionary('rgRFAfE')
	# Returns ['carfare', 'surface', 'warfare']
	# must be 'surface' as f cannot be R (m --> R)
	letter_map['r'] = 'S'
	letter_map['g'] = 'U'
	letter_map['f'] = 'C'
	printText(ciphertext, letter_map)
	# Now we have: THE FREE SURFACE bS zOj STRETCHEk OUT TO A qARyE EoTEzT aUT ACCORkbzy TOOUR ASSUvcTbOz THE vATERbAqS USEk ARE cERFECTqt STRETCHAaqE

	# Search for possible matches for 'ACCORkbzy'
	searchDictionary('ACCORkbzy')
	# Returns: ['accordant', 'according', 'accordion']
	# Based on previous discovered letters, must be 'according'
	letter_map['k'] = 'D'
	letter_map['b'] = 'I'
	letter_map['z'] = 'N'
	letter_map['y'] = 'G'
	printText(ciphertext, letter_map)
	# Now we have: THE FREE SURFACE IS NOj STRETCHED OUT TO A qARGE EoTENT aUT ACCORDING TOOUR ASSUvcTION THE vATERIAqS USED ARE cERFECTqt STRETCHAaqE

	# From this it becomes obvious that:
	letter_map['j'] = 'T'
	letter_map['q'] = 'L'
	letter_map['o'] = 'X'
	letter_map['a'] = 'B'
	letter_map['v'] = 'M'
	letter_map['c'] = 'P'
	letter_map['q'] = 'L'
	letter_map['t'] = 'Y'
	print('Plaintext:')
	printText(ciphertext, letter_map)
	# The plaintext is: THE FREE SURFACE IS NOT STRETCHED OUT TO A LARGE EXTENT BUT ACCORDING TOOUR ASSUMPTION THE MATERIALS USED ARE PERFECTLY STRETCHABLE

if __name__ == '__main__':
	main()