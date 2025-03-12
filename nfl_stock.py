import pandas as pd
import requests
import streamlit as st
import matplotlib.pyplot as plt

# Replace with your actual Sportradar API key
API_KEY = "oEXXprTObqVTRy8SeW2CKB29c5mjt5vxBRpMM4fy"
NFL_BASE_URL = "https://api.sportradar.us/nfl/official/trial/v7/en/games/"

class SportsStockMarket:
    def __init__(self, k=20):
        self.teams = {
            "Minnesota Vikings": 144.0,
            "Washington Commanders": 139.0,
            "Denver Broncos": 136.0,
            "Kansas City Chiefs": 165.0,
            "Pittsburgh Steelers": 150.0,
            "Tampa Bay Buccaneers": 146.0,
            "Detroit Lions": 162.0,
            "Green Bay Packers": 156.0,
            "Los Angeles Chargers": 147.0,
            "Buffalo Bills": 159.0,
            "Chicago Bears": 150.0,
            "Seattle Seahawks": 145.0,
            "Baltimore Ravens": 164.0,
            "Indianapolis Colts": 149.0,
            "Houston Texans": 160.0,
            "Philadelphia Eagles": 161.0,
            "Cincinnati Bengals": 157.0,
            "Arizona Cardinals": 138.0,
            "Tennessee Titans": 143.0,
            "Atlanta Falcons": 148.0,
            "New York Jets": 151.0,
            "San Francisco 49ers": 163.0,
            "Dallas Cowboys": 155.0,
            "Jacksonville Jaguars": 152.0,
            "New York Giants": 141.0,
            "New Orleans Saints": 142.0,
            "New England Patriots": 137.0,
            "Los Angeles Rams": 153.0,
            "Las Vegas Raiders": 140.0,
            "Carolina Panthers": 135.0,
            "Miami Dolphins": 158.0,
            "Cleveland Browns": 154.0
        }
        self.k = k  # Weight constant for ELO calculation

# Simple login system
USERS = {
    "andre": "password123",
    "grace": "securepass",
    "margot": "letmein"
}

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.current_user = None

def login():
    st.sidebar.subheader("🔑 Login")
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")
    if st.sidebar.button("Login"):
        if username in USERS and USERS[username] == password:
            st.session_state.logged_in = True
            st.session_state.current_user = username
            st.sidebar.success(f"Welcome, {username}!")
            st.rerun()
        else:
            st.sidebar.error("Invalid username or password")

def logout():
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.current_user = None
        st.rerun()

if not st.session_state.logged_in:
    login()
    st.stop()
else:
    logout()

# Initialize the Market
market = SportsStockMarket()

# Ensure session state is initialized
if "players" not in st.session_state:
    st.session_state.players = {
        "Andre": {"cash": 10000, "portfolio": {}, "cost_basis": {}},
        "Grace": {"cash": 10000, "portfolio": {}, "cost_basis": {}},
        "Margot": {"cash": 10000, "portfolio": {}, "cost_basis": {}}
    }
if "teams" not in st.session_state:
    st.session_state.teams = market.teams

if "game_log" not in st.session_state:
    st.session_state.game_log = []

# Sidebar Navigation
st.title("🏈 Sports Stock Market Game")
page = st.sidebar.radio("Navigate", ["Home", "Trade", "Portfolio", "Leaderboard", "Game Log"])

if page == "Home":
    st.subheader("📊 Team Stock Prices")
    elo_df = pd.DataFrame(st.session_state.teams.items(), columns=["Team", "ELO Rating"])
    st.dataframe(elo_df.style.format({"ELO Rating": "{:.2f}"}))
    
    if st.button("🔄 Update ELOs with Live Scores"):
        st.session_state.game_log.append("Updated ELOs with latest scores.")
        st.success("ELO Ratings Updated!")
        st.rerun()

elif page == "Trade":
    st.subheader("💰 Buy & Sell Stocks")
    player_name = st.session_state.current_user.capitalize()
    player_data = st.session_state.players[player_name]

    st.write(f"Welcome, {player_name}! Your balance: **${player_data['cash']:.2f}**")

    buy_team = st.selectbox("Select a team to buy", list(market.teams.keys()))
    buy_shares = st.number_input("Enter shares to buy", min_value=0.1, step=0.1)
    if st.button("Buy"):
        price = market.teams[buy_team] * buy_shares
        if player_data["cash"] >= price:
            player_data["cash"] -= price
            player_data["portfolio"][buy_team] = player_data["portfolio"].get(buy_team, 0) + buy_shares
            player_data["cost_basis"][buy_team] = (player_data["cost_basis"].get(buy_team, 0) * (player_data["portfolio"].get(buy_team, 0) - buy_shares) + (price)) / player_data["portfolio"][buy_team]
            st.success(f"{player_name} bought {buy_shares:.2f} shares of {buy_team} at {market.teams[buy_team]:.2f} each.")
        else:
            st.error("Insufficient funds.")

