# Setup — 5 minutes

A GitHub profile README only appears if the repository is named **exactly** like your username.

## 1. Create the repository
1. Go to https://github.com/new
2. Repository name: `Gethubsathvik` (must match your username exactly)
3. Set it to **Public**, tick **Add a README** (you will overwrite it), and create it.

## 2. Upload the files
Copy this folder's contents into the repo root so it looks like:

```
Gethubsathvik/
├── README.md
├── SETUP.md              (optional, can be deleted)
├── scripts/
│   └── update_readme.py
└── .github/
    └── workflows/
        ├── snake.yml
        └── update-readme.yml
```

Easiest way from a terminal:

```bash
git clone https://github.com/Gethubsathvik/Gethubsathvik.git
cd Gethubsathvik
# copy the unzipped files in here, then:
git add .
git commit -m "feat: interactive profile README"
git push
```

## 3. Allow the workflows to push
Repo → **Settings → Actions → General → Workflow permissions** → choose **Read and write permissions** → Save.

## 4. Run the workflows once
Repo → **Actions** tab → run **Generate Contribution Snake** and **Update Profile README** with **Run workflow**.
The snake image is published to an `output` branch; after the first run it shows up in your profile.

## What updates automatically
| Part | Refresh |
| :-- | :-- |
| Contribution snake | every 12 hours |
| Recently updated repositories + timestamp | daily |
| Stats cards, streak, trophies, activity graph | live, on each page load |

## Notes
- The stats cards use public community services (github-readme-stats, streak-stats, etc.). If one is briefly down, its image may not load.
- Private contribution counts only show if you enable *Private contributions* in your GitHub profile settings.
- To pin different projects, edit the `repo=` values in the **Featured Projects** section.
