# Generate SSH key
ssh-keygen -t ed25519 -C "your_email@example.com" -f ~/.ssh/github_account2

# Start SSH agent
eval "$(ssh-agent -s)"

# Add private key
ssh-add ~/.ssh/github_account2

# Display public key
cat ~/.ssh/github_account2.pub

# Add the displayed key to the new GitHub account
# GitHub → Settings → SSH and GPG keys → New SSH key

# Test authentication
ssh -T git@github.com

# Clone using SSH
git clone git@github.com:<github-account2>/<repository>.git

# Enter repository
cd <repository>

# Check branch
git branch

# Pull
git pull

# Make changes

# Check status
git status

# Stage changes
git add .

# Commit
git commit -m "Your commit message"

# Push
git push