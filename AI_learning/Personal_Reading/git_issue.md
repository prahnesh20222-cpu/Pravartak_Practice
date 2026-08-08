# Git Synchronization Troubleshooting Summary

This document summarizes the permission, identity, and branch divergence issues encountered while syncing an Obsidian vault repository across a Linux machine and a Windows machine, along with the steps taken to resolve them.

---

## 💻 Part 1: The Linux Machine Issues

### What Happened?
1. **Permission Denied Error:** The project initially failed to commit because Git commands were executed using elevated privileges (`sudo` or the `root` account). This changed the file ownership inside `.git/objects`, blocking your normal user account from writing new database trees.
2. **Identity Missing Error:** Operating as `root` caused Git to look for your name and email settings inside the root user profile (`/root/.gitconfig`), which was completely empty.
3. **SSH Key Disconnect:** Because SSH keys are isolated by user accounts, the `root` profile could not see or access the SSH keys you originally created under your normal user profile, causing network commands to fail.

### Commands Used / Tried
* To hand file ownership back to your regular user profile:
  ```bash
  sudo chown -R (whoami):(id -gn) .git
  ```
* To configure the Git user identity globally for the profile:
  ```bash
  git config --global user.name "Your Name"
  git config --global user.email "your.email@example.com"
  ```
* To check what keys the root profile could see:
  ```bash
  ls -la /root/.ssh
  ```
* To generate a fresh SSH key specifically for the root user:
  ```bash
  ssh-keygen -t ed25519 -C "root@hp-notebook"
  cat /root/.ssh/id_ed25519.pub
  ```
* To test the secure connection to GitHub:
  ```bash
  ssh -T git@github.com
  ```

---

## 🪟 Part 2: The Windows Machine Issues

### What Happened?
1. **Missing SSH Keys / Path Swap:** The Windows device threw a `Could not read from remote repository` error during a `git pull`. Because the terminal environment was likely elevated or confused, Git was hunting for keys inside the hidden system profile folder (`C:\Windows\System32\...`) instead of your standard user profile folder (`C:\Users\Your_Username\.ssh\`).
2. **File System Locks (.obsidian cache):** Obsidian automatically rewrites a temporary file called `.obsidian/workspace.json` to keep track of your open tabs. Git got stuck in an "unmerged paths" conflict because it couldn't safely overwrite or delete this active cache file while trying to merge changes from your Linux machine.
3. **Diverged Branches:** Both machines had made unique changes—your Windows machine had 2 unique commits locally, while GitHub was holding changes pushed from your Linux machine. This prevented a standard automated pull.

### Commands Used / Tried
* To force Windows to route environmental requests to your proper user profile:
  ```bash
  setx HOME %USERPROFILE%
  ```
* To safely check for hidden key files inside Git Bash:
  ```bash
  ls -la ~/.ssh
  ```
* To force Git Bash to manually add your existing key into its running memory:
  ```bash
  eval \$(ssh-agent -s) && ssh-add ~/.ssh/id_ed25519
  ```
* To force-align a stuck project's network remote URL structure:
  ```bash
  git remote set-url origin git@github.com:your_username/your_repository_name.git
  ```
* To drop a broken/stuck rebase loop state manually:
  ```bash
  git rebase --abort
  rm -rf .git/rebase-apply .git/rebase-merge
  git reset --mixed HEAD
  ```
* To force Git to overwrite the problematic local workspace cache file using GitHub’s version:
  ```bash
  git checkout --theirs .obsidian/workspace.json
  git add .obsidian/workspace.json
  git merge --continue
  ```
* To record file deletions you intentionally made while safely ignoring the unstaged `.obsidian` background cache files:
  ```bash
  git add . --update
  git commit -m "Remove deleted files"
  ```
* To instantly clear out and discard all lingering, noisy, unstaged `.obsidian` changes left in the workspace folder:
  ```bash
  git checkout -- .
  ```
* To upload your finalized, combined history to GitHub:
  ```bash
  git push origin main
  ```

---

## 🔑 Key Concepts Learned

* **`git push` vs `git push origin main`**: Explicitly naming the server (`origin`) and branch (`main`) leaves zero room for error. A simple `git push` works fine as a shortcut, but only *after* Git has established an active upstream tracking link via `git push --set-upstream origin main`.
* **`git checkout -- .`**: The `--` tells Git to look strictly at paths, and the `.` stands for "this entire directory". Running this completely cleans your workspace by undoing any unsaved edits back to your last successful commit state.
* **The Root Pitfall:** Avoid using `sudo git` or running Git tools as an Administrator unless absolutely necessary. Git isolates identities and security handshakes by user accounts, and shifting permissions breaks local tracking databases.
