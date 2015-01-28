from subprocess import Popen, PIPE

# Run "cat", which is a simple Linux program that prints it's input.
process = Popen(['/bin/cat'], stdin=PIPE, stdout=PIPE)
process.stdin.write('Hello\n')
print repr(process.stdout.readline()) # Should print 'Hello\n'
process.stdin.write('World\n')
print repr(process.stdout.readline()) # Should print 'World\n'

# "cat" will exit when you close stdin.  (Not all programs do this!)
process.stdin.close()
print 'Waiting for cat to exit'
process.wait()
print 'cat finished with return code %d' % process.returncode
