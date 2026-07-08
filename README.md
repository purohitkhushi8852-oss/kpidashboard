# 📈 Business KPI Dashboard

An interactive dashboard tracking **Revenue, Profit, and Customer Growth** across
regions and segments, built with **Streamlit** and **Plotly**. Designed as a
practical exec-level view a business would use in a monthly review meeting.

## What it shows
| Section | Insight it gives the business |
|---|---|
| KPI cards | Total Revenue, Total Profit, Profit Margin %, New Customers, Customer Growth % |
| Monthly Revenue & Profit Trend | Line chart — track growth, seasonality, margin erosion over time |
| Customer Growth | New customers per month (bars) + cumulative customer base (line) on dual axis |
| Revenue by Region | Bar chart — which markets drive the business |
| Revenue by Segment | Donut chart — Enterprise vs SMB vs Consumer contribution |
| Filters (sidebar) | Date range, Region, Segment — everything recalculates instantly |
| Raw data + CSV export | Download exactly the slice you filtered |

## Project structure
```
Dashboard/
|-- app.py             # the Streamlit app
|-- data.csv            # sample dataset (24 months, 4 regions x 3 segments)
|-- generate_data.py    # script used to (re)generate data.csv
|-- requirements.txt
|-- README.md
```

---

## 🖥️ Step 1 — Set up in VS Code (run locally)

1. **Create a project folder** and open it in VS Code:
   ```bash
   mkdir kpi-dashboard
   cd kpi-dashboard
   code .
   ```
2. **Add the files** (`app.py`, `data.csv`, `generate_data.py`, `requirements.txt`)
   into this folder — create new files in VS Code's Explorer panel and paste
   the content in, or drag the downloaded files into the folder.
3. **Open a terminal in VS Code**: `Terminal → New Terminal`.
4. **(Recommended) Create a virtual environment:**
   ```bash
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # macOS/Linux:
   source venv/bin/activate
   ```
   You should see `(venv)` at the start of your terminal prompt.
5. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
6. **Run the app:**
   ```bash
   streamlit run app.py
   ```
7. Your browser opens automatically at `http://localhost:8501`. If not, copy
   that URL into your browser manually.
8. To stop the app, go back to the terminal and press `Ctrl + C`.

---

## 🐙 Step 2 — Push to GitHub

1. **Create a new repository** on [github.com/new](https://github.com/new)
   — name it e.g. `kpi-dashboard`, keep it **Public** (required for the free
   tier of Streamlit Community Cloud), and don't initialize with a README
   (you already have one).
2. In the VS Code terminal, inside your project folder, run:
   ```bash
   git init
   git add .
   git commit -m "Initial commit: Business KPI Dashboard"
   git branch -M main
   git remote add origin https://github.com/<your-username>/kpi-dashboard.git
   git push -u origin main
   ```
   Replace `<your-username>` with your actual GitHub username. If prompted,
   sign in to GitHub through VS Code's browser login flow.
3. Refresh your GitHub repo page — you should see all 5 files there.

---

## ☁️ Step 3 — Deploy on Streamlit Community Cloud

> Note: **GitHub Pages cannot run this app** — it only serves static
> HTML/CSS/JS, and Streamlit needs a live Python server. Streamlit Community
> Cloud is the correct (and free) one-click host, made by the Streamlit team.

1. Go to **[share.streamlit.io](https://share.streamlit.io)** and sign in with
   your GitHub account.
2. Click **"Create app"** → **"Deploy a public app from GitHub"**.
3. Select:
   - **Repository:** `<your-username>/kpi-dashboard`
   - **Branch:** `main`
   - **Main file path:** `app.py`
4. Click **"Deploy"**. Streamlit installs `requirements.txt` and launches the
   app — takes 1–2 minutes on first deploy.
5. You'll get a public URL like:
   `https://kpi-dashboard-<random>.streamlit.app`
   Share this with your teacher/class. It auto-updates every time you
   `git push` new changes to `main`.

---

## Using your own data
Replace `data.csv` with your own file, keeping these columns:
`Date, Region, Segment, Revenue, Profit, New_Customers, Total_Customers`
No code changes needed — the dashboard recalculates everything automatically.

## Tech stack
- **Streamlit** — UI framework & app server
- **Pandas** — data loading, filtering, aggregation
- **Plotly Express / Graph Objects** — interactive charts (line, bar, pie, dual-axis)
- **NumPy** — used in `generate_data.py` to synthesize realistic business data
