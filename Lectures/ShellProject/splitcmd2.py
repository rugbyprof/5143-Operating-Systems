"""
Discussion in the TTh class about handling the processing of commands
"""

def grabFlags(cmd):
    flags = []
    cmd = cmd.split()
    for f in cmd:
        if '-' in f:
            flags.append(f.lstrip('-'))

    return ''.join(flags)



# Example commands
cmd = 'ls /etc/hosts -lah | grep .txt > outfile.txt'
cmd = 'ls -l  /usr/local -ah /home/runner/5143shellhelp/ | grep nix > out'
cmd = 'history | grep ls | wc -l > out'
cmd = 'grep < somefile.txt > outfile.txt'
cmd = 'history | grep ls | wc -l > out'
cmd = 'ls -lah | grep cd'
cmd = 'history | grep ls | wc -l > out'

# splits on spaces
print(cmd.split())

# check if redirect to std out is in the string
if '>' in cmd:
    # confirms you redirect to a file
    cmd = cmd.split('>')


print(cmd)

# split command if any `pipes` exist
cmds = cmd[0].split('|')

print(cmds)

# iterate over individual commands
for cmd in cmds:
    print(cmd.split())



# example dictionary to hold process command info
c = {
    'cmd':'ls',
    'params':['/usr/bin','/home'],
    'flags':'lah'
}

flags = grabFlags('ls -l /usr/bin/ -ah')
print(flags)