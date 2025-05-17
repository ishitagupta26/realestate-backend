Real Estate Data Chatbot with Visualization (Django + React)

This is an intelligent real estate data analysis chatbot built using Django (backend) and React (frontend). It allows users to ask smart, human-like questions related to real estate data and receive:
- Interactive charts
- Summary insights powered by an LLM (OpenRouter API)
- Full data tables with optional CSV download

-->Features

 1. Natural Language Chat Interface
- Users can type any query about real estate areas, prices, or demand.
- The system parses the query, applies filters, and returns relevant visual data and summary.

 2. Real-Time Summary using OpenRouter API
- Integrated with `mistralai/mistral-7b-instruct` via OpenRouter API.
- Generates a brief, intelligent summary based on filtered data.

 3. Dynamic Chart Visualization (Recharts + React)
- Displays time-series line charts comparing demand or prices over years.
- Automatically adjusts color and keys based on queried areas.

4. Interactive Table View
- Shows full filtered dataset in a responsive, scrollable table.
- Uses clean formatting and scrollable horizontal view for wide datasets.

 5. Export Data to CSV
- 📥 One-click Download CSV of the full filtered dataset for external use or records.

 6. Hardcoded API Key (for smooth local use)
- Skips `.env`/`.gitignore` complexity.
- Useful for hackathons, demos, or non-hosted submission use.

 7. Multi-Area Comparison Logic
- If user types “compare Wakad and Hinjewadi demand in last 5 years”, the system:
  - Detects both areas
  - Aggregates demand
  - Builds a combined chart
  - Calls LLM for summary

-->Tech Stack

Backend     :-  Django (REST API)         
AI Summary  :-  OpenRouter (Mistral LLM)  
Frontend    :-  React + Recharts          
Styling     :-  CSS + FontAwesome Icons   
File I/O    :-  Pandas, OpenPyXL          
Export      :-  Blob + anchor-based CSV   

-->Example Queries

You can ask:
Show demand trend in Wakad
Compare price between Baner and Kothrud
What was the demand in Hinjewadi in the last 5 years?
Flat rate trend in Wakad
Compare demand in Baner vs Wakad

How to Run Locally

1. Clone the repo
git clone https://github.com/ishitagupta26/realestate-backend.git
cd realestate-backend

2. Create & activate virtual env
   python -m venv .venv
.venv\Scripts\activate   # Windows

3.Install dependencies
pip install -r requirements.txt

4.Run server
python manage.py runserver

5.Run frontend
cd frontend
npm install
npm start

6.Go to: http://localhost:3000 and try a query like:
“Compare Wakad and Hinjewadi demand in last 3 years”
