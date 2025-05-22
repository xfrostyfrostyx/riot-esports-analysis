# 🧠 Riot Esports Data Analysis – Scouting & Strategy Tool

This project demonstrates how I use Python, the Riot Games API, and Google Sheets/Tableau to extract, clean, and analyse League of Legends data for strategic preparation in competitive esports.

> 📊 Focus: Data analysis and visualisation for game planning, draft strategy, and opponent scouting in the Oceanic Developmental Tournament (ODT).

---

## 🎯 Objectives

- Understand team and player tendencies using tournament and solo queue data.
- Identify win conditions, champion pools, and weaknesses.
- Support strategic planning and drafting with data insights.

---

## 🔄 Workflow Overview

1. **Data Extraction**  
   Extract match-level data from the Riot API and champion metadata via Data Dragon.

2. **Data Cleaning & Feature Engineering**  
   Process raw data into structured stats such as:
   - KDA, KPAR, FBPAR, CS@10, Gold Share
   - Kill Share, Damage %, Vision Score/M
   - Per-minute metrics (G/M, DMG/M, WARD/M, etc.)

3. **Data Export**  
   Automatically exports cleaned player-level stats into Google Sheets.

4. **Visualisation**  
   Tableau dashboards are used to visualise team trends, player performance, and matchup scenarios.

5. **Insight & Reporting**  
   Based on QDAVI (Question, Data, Analysis, Visualisation, Insight) analysis cycle, insights are derived to support pre-game planning.

---

## 🛠️ Tools & Technologies

- **Python** – `requests`, `pandas`, `numpy`, `matplotlib`, `seaborn`
- **Riot Games API** – Match & participant data extraction
- **Google Sheets API** – `gspread`, `oauth2client` for exporting data
- **Tableau** – Dashboards for coaches/players
- **QDAVI** – A structured data analysis method

---

<pre><code>### 📁 Repository Structure ```text riot-esports-analysis/ ├── data/ │ └── Summary_Tournament_Data.csv # Example of cleaned player-level tournament data │ ├── notebooks/ │ └── riot_data_extraction_cleaning.py # Full script for Riot API data extraction and processing │ ├── docs/ │ └── Story.pdf # Written walkthrough of scouting analysis and insights │ ├── requirements.txt # Python dependencies for running the script └── README.md # Project overview, workflow, and insights ``` </code></pre>

---

## 🧠 Sample Insights

- UQ’s jungler had **78% kill participation** and **56% first blood participation**, suggesting early-game dominance.
- ADC’s solo queue records reveal a heavy preference for **scaling champions** (Zeri, Aphelios), aligning with team comp strategies.
- **Strategic responses** included denying jungle tempo champions and planning early anti-invade setups.

---

## 👨‍💻 Author

**Ka Wai Gary Lai (xFrostyFrostyx)**  
Data Analyst (Esports) | QUT Graduate | Riot API Enthusiast  
🏆 Focused on using structured data to guide strategic decision-making in competitive League of Legends.

---

## 📚 Additional Info

- [📄 Story.pdf](docs/Story.pdf) — Full breakdown of my analysis thought process and strategic insights
- This repo is part of my personal data analyst portfolio. Feedback and questions welcome!

