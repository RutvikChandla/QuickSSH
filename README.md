# quickssh

Prerequisites 
- python
- applescript
- iterm

```
# change your user name in ssh_manager.py
def ssh_command(row):
    ip = row["ip"]
    return f'ssh -J username@hop username@{ip}'
```

Add in conf.yaml
```
- ip: x.x.x.x
  region: use
  nickname: component-nickname
  tag: tag1 <-- This will be use to search
```

Can add alias to .zshrc / .bashrc
```
bssh() {
  python3 <PATH>/ssh_manager.py
}
```
