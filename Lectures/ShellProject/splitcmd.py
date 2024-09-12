# Example commands
cmd = "grep < somefile.txt > outfile.txt"
cmd = "history | grep ls | wc -l > out"
cmd = "ls -l  /usr/local -ah /home/runner/5143shellhelp/ | grep nix > out"
cmd = "ls /etc/hosts -lah | grep .txt > outfile.txt"
cmd = "grep < somefile.txt > outfile.txt"
cmd = "history | grep ls | wc -l > out"
cmd = "ls -l  /usr/local -ah /home/runner/5143shellhelp/ | grep nix > out"
cmd = "ls -lah | grep cd"
cmd = "ls /etc/hosts -lah | grep .txt > outfile.txt"

# splits on spaces
print(cmd.split())
