

cmd = 'ls /etc/hosts -lah | grep .txt > outfile.txt'
cmd = 'ls -l  /usr/local -ah /home/runner/5143shellhelp/ | grep nix > out'
cmd = 'history | grep ls | wc -l > out'
cmd = 'grep < somefile.txt > outfile.txt'
cmd = 'history | grep ls | wc -l > out'

left,right = cmd.split('>')

print(left)
print(right.strip())

cmds = left.split('|')

i = 0
for cmd in cmds:
    cmds[i] = cmd.strip()
    i += 1
print(cmds)

parts = {
    'cmd':'',
    'flags':'',
    'params':''
}



