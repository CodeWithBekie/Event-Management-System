# Event Management System

A Django-based web application for managing events, attendees, and related tasks.

---

## 🚀 Getting Started

Follow these steps to set up and run the project locally.

### 1️⃣ Clone This Project
Clone the repository from GitHub:
```bash
git clone https://github.com/CodeWithBekie/Event-Management-System.git
```

### 2️⃣ Go to Project Directory
```bash
cd django-event-management
```

### 3️⃣ Create a Virtual Environment
```bash
python3 -m venv env
```

### 4️⃣ Activate Virtual Environment
Mac/Linux:
```bash
source env/bin/activate
```
Windows (PowerShell):
```bash
.\env\Scriptsctivate
```

### 5️⃣ Install Requirements
```bash
pip install -r requirements.txt
```

### 6️⃣ Migrate Database
```bash
python manage.py migrate
```

### 7️⃣ Create Superuser
```bash
python manage.py createsuperuser
```
Follow the prompts to set up an admin account.

### 8️⃣ Run the Project
```bash
python manage.py runserver
```
Open your browser and go to: **http://127.0.0.1:8000/**

---

## 🧑‍💻 Git & GitHub Basics (Beginner Guide)

These steps show how to work with Git and GitHub directly in **VS Code**.  
*(References: [Git Official Docs](https://git-scm.com/doc), [GitHub Docs](https://docs.github.com))*

### Prerequisites
- Install [Git](https://git-scm.com/downloads).
- Install [VS Code](https://code.visualstudio.com/) and the **GitHub Pull Requests and Issues** extension (recommended).
- Sign in to GitHub in VS Code:  
  *View → Command Palette → “GitHub: Sign in”.*

---

### 1️⃣ Fetch Latest Changes
Fetch downloads new data from the remote repository without merging:
- Open VS Code terminal or use the Source Control panel.
- Run:
  ```bash
  git fetch origin
  ```

### 2️⃣ Pull Latest Changes
Pull fetches and merges the latest changes from the remote branch into your local branch:
```bash
git pull origin main
```
*(Replace `main` with your branch name if different.)*

### 3️⃣ Make Your Changes
Edit files or add new code.  
Stage changes:
```bash
git add .
```
Commit changes:
```bash
git commit -m "Describe your changes"
```

### 4️⃣ Push Your Changes
Send your committed changes to GitHub:
```bash
git push origin main
```
If you are on a different branch, replace `main` with that branch name.

### 5️⃣ Create a New Branch
Always create a new branch for a feature or fix:
```bash
git checkout -b feature/your-branch-name
```
Push the new branch to GitHub:
```bash
git push -u origin feature/your-branch-name
```

### 6️⃣ Open a Pull Request (PR)
1. Go to your repository on GitHub.
2. Click **Compare & pull request**.
3. Review your changes and click **Create pull request**.
4. Add a title, description, and reviewers if needed.
5. Once approved, click **Merge pull request**.

---

## 🛠 Helpful VS Code Tips
- **Source Control Panel**: View changes, stage/commit, and manage branches visually.
- **Command Palette** (`Ctrl+Shift+P` or `Cmd+Shift+P`): Search commands like “Git: Fetch” or “Git: Checkout to…”.

---

## 📚 Resources
- [Git Official Documentation](https://git-scm.com/doc)
- [GitHub Docs: Hello World](https://docs.github.com/en/get-started/quickstart/hello-world)
- [VS Code & GitHub](https://code.visualstudio.com/docs/sourcecontrol/github)

---

## 🤝 Contributing
1. Fork the repo.
2. Create a branch: `git checkout -b feature/awesome-feature`.
3. Commit changes: `git commit -m "Add awesome feature"`.
4. Push to branch: `git push origin feature/awesome-feature`.
5. Open a Pull Request.

---

**Enjoy building and contributing!**
