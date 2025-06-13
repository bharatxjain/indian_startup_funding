<h1>Indian Startup Funding Analysis 🧠📊</h1>
This Streamlit application provides an interactive dashboard for analyzing Indian startup funding trends using data from a startup funding CSV file. The app supports three main types of analysis:
<ol type="A">
    <li>Overall Analysis</li>
    <li>Individual Startup Analysis</li>
    <li>Individual Investor Analysis</li>  
</ol>


<h2>Structure</h2>
<b>startup_funding_analysis:</b>
<ol>
  <li>app_funding.py # Main Streamlit application file</li>
  <li>startup_funding.csv   # Input dataset file (sample)</li>
  <li>README.md             # Project documentation (this file)</li>   
</ol>


<h2>How to Run</h2>
<b>Install Streamlit & Required Libraries</b>
<ol>
  <li>pip install -r requirements.txt</li>
</ol>

<h3>Contents of requirements.txt:</h3>
<ol>
  <li>streamlit</li>
  <li>pandas</li>
  <li>matplotlib</li>
</ol>


<h2>Run the Streamlit App</h2>
streamlit run app_funding.py

<h2>Dataset Location</h2>
<p></p>Ensure the file startup_funding.csv exists at:
https://www.kaggle.com/datasets/sudalairajkumar/indian-startup-funding</p>
<p></p>You can also modify the path in load_data().</p>
