#
# Some support for Full Maude on top of the Python bindings
#

import os
import maude
import sys
import re


def read_all(fd: int) -> str:
	"""Read all from a file descriptor, the close it"""

	tmp = os.read(fd, 500)

	# We assume there is a zero-character as sentinel
	while tmp[-1]:
		tmp += os.read(fd, 500)

	os.close(fd)

	return tmp


def input_str(txt: str) -> (str, str):
	"""Input the argument to Maude and get the result as string"""

	# Save standard input and error to be restored
	stdout_copy = os.dup(1)
	stderr_copy = os.dup(2)

	# Create two pipes for capturing standard input and error
	out_rd, out_wr = os.pipe()
	err_rd, err_wr = os.pipe()

	# Replace the standard stream by the pipes
	os.dup2(out_wr, 1)
	os.dup2(err_wr, 2)

	# Close the copies of the write ends
	os.close(out_wr)
	os.close(err_wr)

	maude.input(txt)

	# Add a sentinel to the end of input and also allows
	# using read without blocking in a portable way
	sys.stdout.write('\0')
	sys.stdout.flush()
	sys.stderr.write('\0')
	sys.stderr.flush()

	out_txt = read_all(out_rd)
	err_txt = read_all(err_rd)

	# Restore the standard streams
	os.dup2(stdout_copy, 1)
	os.dup2(stderr_copy, 2)

	# Close the copies of the standard streams
	os.close(stdout_copy)
	os.close(stderr_copy)

	return out_txt[:-1].decode(), err_txt[:-1].decode()


def getFMModule(name: str) -> maude.Module:
	"""Get a Full Maude module"""

	module_text, _ = input_str(f'(red in META-LEVEL : upModule({name}) .)')

	# Remove escape characters from the string
	module_text = re.sub('\x1b\[[0-9;]+m', '', module_text)

	# Get the result of the command (if any)
	index = module_text.find('result StratModule :')

	if index < 0:
		return None

	# Parse the metarepresentation in META-LEVEL
	ml = maude.getModule('META-LEVEL')
	metamodule = ml.parseTerm(module_text[index + 20:])

	return maude.downModule(metamodule) if metamodule else None
