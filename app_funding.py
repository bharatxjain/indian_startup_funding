import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ---------- Function to Convert USD to INR Crores ----------
def to_inr(dollar):
    inr = dollar * 82.5
    return inr / 10000000

# ---------- Load and Clean Data ----------
def load_data(path=r"C:\Users\dell\Documents\startup_funding.csv"):
    df = pd.read_csv(path)
     # Rename columns for easier access
      # Rename columns for consistency
    df.rename(columns={
        'Date dd/mm/yyyy': 'date',
        'Startup Name': 'startup',
        'Industry Vertical': 'vertical',
        'SubVertical': 'subvertical',
        'City Location': 'city',
        'Investors Name': 'investors',
        'InvestmentnType': 'round',
        'Amount in USD': 'amount_usd'
    }, inplace=True)

    # Parse date column
    df['date'] = pd.to_datetime(df['date'], errors='coerce', dayfirst=True)

    # Clean and convert amount column
    cleaned_amount = []
    for x in df['amount_usd']:
        try:
            amount = float(str(x).replace(',', ''))
        except:
            amount = 0
        cleaned_amount.append(amount)
    df['amount_usd'] = cleaned_amount

    # Convert USD to INR Crores
    df['amount'] = [to_inr(x) for x in df['amount_usd']]

    # Handle missing data
    df.dropna(subset=['date', 'startup'], inplace=True)
    if 'city' not in df.columns:
        df['city'] = 'Unknown'
    df.fillna({'vertical': 'Unknown', 'city': 'Unknown', 'round': 'Unknown'}, inplace=True)

    # Normalize investors column
    df['investors'] = df['investors'].astype(str).str.split(',')
    df = df.explode('investors')  #Add investor in NEW ROW as individual
    df['investors'] = df['investors'].str.strip()
    df.drop_duplicates(inplace=True)

    return df

# ---------- Load Data ----------
df = load_data()

# Configure Streamlit layout
st.set_page_config(layout="wide")
st.title("Indian Startup Funding Analysis")

# Sidebar selection
st.sidebar.title("Startups x Investment")
option = st.sidebar.selectbox("Select", ["Overall", "StartUp", "Investor"])

# ---------- Overall Analysis ----------
if option == "Overall" or option == "":
    if st.sidebar.button("Fetch Details") or option == "Overall":
        st.header("Overall Analysis")
        st.write("This section provides a comprehensive overview of Indian startup funding trends.")

        # Summary Statistics
        st.subheader("Data Summary")
        st.dataframe(df.describe())

        # Top Funded Startups
        st.subheader("Top 10 Funded Startups")
        top_startups = df.groupby('startup')['amount'].sum().sort_values(ascending=False).head(10)
        fig1, ax1 = plt.subplots()
        top_startups.plot(kind='barh', ax=ax1, color='teal')
        ax1.set_xlabel("Funding (₹ Cr)")
        ax1.set_title("Top 10 Funded Startups")
        st.pyplot(fig1)

         # Pie Chart of Top 10 Funded Startups by Funding Share
        st.subheader("Funding Share of Top 10 Startups")
        top_startups = df.groupby('startup')['amount'].sum().sort_values(ascending=False).head(10)
        fig, ax = plt.subplots()
        ax.pie(top_startups, labels=top_startups.index, autopct='%1.1f%%', startangle=140)
        ax.set_title("Funding Distribution Among Top 10 Startups")
        ax.axis('equal')  # Equal aspect ratio ensures pie is drawn as a circle.
        st.pyplot(fig)


        # Funding Trend
        st.subheader("📈 Funding Trend Over Time (Monthly)")
        # Group funding by Month
        monthly_funding = df.groupby(df['date'].dt.to_period('M'))['amount'].sum()
        monthly_funding.index = monthly_funding.index.to_timestamp()  # Convert Period to Timestamp
        # Plotting
        fig2, ax2 = plt.subplots(figsize=(12, 6))
        monthly_funding.plot(ax=ax2, color='darkblue', marker='o', linestyle='-')
        # Enhancements
        ax2.set_ylabel("Funding (₹ Cr)", fontsize=12)
        ax2.set_xlabel("Month-Year", fontsize=12)
        ax2.set_title("Monthly Funding Trend in Indian Startups", fontsize=14, fontweight='bold')
        ax2.grid(True, linestyle='--', alpha=0.5)
        # Rotate x-axis labels
        plt.xticks(rotation=45, ha='right')
        # Add value annotations
        for x, y in zip(monthly_funding.index, monthly_funding.values):
            ax2.annotate(f'{y:.0f}', (x, y), textcoords="offset points", xytext=(0, 5), ha='center', fontsize=8, color='darkgreen')
        # Show plot
        st.pyplot(fig2)

        # Sector Analysis
        st.subheader("Sector-wise Funding")
        sector_totals = df.groupby('vertical')['amount'].sum().sort_values(ascending=False).head(10)
        fig3, ax3 = plt.subplots()
        sector_totals.plot(kind='bar', ax=ax3, color='purple')
        ax3.set_ylabel("Funding (₹ Cr)")
        ax3.set_title("Top 10 Sectors by Total Funding")
        st.pyplot(fig3)

# ---------- Individual Startup Analysis ----------
elif option == "StartUp":
    selected_startup = st.sidebar.selectbox('Select StartUp', sorted(df['startup'].unique().tolist()))
    if st.sidebar.button("Search Details"):
        st.header(f"Startup Analysis: {selected_startup}")

        temp_df = df[df['startup'].str.lower() == selected_startup.lower()]

        st.subheader("Startup Profile")
        st.write(f"**Name:** {selected_startup}")
        st.write(f"**Industry:** {temp_df['vertical'].mode()[0]}")
        if 'city' in temp_df.columns:
            st.write(f"**Location:** {temp_df['city'].mode()[0] if not temp_df['city'].isna().all() else 'Unknown'}")
        st.write(f"**Funding Rounds:** {temp_df.shape[0]}") #fetcing the number of rows in temp_df which are the num of rounds

        # Funding Timeline
        st.subheader("Funding Timeline")
        fig4, ax4 = plt.subplots()
        ax4.plot(temp_df['date'], temp_df['amount'], marker='o', color='green')
        ax4.set_title(f"Funding Timeline for {selected_startup}")
        ax4.set_ylabel("Funding (₹ Cr)")
        st.pyplot(fig4)

        # Funding Table
        st.subheader("Funding Rounds")
        st.dataframe(temp_df[['date', 'investors', 'round', 'amount']])

        # Similar Startups
        st.subheader("Similar Startups")
        same_vertical = df[df['vertical'] == temp_df['vertical'].iloc[0]]
        similar = same_vertical['startup'].drop_duplicates().tolist()
        similar = [s for s in similar if s.lower() != selected_startup.lower()]
        st.write(similar[:10])

# ---------- Individual Investor Analysis ----------
else:
    selected_investor = st.sidebar.selectbox('Select Investor', sorted(df['investors'].dropna().unique().tolist()))
    if st.sidebar.button("Search Details"):
        st.header(f"Investor Analysis: {selected_investor}")

        inv_df = df[df['investors'].str.lower() == selected_investor.lower()]

        if inv_df.empty:
            st.warning("No data available for this investor.")
        else:
            st.subheader("Investor Profile")
            st.write(f"**Name:** {selected_investor}")

            # Most Recent Investment
            recent = inv_df.sort_values(by='date', ascending=False).iloc[0]
            st.write(f"**Recent Investment:** {recent['startup']} on {recent['date'].date()}")

            # Biggest Investment
            top_investment = inv_df.sort_values(by='amount', ascending=False).iloc[0]
            st.write(f"**Biggest Investment:** {top_investment['startup']} - ₹{top_investment['amount']:.2f} Cr")

            # Sector Distribution
            st.subheader("Sector Distribution")
            sector_dist = inv_df['vertical'].value_counts()
            fig5, ax5 = plt.subplots()
            ax5.pie(sector_dist, labels=sector_dist.index, autopct='%1.1f%%')
            ax5.set_title("Sectors Invested In")
            st.pyplot(fig5)

            # Stage Distribution
            st.subheader("Stage Distribution")
            round_dist = inv_df['round'].value_counts()
            fig6, ax6 = plt.subplots()
            ax6.pie(round_dist, labels=round_dist.index, autopct='%1.1f%%')
            ax6.set_title("Investment Rounds")
            st.pyplot(fig6)

            # City Distribution
            st.subheader("City Distribution")
            if 'city' in inv_df.columns:
                city_dist = inv_df['city'].value_counts()
                fig7, ax7 = plt.subplots()
                ax7.pie(city_dist, labels=city_dist.index, autopct='%1.1f%%')
                ax7.set_title("Cities Invested In")
                st.pyplot(fig7)

            # Year-on-Year Funding
            st.subheader("Year-on-Year Investment")
            yoy = inv_df.groupby(inv_df['date'].dt.year)['amount'].sum()
            fig8, ax8 = plt.subplots()
            yoy.plot(kind='bar', ax=ax8, color='orange')
            ax8.set_ylabel("Amount (₹ Cr)")
            ax8.set_title("Yearly Investment")
            st.pyplot(fig8)

            # Similar Investors
            st.subheader("Similar Investors")
            peer_investments = df[df['vertical'].isin(inv_df['vertical'].unique())]
            peers = peer_investments['investors'].dropna().unique().tolist()
            peers = list(set([i for i in peers if selected_investor.lower() not in i.lower()]))
            st.write(peers[:10])

            # Detailed Table
            st.subheader("Detailed Funding")
            st.dataframe(inv_df[['date', 'startup', 'vertical', 'amount', 'round']].sort_values(by='amount', ascending=False))
#footer
st.write("Made with ❤️ BHARAT")