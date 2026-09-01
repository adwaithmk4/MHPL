import streamlit as st
import pandas as pd
import json
import os
import random

# Set up page config
st.set_page_config(
    page_title="MHPL Cricket Auction",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom IPL-Style CSS Styling (Gold & Dark Blue Theme)
st.markdown("""
<style>
    /* Main layout and background */
    .stApp {
        background-color: #0d1b2a;
        color: #e0e1dd;
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: #1b263b;
        border-right: 3px solid #e0a96d;
    }
    
    /* Custom Headers */
    h1, h2, h3 {
        color: #e0a96d !important;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        font-weight: 800;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
    }
    
    /* Card design for Player Card */
    .player-card {
        background: linear-gradient(135deg, #1b263b 0%, #0d1b2a 100%);
        border: 2px solid #e0a96d;
        border-radius: 15px;
        padding: 25px;
        box-shadow: 0 8px 16px rgba(0,0,0,0.6);
        color: #ffffff;
        margin-bottom: 20px;
    }
    
    .player-name {
        font-size: 2.2rem;
        font-weight: 900;
        color: #e0a96d;
        text-transform: uppercase;
        margin-bottom: 5px;
        border-bottom: 2px solid #e0a96d;
        padding-bottom: 10px;
    }
    
    .player-role {
        font-size: 1.2rem;
        background-color: #e0a96d;
        color: #0d1b2a;
        padding: 3px 15px;
        border-radius: 20px;
        font-weight: 700;
        display: inline-block;
        margin-bottom: 15px;
        text-transform: uppercase;
    }
    
    .player-stat {
        font-size: 1.1rem;
        margin-bottom: 8px;
    }
    
    .player-stat strong {
        color: #e0a96d;
    }
    
    .remarks-box {
        background-color: rgba(224, 169, 109, 0.15);
        border-left: 5px solid #e0a96d;
        padding: 10px 15px;
        margin-top: 15px;
        border-radius: 0 10px 10px 0;
        font-style: italic;
    }
    
    /* Buttons */
    .stButton>button {
        background-color: #e0a96d;
        color: #0d1b2a;
        font-weight: bold;
        border: none;
        border-radius: 5px;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        background-color: #ffffff;
        color: #0d1b2a;
        box-shadow: 0 0 10px #e0a96d;
        transform: translateY(-2px);
    }
    
    /* Metrics */
    div[data-testid="metric-container"] {
        background-color: #1b263b;
        border: 1px solid #415a77;
        border-radius: 10px;
        padding: 10px 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    
    div[data-testid="stMetricLabel"] {
        color: #e0a96d !important;
        font-weight: bold;
        text-transform: uppercase;
    }
    
    /* Custom table formatting */
    .styled-table {
        width: 100%;
        border-collapse: collapse;
        margin: 25px 0;
        font-size: 0.9em;
        font-family: sans-serif;
        box-shadow: 0 0 20px rgba(0, 0, 0, 0.15);
    }
    
</style>
""", unsafe_allow_html=True)

# ----------------------------------------
# 1. EM-BEDDED PLAYER DATA FALLBACK
# ----------------------------------------
# This placeholder will be replaced with the JSON representation of the cleaned player list during generation.
EMBEDDED_PLAYERS = [
    {
        "id": "PL_001",
        "name": "G Vamsi",
        "role": "All-rounder",
        "department": "Ir",
        "reg_num": "2501305019",
        "course": "International relations and politics",
        "wicket_keeper": "No",
        "batting_style": "Right",
        "bowling_hand": "Right",
        "bowling_style": "Fast",
        "photo_url": "https://drive.google.com/open?id=1GAHV3CtBEvm8KnC5PO6V47EfNDo4hvi2",
        "photo_direct": "https://lh3.googleusercontent.com/u/0/d/1GAHV3CtBEvm8KnC5PO6V47EfNDo4hvi2",
        "remarks": "Nothing"
    },
    {
        "id": "PL_002",
        "name": "Adhithyan kp",
        "role": "Batter",
        "department": "M. Com",
        "reg_num": "2602505001",
        "course": "International business",
        "wicket_keeper": "No",
        "batting_style": "Left",
        "bowling_hand": None,
        "bowling_style": None,
        "photo_url": "https://drive.google.com/open?id=1o-f24aKEpTdFvE20kLnfcrSIZCvMxCSG",
        "photo_direct": "https://lh3.googleusercontent.com/u/0/d/1o-f24aKEpTdFvE20kLnfcrSIZCvMxCSG",
        "remarks": None
    },
    {
        "id": "PL_003",
        "name": "Davis Titus",
        "role": "All-rounder",
        "department": "Public Administration",
        "reg_num": "2302007006",
        "course": "Phd",
        "wicket_keeper": "No",
        "batting_style": "Right",
        "bowling_hand": "Right",
        "bowling_style": "Off Spin",
        "photo_url": "https://drive.google.com/open?id=1LQvfed8_N37ZMT5u7ZUA3w-cKG4EVIpM",
        "photo_direct": "https://lh3.googleusercontent.com/u/0/d/1LQvfed8_N37ZMT5u7ZUA3w-cKG4EVIpM",
        "remarks": None
    },
    {
        "id": "PL_004",
        "name": "Farith",
        "role": "All-rounder",
        "department": "IR",
        "reg_num": "9626560501",
        "course": "International relations and political science",
        "wicket_keeper": "No",
        "batting_style": "Right",
        "bowling_hand": "Right",
        "bowling_style": "Leg Spin",
        "photo_url": "https://drive.google.com/open?id=1oQnEcqoUbQMVRgNhrEIE6Zgq6VBSAbz_",
        "photo_direct": "https://lh3.googleusercontent.com/u/0/d/1oQnEcqoUbQMVRgNhrEIE6Zgq6VBSAbz_",
        "remarks": "\ud83d\ude4f\ud83c\udffb"
    },
    {
        "id": "PL_005",
        "name": "Mahesh",
        "role": "All-rounder",
        "department": "SOCIAL WORK",
        "reg_num": "2601505039",
        "course": "MSW",
        "wicket_keeper": "No",
        "batting_style": "Right",
        "bowling_hand": "Right",
        "bowling_style": "Medium Fast",
        "photo_url": "https://drive.google.com/open?id=1vOZh-63GTE-Q1IyzaSVerb7k7qf-5MbI",
        "photo_direct": "https://lh3.googleusercontent.com/u/0/d/1vOZh-63GTE-Q1IyzaSVerb7k7qf-5MbI",
        "remarks": None
    },
    {
        "id": "PL_006",
        "name": "PALLI YASWANTH",
        "role": "All-rounder",
        "department": "Computer",
        "reg_num": "2600704154",
        "course": "Bsc Data Science and AI",
        "wicket_keeper": "No",
        "batting_style": "Right",
        "bowling_hand": "Right",
        "bowling_style": "Fast",
        "photo_url": "https://drive.google.com/open?id=1lkyNudYKR8YL2IexMLXde0k2sFGEqtcr",
        "photo_direct": "https://lh3.googleusercontent.com/u/0/d/1lkyNudYKR8YL2IexMLXde0k2sFGEqtcr",
        "remarks": None
    },
    {
        "id": "PL_007",
        "name": "Egiti Bala venkateswarlu",
        "role": "Bowler",
        "department": "Tourism studies",
        "reg_num": "2502605041",
        "course": "MBA TTM",
        "wicket_keeper": "No",
        "batting_style": "Right",
        "bowling_hand": "Right",
        "bowling_style": "Fast",
        "photo_url": "https://drive.google.com/open?id=1Y8pnNICY7fLuuVNa1NF2UdjnU1jBtNQy",
        "photo_direct": "https://lh3.googleusercontent.com/u/0/d/1Y8pnNICY7fLuuVNa1NF2UdjnU1jBtNQy",
        "remarks": None
    },
    {
        "id": "PL_008",
        "name": "Adhithyan kp",
        "role": "Batter",
        "department": "M. Com",
        "reg_num": "2602505001",
        "course": "International business",
        "wicket_keeper": "No",
        "batting_style": "Right",
        "bowling_hand": None,
        "bowling_style": None,
        "photo_url": "https://drive.google.com/open?id=1_SamMBMAhhG_LxTk0KiGC1k8itFJ77zb",
        "photo_direct": "https://lh3.googleusercontent.com/u/0/d/1_SamMBMAhhG_LxTk0KiGC1k8itFJ77zb",
        "remarks": "Nop"
    },
    {
        "id": "PL_009",
        "name": "Abhinav S",
        "role": "Bowler",
        "department": "PLS",
        "reg_num": "2601005002",
        "course": "MSc Botany",
        "wicket_keeper": "No",
        "batting_style": "Right",
        "bowling_hand": "Right",
        "bowling_style": "Medium Fast",
        "photo_url": "https://drive.google.com/open?id=1W50SUN4CgetVkSt5CFz1vypArgcNIotB",
        "photo_direct": "https://lh3.googleusercontent.com/u/0/d/1W50SUN4CgetVkSt5CFz1vypArgcNIotB",
        "remarks": None
    },
    {
        "id": "PL_010",
        "name": "Amal Babu K",
        "role": "Bowler",
        "department": "DCIB",
        "reg_num": "2502507001",
        "course": "PhD",
        "wicket_keeper": "No",
        "batting_style": "Left",
        "bowling_hand": "Right",
        "bowling_style": "Medium Fast",
        "photo_url": "https://drive.google.com/open?id=1Bv9P9psTnpXeZ1I775LBjneUZxPiN88_",
        "photo_direct": "https://lh3.googleusercontent.com/u/0/d/1Bv9P9psTnpXeZ1I775LBjneUZxPiN88_",
        "remarks": None
    },
    {
        "id": "PL_011",
        "name": "Yogesh Kumar Nial",
        "role": "All-rounder",
        "department": "ITEP",
        "reg_num": "2501604019",
        "course": "ITEP Physics",
        "wicket_keeper": "No",
        "batting_style": "Right",
        "bowling_hand": "Right",
        "bowling_style": "Medium Fast",
        "photo_url": "https://drive.google.com/open?id=15u3PtY9aNQwxFILIcrcu8PQrwfakLYD0",
        "photo_direct": "https://lh3.googleusercontent.com/u/0/d/15u3PtY9aNQwxFILIcrcu8PQrwfakLYD0",
        "remarks": None
    },
    {
        "id": "PL_012",
        "name": "Sandeep Nayak",
        "role": "Batter",
        "department": "ITEP",
        "reg_num": "2401604219",
        "course": "Economics",
        "wicket_keeper": "No",
        "batting_style": "Right",
        "bowling_hand": None,
        "bowling_style": None,
        "photo_url": "https://drive.google.com/open?id=1zLi3fNF2HkYGldfP-J1jU9hxD2bAjy3G",
        "photo_direct": "https://lh3.googleusercontent.com/u/0/d/1zLi3fNF2HkYGldfP-J1jU9hxD2bAjy3G",
        "remarks": "No"
    },
    {
        "id": "PL_013",
        "name": "Govinda Naik",
        "role": "Batter",
        "department": "Economics",
        "reg_num": "2600205016",
        "course": "Post Graduation",
        "wicket_keeper": "No",
        "batting_style": "Right",
        "bowling_hand": None,
        "bowling_style": None,
        "photo_url": "https://drive.google.com/open?id=15aXINThkg6hvL1RRppTxtC-yAd948sT1",
        "photo_direct": "https://lh3.googleusercontent.com/u/0/d/15aXINThkg6hvL1RRppTxtC-yAd948sT1",
        "remarks": "No"
    },
    {
        "id": "PL_014",
        "name": "ANoneDU R NATH",
        "role": "Batter",
        "department": "COMPUTER SCIENCE",
        "reg_num": "2600704107",
        "course": "B. Sc. (Hons.) Data Science and Artificial Intelligence",
        "wicket_keeper": "Yes",
        "batting_style": "Right",
        "bowling_hand": None,
        "bowling_style": None,
        "photo_url": "https://drive.google.com/open?id=15Nib1yTW5dnC6L44UDXU5gFPsY47w2Fh",
        "photo_direct": "https://lh3.googleusercontent.com/u/0/d/15Nib1yTW5dnC6L44UDXU5gFPsY47w2Fh",
        "remarks": None
    },
    {
        "id": "PL_015",
        "name": "PAKA BHARATH KUMAR",
        "role": "All-rounder",
        "department": "Business studies & management",
        "reg_num": "2602504062",
        "course": "B.com hons",
        "wicket_keeper": "No",
        "batting_style": "Right",
        "bowling_hand": "Right",
        "bowling_style": "Off Spin",
        "photo_url": "https://drive.google.com/open?id=1EOl2vcnO5TheKkHngHkfePHi82z4OZDq",
        "photo_direct": "https://lh3.googleusercontent.com/u/0/d/1EOl2vcnO5TheKkHngHkfePHi82z4OZDq",
        "remarks": "NO"
    },
    {
        "id": "PL_016",
        "name": "BAYAJI PUALA",
        "role": "Batter",
        "department": "Education",
        "reg_num": "2601605003",
        "course": "M.ed",
        "wicket_keeper": "Yes",
        "batting_style": "Right",
        "bowling_hand": None,
        "bowling_style": None,
        "photo_url": "https://drive.google.com/open?id=1jLYuOC_GbosgB5s4rhXRU4U_pK0_Ct1Z",
        "photo_direct": "https://lh3.googleusercontent.com/u/0/d/1jLYuOC_GbosgB5s4rhXRU4U_pK0_Ct1Z",
        "remarks": "No"
    },
    {
        "id": "PL_017",
        "name": "Mohamed Asmar M I",
        "role": "All-rounder",
        "department": "Commerce and International Business",
        "reg_num": "2502504016",
        "course": "B. Com(Hons) FiNonecial analytics (2nd year)",
        "wicket_keeper": "No",
        "batting_style": "Left",
        "bowling_hand": "Right",
        "bowling_style": "Medium Fast",
        "photo_url": "https://drive.google.com/open?id=1sLCUjCZZiSOEED0qPj0UJ51w8qA_PINW",
        "photo_direct": "https://lh3.googleusercontent.com/u/0/d/1sLCUjCZZiSOEED0qPj0UJ51w8qA_PINW",
        "remarks": "Left-hand batsman and right-arm medium-fast bowler.Participated in inter school tournament and mhpl."
    },
    {
        "id": "PL_018",
        "name": "Santo Sali",
        "role": "All-rounder",
        "department": "Mathematics",
        "reg_num": "2300907001",
        "course": "PhD",
        "wicket_keeper": "No",
        "batting_style": "Right",
        "bowling_hand": "Right",
        "bowling_style": "Fast",
        "photo_url": "https://drive.google.com/open?id=1nL-QNEQ0jaUQ75JOVcWhtVZzuSfwmKBP",
        "photo_direct": "https://lh3.googleusercontent.com/u/0/d/1nL-QNEQ0jaUQ75JOVcWhtVZzuSfwmKBP",
        "remarks": None
    },
    {
        "id": "PL_019",
        "name": "ROMIT MANKARA",
        "role": "All-rounder",
        "department": "COMPUTER SCIENCE",
        "reg_num": "2600704139",
        "course": "BSC DATA SCIENCE AND AI",
        "wicket_keeper": "No",
        "batting_style": "Right",
        "bowling_hand": "Right",
        "bowling_style": "Medium Fast",
        "photo_url": "https://drive.google.com/open?id=1O7FWNaUwcB0THiepmhCs1vk77Gvw61kJ",
        "photo_direct": "https://lh3.googleusercontent.com/u/0/d/1O7FWNaUwcB0THiepmhCs1vk77Gvw61kJ",
        "remarks": None
    },
    {
        "id": "PL_020",
        "name": "Modhugu Shyam",
        "role": "All-rounder",
        "department": "Business studies&management",
        "reg_num": "2502504038",
        "course": "B.com hons",
        "wicket_keeper": "No",
        "batting_style": "Right",
        "bowling_hand": "Right",
        "bowling_style": "Medium Fast",
        "photo_url": "https://drive.google.com/open?id=1WQfSzbbZiScu0tnsgcWQYxxJHv0eSuk8",
        "photo_direct": "https://lh3.googleusercontent.com/u/0/d/1WQfSzbbZiScu0tnsgcWQYxxJHv0eSuk8",
        "remarks": "No"
    },
    {
        "id": "PL_021",
        "name": "Subrata Mondal",
        "role": "All-rounder",
        "department": "MPH",
        "reg_num": "2601905027",
        "course": "Master of public health",
        "wicket_keeper": "No",
        "batting_style": "Right",
        "bowling_hand": "Right",
        "bowling_style": "Medium Fast",
        "photo_url": "https://drive.google.com/open?id=1ew44B7u1yKP-GRFujxED6rS5OcrZ6ub4",
        "photo_direct": "https://lh3.googleusercontent.com/u/0/d/1ew44B7u1yKP-GRFujxED6rS5OcrZ6ub4",
        "remarks": None
    },
    {
        "id": "PL_022",
        "name": "AILENI SAIRAHUL",
        "role": "All-rounder",
        "department": "MA ECONOMICS",
        "reg_num": "2600205002",
        "course": "MA ECONOMICS",
        "wicket_keeper": "No",
        "batting_style": "Right",
        "bowling_hand": "Right",
        "bowling_style": "Medium Fast",
        "photo_url": "https://drive.google.com/open?id=1lgqfHyUYJwHEpIOCTBuFgZ-1eaTYptKv",
        "photo_direct": "https://lh3.googleusercontent.com/u/0/d/1lgqfHyUYJwHEpIOCTBuFgZ-1eaTYptKv",
        "remarks": "No"
    },
    {
        "id": "PL_023",
        "name": "Arshlaan khan",
        "role": "Batter",
        "department": "ITEP",
        "reg_num": "2501604439",
        "course": "B.Com B.Ed",
        "wicket_keeper": "No",
        "batting_style": "Right",
        "bowling_hand": None,
        "bowling_style": None,
        "photo_url": "https://drive.google.com/open?id=1lsKvqv6FYE0Fn3a2_qZaq3Nz4cSR3US9",
        "photo_direct": "https://lh3.googleusercontent.com/u/0/d/1lsKvqv6FYE0Fn3a2_qZaq3Nz4cSR3US9",
        "remarks": None
    },
    {
        "id": "PL_024",
        "name": "Sharanabasava",
        "role": "All-rounder",
        "department": "Department of Public Health Sciences",
        "reg_num": "2601905035",
        "course": "Master's in Public Health",
        "wicket_keeper": "No",
        "batting_style": "Right",
        "bowling_hand": "Right",
        "bowling_style": "Leg Spin",
        "photo_url": "https://drive.google.com/open?id=1oGQkiiMEWGAueosxfgRxxDdAcIeFc6KY",
        "photo_direct": "https://lh3.googleusercontent.com/u/0/d/1oGQkiiMEWGAueosxfgRxxDdAcIeFc6KY",
        "remarks": "Nothing"
    },
    {
        "id": "PL_025",
        "name": "Arjun Sreekumar",
        "role": "All-rounder",
        "department": "ITEP",
        "reg_num": "2401604411",
        "course": "Itep",
        "wicket_keeper": "No",
        "batting_style": "Right",
        "bowling_hand": "Right",
        "bowling_style": "Medium Fast",
        "photo_url": "https://drive.google.com/open?id=1zsfDQSOGlY2lCNXAfecwYMiuiroTCLGZ",
        "photo_direct": "https://lh3.googleusercontent.com/u/0/d/1zsfDQSOGlY2lCNXAfecwYMiuiroTCLGZ",
        "remarks": None
    },
    {
        "id": "PL_026",
        "name": "ABHINAV K P",
        "role": "All-rounder",
        "department": "DCIB",
        "reg_num": "2302507009",
        "course": "PhD",
        "wicket_keeper": "No",
        "batting_style": "Right",
        "bowling_hand": "Right",
        "bowling_style": "Fast",
        "photo_url": "https://drive.google.com/open?id=1GPw6_5W0YB2SN1hYxEhqXLAxpgterCep",
        "photo_direct": "https://lh3.googleusercontent.com/u/0/d/1GPw6_5W0YB2SN1hYxEhqXLAxpgterCep",
        "remarks": None
    },
    {
        "id": "PL_027",
        "name": "AbhiNoneth S Kumar",
        "role": "All-rounder",
        "department": "Public administration and policy studies",
        "reg_num": "2602005001",
        "course": "MA Public Administration and Policy studies",
        "wicket_keeper": "No",
        "batting_style": "Right",
        "bowling_hand": "Right",
        "bowling_style": "Medium Fast",
        "photo_url": "https://drive.google.com/open?id=1yE_0giM_rci8IjiH11eOR5TNzHKI2xpE",
        "photo_direct": "https://lh3.googleusercontent.com/u/0/d/1yE_0giM_rci8IjiH11eOR5TNzHKI2xpE",
        "remarks": None
    },
    {
        "id": "PL_028",
        "name": "Bablu Chhura",
        "role": "Batter",
        "department": "Education",
        "reg_num": "2401604207",
        "course": "ITEP Economics",
        "wicket_keeper": "Yes",
        "batting_style": "Right",
        "bowling_hand": None,
        "bowling_style": None,
        "photo_url": "https://drive.google.com/open?id=1kg4gXuhK5ODOb_aXq2UcDWU0CgGyh93p",
        "photo_direct": "https://lh3.googleusercontent.com/u/0/d/1kg4gXuhK5ODOb_aXq2UcDWU0CgGyh93p",
        "remarks": None
    },
    {
        "id": "PL_029",
        "name": "Ashwin venugopal",
        "role": "All-rounder",
        "department": "Tourism Studies",
        "reg_num": "2502605008",
        "course": "MBATTM",
        "wicket_keeper": "No",
        "batting_style": "Right",
        "bowling_hand": "Left",
        "bowling_style": "Medium Fast",
        "photo_url": "https://drive.google.com/open?id=1S5isodPGb1Q_W0gp9uLVcarM5ldeKvNG",
        "photo_direct": "https://lh3.googleusercontent.com/u/0/d/1S5isodPGb1Q_W0gp9uLVcarM5ldeKvNG",
        "remarks": "Played south zone"
    },
    {
        "id": "PL_030",
        "name": "Ashutosh Pandey",
        "role": "All-rounder",
        "department": "Economics",
        "reg_num": "2600145005",
        "course": "PhD",
        "wicket_keeper": "No",
        "batting_style": "Right",
        "bowling_hand": "Right",
        "bowling_style": "Medium Fast",
        "photo_url": "https://drive.google.com/open?id=1Qb_2LKRDBiAA308bWEL4qBr1V3l-smrA",
        "photo_direct": "https://lh3.googleusercontent.com/u/0/d/1Qb_2LKRDBiAA308bWEL4qBr1V3l-smrA",
        "remarks": None
    },
    {
        "id": "PL_031",
        "name": "Jagabandhu Behera",
        "role": "All-rounder",
        "department": "ITEP",
        "reg_num": "2601604007",
        "course": "Physics",
        "wicket_keeper": "No",
        "batting_style": "Right",
        "bowling_hand": "Right",
        "bowling_style": "Medium Fast",
        "photo_url": "https://drive.google.com/open?id=1sUInoJcz7XMw19NOJ_zmNSTncMQtZdpu",
        "photo_direct": "https://lh3.googleusercontent.com/u/0/d/1sUInoJcz7XMw19NOJ_zmNSTncMQtZdpu",
        "remarks": None
    },
    {
        "id": "PL_032",
        "name": "Thejas kanNone",
        "role": "All-rounder",
        "department": "Dept of Genomic Science",
        "reg_num": "2500505019",
        "course": "MSc Genomic Science",
        "wicket_keeper": "No",
        "batting_style": "Right",
        "bowling_hand": "Left",
        "bowling_style": "Leg Spin",
        "photo_url": "https://drive.google.com/open?id=14FjcilC7v0ShsjQi9ptuSkytrJoTD_yJ",
        "photo_direct": "https://lh3.googleusercontent.com/u/0/d/14FjcilC7v0ShsjQi9ptuSkytrJoTD_yJ",
        "remarks": None
    },
    {
        "id": "PL_033",
        "name": "B.Shoban Babu",
        "role": "Batter",
        "department": "Tourism",
        "reg_num": "2502605033",
        "course": "MBA TTM",
        "wicket_keeper": "Yes",
        "batting_style": "Right",
        "bowling_hand": None,
        "bowling_style": None,
        "photo_url": "https://drive.google.com/open?id=1Md2uYKh4SUwzAus-GmzMexK-9CzW-u8S",
        "photo_direct": "https://lh3.googleusercontent.com/u/0/d/1Md2uYKh4SUwzAus-GmzMexK-9CzW-u8S",
        "remarks": None
    },
    {
        "id": "PL_034",
        "name": "Abhishek kj",
        "role": "Bowler",
        "department": "Genomic science",
        "reg_num": "2500505022",
        "course": "Msc Genomic science",
        "wicket_keeper": "No",
        "batting_style": "Left",
        "bowling_hand": "Right",
        "bowling_style": "Medium Fast",
        "photo_url": "https://drive.google.com/open?id=1V2zJZSoCOL6SIRjO2yl8eQn1RapcoYm3",
        "photo_direct": "https://lh3.googleusercontent.com/u/0/d/1V2zJZSoCOL6SIRjO2yl8eQn1RapcoYm3",
        "remarks": None
    },
    {
        "id": "PL_035",
        "name": "Ravendra Yadav",
        "role": "Batter",
        "department": "Bsc Physics",
        "reg_num": "2600604027",
        "course": "Bsc Physics Semiconductor",
        "wicket_keeper": "No",
        "batting_style": "Right",
        "bowling_hand": None,
        "bowling_style": None,
        "photo_url": "https://drive.google.com/open?id=1thoVqb7kg2zFCp_AAozazPoLlkIWf7sG",
        "photo_direct": "https://lh3.googleusercontent.com/u/0/d/1thoVqb7kg2zFCp_AAozazPoLlkIWf7sG",
        "remarks": None
    },
    {
        "id": "PL_036",
        "name": "Pruthiraj sethi",
        "role": "All-rounder",
        "department": "Itep physics",
        "reg_num": "2601604024",
        "course": "Physics",
        "wicket_keeper": "No",
        "batting_style": "Right",
        "bowling_hand": "Right",
        "bowling_style": "Medium Fast",
        "photo_url": "https://drive.google.com/open?id=1I3n-kf1HAmWGoy6JbrzQreZhOopkf4fL",
        "photo_direct": "https://lh3.googleusercontent.com/u/0/d/1I3n-kf1HAmWGoy6JbrzQreZhOopkf4fL",
        "remarks": None
    },
    {
        "id": "PL_037",
        "name": "Adwaith M K",
        "role": "Bowler",
        "department": "Computer Science",
        "reg_num": "2500705017",
        "course": "2nd MSC CS",
        "wicket_keeper": "No",
        "batting_style": "Right",
        "bowling_hand": "Right",
        "bowling_style": "Off Spin",
        "photo_url": "https://drive.google.com/open?id=1R2kez6SUOTIj4EMzZtdMYXdem2sWFksh",
        "photo_direct": "https://lh3.googleusercontent.com/u/0/d/1R2kez6SUOTIj4EMzZtdMYXdem2sWFksh",
        "remarks": None
    },
    {
        "id": "PL_038",
        "name": "Adithyan v p",
        "role": "Batter",
        "department": "Computer science",
        "reg_num": "2500704002",
        "course": "BCA",
        "wicket_keeper": "No",
        "batting_style": "Right",
        "bowling_hand": None,
        "bowling_style": None,
        "photo_url": "https://drive.google.com/open?id=1IiUqZJoRcQMYiQC5BNJWlLp2YklxyXhl",
        "photo_direct": "https://lh3.googleusercontent.com/u/0/d/1IiUqZJoRcQMYiQC5BNJWlLp2YklxyXhl",
        "remarks": "No.."
    },
    {
        "id": "PL_039",
        "name": "ALAN",
        "role": "Batter",
        "department": "Computer Science",
        "reg_num": "2500704003",
        "course": "BCA",
        "wicket_keeper": "Yes",
        "batting_style": "Right",
        "bowling_hand": None,
        "bowling_style": None,
        "photo_url": "https://drive.google.com/open?id=1EMMKCT_e-IF_WsCyX69zuZHy0shGjyca",
        "photo_direct": "https://lh3.googleusercontent.com/u/0/d/1EMMKCT_e-IF_WsCyX69zuZHy0shGjyca",
        "remarks": None
    },
    {
        "id": "PL_040",
        "name": "Prewthiraj P",
        "role": "All-rounder",
        "department": "Yoga",
        "reg_num": "2502205014",
        "course": "Msc yoga therappy",
        "wicket_keeper": "No",
        "batting_style": "Right",
        "bowling_hand": "Right",
        "bowling_style": "Fast",
        "photo_url": "https://drive.google.com/open?id=1KBCBPvmo74gr0qYqNfcxxqeC3eVCxsgx",
        "photo_direct": "https://lh3.googleusercontent.com/u/0/d/1KBCBPvmo74gr0qYqNfcxxqeC3eVCxsgx",
        "remarks": "Black mole in right hand"
    },
    {
        "id": "PL_041",
        "name": "Md Nasir Ali",
        "role": "All-rounder",
        "department": "Biological sciences",
        "reg_num": "2600505039",
        "course": "M.Sc Genomic science",
        "wicket_keeper": "No",
        "batting_style": "Right",
        "bowling_hand": "Right",
        "bowling_style": "Medium Fast",
        "photo_url": "https://drive.google.com/open?id=10UAGBNP7R4eMW7D_SYRnwyY47pOJWun-",
        "photo_direct": "https://lh3.googleusercontent.com/u/0/d/10UAGBNP7R4eMW7D_SYRnwyY47pOJWun-",
        "remarks": None
    },
    {
        "id": "PL_042",
        "name": "Alan S Abraham",
        "role": "All-rounder",
        "department": "Social Work",
        "reg_num": "2601505002",
        "course": "MSW",
        "wicket_keeper": "No",
        "batting_style": "Right",
        "bowling_hand": "Right",
        "bowling_style": "Medium Fast",
        "photo_url": "https://drive.google.com/open?id=1pUv2AkbWlncJLF8lC48UzWYO28726kXb",
        "photo_direct": "https://lh3.googleusercontent.com/u/0/d/1pUv2AkbWlncJLF8lC48UzWYO28726kXb",
        "remarks": None
    },
    {
        "id": "PL_043",
        "name": "Aswin Dev",
        "role": "All-rounder",
        "department": "Yoga",
        "reg_num": "2502205012",
        "course": "MSC Yoga Therapy",
        "wicket_keeper": "No",
        "batting_style": "Right",
        "bowling_hand": "Right",
        "bowling_style": "Leg Spin",
        "photo_url": "https://drive.google.com/open?id=1c6OqIMHiGGrR-ywXAqoIyclwBWXsun7d",
        "photo_direct": "https://lh3.googleusercontent.com/u/0/d/1c6OqIMHiGGrR-ywXAqoIyclwBWXsun7d",
        "remarks": "No"
    },
    {
        "id": "PL_044",
        "name": "G. Dinesh",
        "role": "All-rounder",
        "department": "IR",
        "reg_num": "2501305005",
        "course": "IR",
        "wicket_keeper": "No",
        "batting_style": "Right",
        "bowling_hand": "Right",
        "bowling_style": "Medium Fast",
        "photo_url": "https://drive.google.com/open?id=1oX68JCqPzW-kaTqzdXGvUMIeaXQEJ1xJ",
        "photo_direct": "https://lh3.googleusercontent.com/u/0/d/1oX68JCqPzW-kaTqzdXGvUMIeaXQEJ1xJ",
        "remarks": None
    },
    {
        "id": "PL_045",
        "name": "Muhammad Shibli V",
        "role": "Batter",
        "department": "Computer science",
        "reg_num": "2600704018",
        "course": "BCA",
        "wicket_keeper": "Yes",
        "batting_style": "Right",
        "bowling_hand": None,
        "bowling_style": None,
        "photo_url": "https://drive.google.com/open?id=1nea7dpQU2UJRTrHsben3VzLBWzLVuoYx",
        "photo_direct": "https://lh3.googleusercontent.com/u/0/d/1nea7dpQU2UJRTrHsben3VzLBWzLVuoYx",
        "remarks": None
    },
    {
        "id": "PL_046",
        "name": "Siva Praveen SR",
        "role": "All-rounder",
        "department": "MSC Microbiology",
        "reg_num": "2602805026",
        "course": "Microbiology",
        "wicket_keeper": "No",
        "batting_style": "Right",
        "bowling_hand": "Right",
        "bowling_style": "Medium Fast",
        "photo_url": "https://drive.google.com/open?id=1kZfj3A_RlmI59avigKbVohncDWtLgabo",
        "photo_direct": "https://lh3.googleusercontent.com/u/0/d/1kZfj3A_RlmI59avigKbVohncDWtLgabo",
        "remarks": None
    },
    {
        "id": "PL_047",
        "name": "Siddharth Sanjay",
        "role": "Bowler",
        "department": "Genomic Science",
        "reg_num": "2600505021",
        "course": "MSc",
        "wicket_keeper": "No",
        "batting_style": "Right",
        "bowling_hand": "Right",
        "bowling_style": "Off Spin",
        "photo_url": "https://drive.google.com/open?id=1gQdgYeKkbyCio838RSAjkHPmDQFhAIgb",
        "photo_direct": "https://lh3.googleusercontent.com/u/0/d/1gQdgYeKkbyCio838RSAjkHPmDQFhAIgb",
        "remarks": None
    },
    {
        "id": "PL_048",
        "name": "Dhirendra",
        "role": "All-rounder",
        "department": "ENGLISH",
        "reg_num": "2600105015",
        "course": "MA English and Comparative Literature",
        "wicket_keeper": "No",
        "batting_style": "Left",
        "bowling_hand": "Right",
        "bowling_style": "Fast",
        "photo_url": "https://drive.google.com/open?id=1-uQxBMGTRizjhY_QqCJugxVMWcLOvFN2",
        "photo_direct": "https://lh3.googleusercontent.com/u/0/d/1-uQxBMGTRizjhY_QqCJugxVMWcLOvFN2",
        "remarks": None
    },
    {
        "id": "PL_049",
        "name": "Aditya Pramod Tirmare",
        "role": "All-rounder",
        "department": "Msc mathematics",
        "reg_num": "2600905026",
        "course": "Mathematics",
        "wicket_keeper": "No",
        "batting_style": "Right",
        "bowling_hand": "Right",
        "bowling_style": "Medium Fast",
        "photo_url": "https://drive.google.com/open?id=1dPfmyyilAose8jL1j6KGiJ96L5B1SE-v",
        "photo_direct": "https://lh3.googleusercontent.com/u/0/d/1dPfmyyilAose8jL1j6KGiJ96L5B1SE-v",
        "remarks": None
    },
    {
        "id": "PL_050",
        "name": "Padmanabha Luha",
        "role": "All-rounder",
        "department": "IR & POL.SC",
        "reg_num": "2601305048",
        "course": "Master",
        "wicket_keeper": "No",
        "batting_style": "Right",
        "bowling_hand": "Right",
        "bowling_style": "Medium Fast",
        "photo_url": "https://drive.google.com/open?id=143BXUheT_KTQPc8SS6Z39i1XIoxycm7O",
        "photo_direct": "https://lh3.googleusercontent.com/u/0/d/143BXUheT_KTQPc8SS6Z39i1XIoxycm7O",
        "remarks": None
    },
    {
        "id": "PL_051",
        "name": "Sanjai S",
        "role": "Batter",
        "department": "International relations and politics",
        "reg_num": "2501305029",
        "course": "International relations and political science",
        "wicket_keeper": "No",
        "batting_style": "Right",
        "bowling_hand": None,
        "bowling_style": None,
        "photo_url": "https://drive.google.com/open?id=1DlPokiEBWYrQsZyTKUTFk14hiROkXhdo",
        "photo_direct": "https://lh3.googleusercontent.com/u/0/d/1DlPokiEBWYrQsZyTKUTFk14hiROkXhdo",
        "remarks": None
    },
    {
        "id": "PL_052",
        "name": "Devadhathan. V. S",
        "role": "All-rounder",
        "department": "Social work",
        "reg_num": "2601505014",
        "course": "MSW",
        "wicket_keeper": "No",
        "batting_style": "Right",
        "bowling_hand": "Right",
        "bowling_style": "Medium Fast",
        "photo_url": "https://drive.google.com/open?id=1wf_lqs1f29nRnl_MLrLZ8mOQ09ENiyDl",
        "photo_direct": "https://lh3.googleusercontent.com/u/0/d/1wf_lqs1f29nRnl_MLrLZ8mOQ09ENiyDl",
        "remarks": None
    },
    {
        "id": "PL_053",
        "name": "Adhithyan V Suresh",
        "role": "All-rounder",
        "department": "Geology",
        "reg_num": "2602105001",
        "course": "Msc Geology",
        "wicket_keeper": "No",
        "batting_style": "Right",
        "bowling_hand": "Right",
        "bowling_style": "Medium Fast",
        "photo_url": "https://drive.google.com/open?id=13-y3fOUY4B8BFi-9-hhM0YCmWmHPbRBC",
        "photo_direct": "https://lh3.googleusercontent.com/u/0/d/13-y3fOUY4B8BFi-9-hhM0YCmWmHPbRBC",
        "remarks": None
    },
    {
        "id": "PL_054",
        "name": "LOVE KUMAR",
        "role": "All-rounder",
        "department": "Msc .Computer science",
        "reg_num": "2600705016",
        "course": "Computer science",
        "wicket_keeper": "No",
        "batting_style": "Right",
        "bowling_hand": "Right",
        "bowling_style": "Medium Fast",
        "photo_url": "https://drive.google.com/open?id=16d6xEyIghNmy2SHRKdQoeRIPlZ0yN8AT",
        "photo_direct": "https://lh3.googleusercontent.com/u/0/d/16d6xEyIghNmy2SHRKdQoeRIPlZ0yN8AT",
        "remarks": None
    },
    {
        "id": "PL_055",
        "name": "M. Sandeep",
        "role": "All-rounder",
        "department": "School of global studies",
        "reg_num": "2601305017",
        "course": "International relations",
        "wicket_keeper": "No",
        "batting_style": "Right",
        "bowling_hand": "Right",
        "bowling_style": "Medium Fast",
        "photo_url": "https://drive.google.com/open?id=1bDsxSygCb8Mislee-6zO9btpk9AN_4xz",
        "photo_direct": "https://lh3.googleusercontent.com/u/0/d/1bDsxSygCb8Mislee-6zO9btpk9AN_4xz",
        "remarks": None
    },
    {
        "id": "PL_056",
        "name": "Krishna Vamsi",
        "role": "Batter",
        "department": "Microbiology",
        "reg_num": "2602805037",
        "course": "Msc",
        "wicket_keeper": "Yes",
        "batting_style": "Right",
        "bowling_hand": None,
        "bowling_style": None,
        "photo_url": "https://drive.google.com/open?id=1mce8IdTFnusZSNRgXLL3ZfUkJLekMgLV",
        "photo_direct": "https://lh3.googleusercontent.com/u/0/d/1mce8IdTFnusZSNRgXLL3ZfUkJLekMgLV",
        "remarks": "no"
    },
    {
        "id": "PL_057",
        "name": "Rajeev Kumar Singh",
        "role": "Batter",
        "department": "IR &PS",
        "reg_num": "2601305025",
        "course": "IR & PS",
        "wicket_keeper": "No",
        "batting_style": "Right",
        "bowling_hand": None,
        "bowling_style": None,
        "photo_url": "https://drive.google.com/open?id=1QCLZXv7WUDk3S0vSUb6aJOhRum-sxQzP",
        "photo_direct": "https://lh3.googleusercontent.com/u/0/d/1QCLZXv7WUDk3S0vSUb6aJOhRum-sxQzP",
        "remarks": "A mol on my right hand thumb"
    },
    {
        "id": "PL_058",
        "name": "Premraj Nag",
        "role": "Batter",
        "department": "Itep",
        "reg_num": "2501604217",
        "course": "BA.Bed economics",
        "wicket_keeper": "Yes",
        "batting_style": "Right",
        "bowling_hand": None,
        "bowling_style": None,
        "photo_url": "https://drive.google.com/open?id=15CFCAOrjsyZBKcsxZuVjowJJTKIQQKQj",
        "photo_direct": "https://lh3.googleusercontent.com/u/0/d/15CFCAOrjsyZBKcsxZuVjowJJTKIQQKQj",
        "remarks": None
    },
    {
        "id": "PL_059",
        "name": "Siddhanta Nagvanshi",
        "role": "Batter",
        "department": "ITEP",
        "reg_num": "2301604209",
        "course": "ECONOMICS",
        "wicket_keeper": "Yes",
        "batting_style": "Right",
        "bowling_hand": None,
        "bowling_style": None,
        "photo_url": "https://drive.google.com/open?id=1dB8TmUPO9pqATATKnbHRHeFKfnIr5GTW",
        "photo_direct": "https://lh3.googleusercontent.com/u/0/d/1dB8TmUPO9pqATATKnbHRHeFKfnIr5GTW",
        "remarks": "Keep it"
    },
    {
        "id": "PL_060",
        "name": "K.Yaswanth kumar",
        "role": "All-rounder",
        "department": "IR",
        "reg_num": "2501305035",
        "course": "MA international relations and politics",
        "wicket_keeper": "No",
        "batting_style": "Right",
        "bowling_hand": "Right",
        "bowling_style": "Off Spin",
        "photo_url": "https://drive.google.com/open?id=1ATpbhYSEiW35NqqfWQy-W3zlQgaIy6oa",
        "photo_direct": "https://lh3.googleusercontent.com/u/0/d/1ATpbhYSEiW35NqqfWQy-W3zlQgaIy6oa",
        "remarks": "Nothing is there just i want to play under Abhishek or Vamsi captaincy"
    },
    {
        "id": "PL_061",
        "name": "Ramavath Rupesh",
        "role": "Batter",
        "department": "Department of Manegement",
        "reg_num": "2602405024",
        "course": "MBA (general)",
        "wicket_keeper": "No",
        "batting_style": "Right",
        "bowling_hand": None,
        "bowling_style": None,
        "photo_url": "https://drive.google.com/open?id=1Pyf4_BiDRo0GvezUMTSG9Od06ghj8OOO",
        "photo_direct": "https://lh3.googleusercontent.com/u/0/d/1Pyf4_BiDRo0GvezUMTSG9Od06ghj8OOO",
        "remarks": "No"
    },
    {
        "id": "PL_062",
        "name": "BAYAJI PUALA",
        "role": "Batter",
        "department": "Education",
        "reg_num": "2601605003",
        "course": "M.Ed",
        "wicket_keeper": "Yes",
        "batting_style": "Right",
        "bowling_hand": None,
        "bowling_style": None,
        "photo_url": "https://drive.google.com/open?id=1gfDYfLsLs5839m4h_MpU7miRWzPz46Wr",
        "photo_direct": "https://lh3.googleusercontent.com/u/0/d/1gfDYfLsLs5839m4h_MpU7miRWzPz46Wr",
        "remarks": None
    },
    {
        "id": "PL_063",
        "name": "Vishnu K Vinu",
        "role": "Bowler",
        "department": "Department of Law",
        "reg_num": "2501705020",
        "course": "LLM",
        "wicket_keeper": "No",
        "batting_style": "Right",
        "bowling_hand": "Right",
        "bowling_style": "Fast",
        "photo_url": "https://drive.google.com/open?id=1IkofPByqnZTJoHWVLK1By1eH_CtzHHnT",
        "photo_direct": "https://lh3.googleusercontent.com/u/0/d/1IkofPByqnZTJoHWVLK1By1eH_CtzHHnT",
        "remarks": None
    },
    {
        "id": "PL_064",
        "name": "Dayanidhi patra",
        "role": "Batter",
        "department": "ITEP ZOOLOGY",
        "reg_num": "2601604109",
        "course": "Bsc.bed Zoology",
        "wicket_keeper": "No",
        "batting_style": "Right",
        "bowling_hand": None,
        "bowling_style": None,
        "photo_url": "https://drive.google.com/open?id=1Q22g-OnUiybvHCxMnOwEkLgXI9haCNAT",
        "photo_direct": "https://lh3.googleusercontent.com/u/0/d/1Q22g-OnUiybvHCxMnOwEkLgXI9haCNAT",
        "remarks": None
    },
    {
        "id": "PL_065",
        "name": "SuNoneda kishore",
        "role": "Bowler",
        "department": "Business studies",
        "reg_num": "2602504023",
        "course": "Bcom hons",
        "wicket_keeper": "No",
        "batting_style": "Right",
        "bowling_hand": "Right",
        "bowling_style": "Medium Fast",
        "photo_url": "https://drive.google.com/open?id=1fBGhE4xDoVmScdK0GKXKJi0LE2QPrkhK",
        "photo_direct": "https://lh3.googleusercontent.com/u/0/d/1fBGhE4xDoVmScdK0GKXKJi0LE2QPrkhK",
        "remarks": None
    },
    {
        "id": "PL_066",
        "name": "Haseeb M A",
        "role": "All-rounder",
        "department": "Department of commerce and international business",
        "reg_num": "2602504054",
        "course": "Bcom(hons)",
        "wicket_keeper": "No",
        "batting_style": "Right",
        "bowling_hand": "Right",
        "bowling_style": "Off Spin",
        "photo_url": "https://drive.google.com/open?id=1sMNDHmi93lsUlHn7dVU9wFFzdWx4qoVD",
        "photo_direct": "https://lh3.googleusercontent.com/u/0/d/1sMNDHmi93lsUlHn7dVU9wFFzdWx4qoVD",
        "remarks": "Selected in high school cricket team in twice"
    },
    {
        "id": "PL_067",
        "name": "Dasarath(Das)",
        "role": "All-rounder",
        "department": "Education (itep)",
        "reg_num": "2301604012",
        "course": "Bsc bed physics",
        "wicket_keeper": "No",
        "batting_style": "Right",
        "bowling_hand": "Right",
        "bowling_style": "Fast",
        "photo_url": "https://drive.google.com/open?id=14LqgKedZZUKgb0r2O8PseSGClFkGhD46",
        "photo_direct": "https://lh3.googleusercontent.com/u/0/d/14LqgKedZZUKgb0r2O8PseSGClFkGhD46",
        "remarks": "No"
    },
    {
        "id": "PL_068",
        "name": "Arjun P",
        "role": "All-rounder",
        "department": "iTEP",
        "reg_num": "2401604104",
        "course": "zoology",
        "wicket_keeper": "No",
        "batting_style": "Right",
        "bowling_hand": "Right",
        "bowling_style": "Off Spin",
        "photo_url": "https://drive.google.com/open?id=1Yj8qnYXFU8l47XXDcCgHhFbLRGboJE1R",
        "photo_direct": "https://lh3.googleusercontent.com/u/0/d/1Yj8qnYXFU8l47XXDcCgHhFbLRGboJE1R",
        "remarks": None
    },
    {
        "id": "PL_069",
        "name": "Arjun S Nair",
        "role": "Bowler",
        "department": "ITEP",
        "reg_num": "266410069116",
        "course": "Bcom bed",
        "wicket_keeper": "No",
        "batting_style": "Right",
        "bowling_hand": "Right",
        "bowling_style": "Off Spin",
        "photo_url": "https://drive.google.com/open?id=15i8PLtuwvvmzQYOE2XHbvHuF7akNsaIG",
        "photo_direct": "https://lh3.googleusercontent.com/u/0/d/15i8PLtuwvvmzQYOE2XHbvHuF7akNsaIG",
        "remarks": None
    },
    {
        "id": "PL_070",
        "name": "A Tharun",
        "role": "Bowler",
        "department": "Business studies",
        "reg_num": "2502504001",
        "course": "B.com",
        "wicket_keeper": "No",
        "batting_style": "Right",
        "bowling_hand": "Right",
        "bowling_style": "Medium Fast",
        "photo_url": "https://drive.google.com/open?id=1pJ_MGCpZXB28zNPRb0VrASNJhlfapbEp",
        "photo_direct": "https://lh3.googleusercontent.com/u/0/d/1pJ_MGCpZXB28zNPRb0VrASNJhlfapbEp",
        "remarks": None
    },
    {
        "id": "PL_071",
        "name": "Venu hr",
        "role": "Batter",
        "department": "IR",
        "reg_num": "2601305036",
        "course": "MA",
        "wicket_keeper": "No",
        "batting_style": "Right",
        "bowling_hand": None,
        "bowling_style": None,
        "photo_url": "https://drive.google.com/open?id=1iLLCEMJ68uT9ppmS2hbGhqb1YdSbTctW",
        "photo_direct": "https://lh3.googleusercontent.com/u/0/d/1iLLCEMJ68uT9ppmS2hbGhqb1YdSbTctW",
        "remarks": "Better fielder"
    },
    {
        "id": "PL_072",
        "name": "Karan",
        "role": "All-rounder",
        "department": "IR",
        "reg_num": "2601305015",
        "course": "MA",
        "wicket_keeper": "No",
        "batting_style": "Right",
        "bowling_hand": "Right",
        "bowling_style": "Medium Fast",
        "photo_url": "https://drive.google.com/open?id=1dDmaAINu6hlR291xXy47H_rqnBScNPLX",
        "photo_direct": "https://lh3.googleusercontent.com/u/0/d/1dDmaAINu6hlR291xXy47H_rqnBScNPLX",
        "remarks": None
    },
    {
        "id": "PL_073",
        "name": "Bhanu Prakash",
        "role": "All-rounder",
        "department": "Ma economics",
        "reg_num": "2500205027",
        "course": "Ma economics",
        "wicket_keeper": "No",
        "batting_style": "Right",
        "bowling_hand": "Right",
        "bowling_style": "Medium Fast",
        "photo_url": "https://drive.google.com/open?id=1GdwN9kOqOxYVwYYYIDdoUbUNbWXK_WHu",
        "photo_direct": "https://lh3.googleusercontent.com/u/0/d/1GdwN9kOqOxYVwYYYIDdoUbUNbWXK_WHu",
        "remarks": None
    },
    {
        "id": "PL_074",
        "name": "Amaljith",
        "role": "Batter",
        "department": "DCIB",
        "reg_num": "2302507002",
        "course": "PhD",
        "wicket_keeper": "Yes",
        "batting_style": "Right",
        "bowling_hand": None,
        "bowling_style": None,
        "photo_url": "https://drive.google.com/open?id=1yvBLRmSSeS_cpXKLTyaaFBjnEPPBOQHX",
        "photo_direct": "https://lh3.googleusercontent.com/u/0/d/1yvBLRmSSeS_cpXKLTyaaFBjnEPPBOQHX",
        "remarks": None
    },
    {
        "id": "PL_075",
        "name": "Karthik Shukla",
        "role": "All-rounder",
        "department": "International relations (IR)",
        "reg_num": "2601305016",
        "course": "MA in IR",
        "wicket_keeper": "No",
        "batting_style": "Right",
        "bowling_hand": "Right",
        "bowling_style": "Medium Fast",
        "photo_url": "https://drive.google.com/open?id=1F_SR3H_t6XRSlHbVbmD5R8QA0pEu7K33",
        "photo_direct": "https://lh3.googleusercontent.com/u/0/d/1F_SR3H_t6XRSlHbVbmD5R8QA0pEu7K33",
        "remarks": None
    },
    {
        "id": "PL_076",
        "name": "Harsha",
        "role": "Batter",
        "department": "Public administration and policy study",
        "reg_num": "2602005010",
        "course": "Public administration",
        "wicket_keeper": "No",
        "batting_style": "Right",
        "bowling_hand": None,
        "bowling_style": None,
        "photo_url": "https://drive.google.com/open?id=1WZI3BQdJ39XsettIRjyVK99z3O16jekB",
        "photo_direct": "https://lh3.googleusercontent.com/u/0/d/1WZI3BQdJ39XsettIRjyVK99z3O16jekB",
        "remarks": "No"
    },
    {
        "id": "PL_077",
        "name": "Shubham Kumar",
        "role": "Batter",
        "department": "Computer science",
        "reg_num": "260070422",
        "course": "Bca",
        "wicket_keeper": "Yes",
        "batting_style": "Right",
        "bowling_hand": None,
        "bowling_style": None,
        "photo_url": "https://drive.google.com/open?id=15oC3ex9HorytCjyDkD498iaSXcZOKm4j",
        "photo_direct": "https://lh3.googleusercontent.com/u/0/d/15oC3ex9HorytCjyDkD498iaSXcZOKm4j",
        "remarks": "No"
    },
    {
        "id": "PL_078",
        "name": "Damodhara naidu",
        "role": "All-rounder",
        "department": "Law",
        "reg_num": "2501705016",
        "course": "LLM",
        "wicket_keeper": "No",
        "batting_style": "Right",
        "bowling_hand": "Right",
        "bowling_style": "Medium Fast",
        "photo_url": "https://drive.google.com/open?id=1I5mj2NEcWkp8ZRXffVhRJOLdkiqaEVHq",
        "photo_direct": "https://lh3.googleusercontent.com/u/0/d/1I5mj2NEcWkp8ZRXffVhRJOLdkiqaEVHq",
        "remarks": None
    },
    {
        "id": "PL_079",
        "name": "Firdosh Khan",
        "role": "All-rounder",
        "department": "Itep bsc bed physics",
        "reg_num": "2601604005",
        "course": "Bsc bed physics ITEP",
        "wicket_keeper": "No",
        "batting_style": "Right",
        "bowling_hand": "Right",
        "bowling_style": "Medium Fast",
        "photo_url": "https://drive.google.com/open?id=1IkzhKDYPj0NnHTtaW2g9OVcyt4avrDOs",
        "photo_direct": "https://lh3.googleusercontent.com/u/0/d/1IkzhKDYPj0NnHTtaW2g9OVcyt4avrDOs",
        "remarks": None
    },
    {
        "id": "PL_080",
        "name": "Sarathlal M , SRT 13",
        "role": "Bowler",
        "department": "English",
        "reg_num": "2300107009",
        "course": "PhD",
        "wicket_keeper": "No",
        "batting_style": "Right",
        "bowling_hand": "Right",
        "bowling_style": "Medium Fast",
        "photo_url": "https://drive.google.com/open?id=1-h0h76PV-vuAwaFOkOOARfN4xMTRkfOD",
        "photo_direct": "https://lh3.googleusercontent.com/u/0/d/1-h0h76PV-vuAwaFOkOOARfN4xMTRkfOD",
        "remarks": "Playing for a team"
    },
    {
        "id": "PL_081",
        "name": "Aadil J",
        "role": "Bowler",
        "department": "Economics",
        "reg_num": "2500205016",
        "course": "2nd MA ECONOMICS",
        "wicket_keeper": "No",
        "batting_style": "Right",
        "bowling_hand": "Right",
        "bowling_style": "Medium Fast",
        "photo_url": "https://drive.google.com/open?id=1m5prfvrdkTqUVhrh2fMRfiLiXkxyUUmJ",
        "photo_direct": "https://lh3.googleusercontent.com/u/0/d/1m5prfvrdkTqUVhrh2fMRfiLiXkxyUUmJ",
        "remarks": None
    },
    {
        "id": "PL_082",
        "name": "Jayaraj P",
        "role": "All-rounder",
        "department": "Dept. Of Commerce & IB",
        "reg_num": "2602507002",
        "course": "Commerce",
        "wicket_keeper": "No",
        "batting_style": "Right",
        "bowling_hand": "Right",
        "bowling_style": "Off Spin",
        "photo_url": "https://drive.google.com/open?id=1DGsQM9HUIN6c6Hcmkbs5ni3GfQyd5QMk",
        "photo_direct": "https://lh3.googleusercontent.com/u/0/d/1DGsQM9HUIN6c6Hcmkbs5ni3GfQyd5QMk",
        "remarks": None
    },
    {
        "id": "PL_083",
        "name": "BAYAJI PUALA",
        "role": "Batter",
        "department": "Education",
        "reg_num": "2601605003",
        "course": "M.Ed",
        "wicket_keeper": "Yes",
        "batting_style": "Right",
        "bowling_hand": None,
        "bowling_style": None,
        "photo_url": "https://drive.google.com/open?id=1wKdhetzwOlwz2QSbfx_eEfKsfLJi9jFN",
        "photo_direct": "https://lh3.googleusercontent.com/u/0/d/1wKdhetzwOlwz2QSbfx_eEfKsfLJi9jFN",
        "remarks": None
    },
    {
        "id": "PL_084",
        "name": "ANDREW",
        "role": "Batter",
        "department": "Public administration",
        "reg_num": "2602005034",
        "course": "Public administration and policy studies",
        "wicket_keeper": "No",
        "batting_style": "Right",
        "bowling_hand": None,
        "bowling_style": None,
        "photo_url": "https://drive.google.com/open?id=10Nhal4_2PkQwW8pYljrCo45A6qkZJKKQ",
        "photo_direct": "https://lh3.googleusercontent.com/u/0/d/10Nhal4_2PkQwW8pYljrCo45A6qkZJKKQ",
        "remarks": None
    },
    {
        "id": "PL_085",
        "name": "R.S.Niranchan",
        "role": "All-rounder",
        "department": "Department of commerce and international Business",
        "reg_num": "2502504020",
        "course": "B.Com(hons)",
        "wicket_keeper": "No",
        "batting_style": "Left",
        "bowling_hand": "Right",
        "bowling_style": "Medium Fast",
        "photo_url": "https://drive.google.com/open?id=1QKLn8tR_sN-StOIE3BUUsEDwYmgiRiaa",
        "photo_direct": "https://lh3.googleusercontent.com/u/0/d/1QKLn8tR_sN-StOIE3BUUsEDwYmgiRiaa",
        "remarks": None
    },
    {
        "id": "PL_086",
        "name": "Amal.A",
        "role": "All-rounder",
        "department": "Commerce",
        "reg_num": "8075870054",
        "course": "Phd",
        "wicket_keeper": "No",
        "batting_style": "Left",
        "bowling_hand": "Right",
        "bowling_style": "Medium Fast",
        "photo_url": "https://drive.google.com/open?id=14Mmp0cf-Q8zWia2Qmw1VWkfQOykGKOJa",
        "photo_direct": "https://lh3.googleusercontent.com/u/0/d/14Mmp0cf-Q8zWia2Qmw1VWkfQOykGKOJa",
        "remarks": None
    },
    {
        "id": "PL_087",
        "name": "Pramod Kumar",
        "role": "Bowler",
        "department": "Chemistry",
        "reg_num": "PCH071904",
        "course": "PhD",
        "wicket_keeper": "No",
        "batting_style": "Right",
        "bowling_hand": "Right",
        "bowling_style": "Fast",
        "photo_url": "https://drive.google.com/open?id=1W8Jf8yRXQ49MNpdghfhMeeLbpRSIMuNm",
        "photo_direct": "https://lh3.googleusercontent.com/u/0/d/1W8Jf8yRXQ49MNpdghfhMeeLbpRSIMuNm",
        "remarks": None
    },
    {
        "id": "PL_088",
        "name": "Blessing S",
        "role": "Batter",
        "department": "Computer Science",
        "reg_num": "2600704031",
        "course": "BCA Honours",
        "wicket_keeper": "Yes",
        "batting_style": "Right",
        "bowling_hand": None,
        "bowling_style": None,
        "photo_url": "https://drive.google.com/open?id=1EH0K3LK82xjxTMO2nUYNl9ZkEV5iCSMW",
        "photo_direct": "https://lh3.googleusercontent.com/u/0/d/1EH0K3LK82xjxTMO2nUYNl9ZkEV5iCSMW",
        "remarks": None
    },
    {
        "id": "PL_089",
        "name": "Vivek M S",
        "role": "All-rounder",
        "department": "Public health",
        "reg_num": "2301907012",
        "course": "PhD",
        "wicket_keeper": "No",
        "batting_style": "Right",
        "bowling_hand": "Right",
        "bowling_style": "Medium Fast",
        "photo_url": "https://drive.google.com/open?id=1c5UG_dbdl7FSYc7RU4I26wAh795pjkpf",
        "photo_direct": "https://lh3.googleusercontent.com/u/0/d/1c5UG_dbdl7FSYc7RU4I26wAh795pjkpf",
        "remarks": None
    },
    {
        "id": "PL_090",
        "name": "Kaushik",
        "role": "All-rounder",
        "department": "School of global studies",
        "reg_num": "2602304011",
        "course": "International relations",
        "wicket_keeper": "No",
        "batting_style": "Right",
        "bowling_hand": "Right",
        "bowling_style": "Fast",
        "photo_url": "https://drive.google.com/open?id=1kCuVIMAX7oUdn5dDctlpzpyxHGhR3krA",
        "photo_direct": "https://lh3.googleusercontent.com/u/0/d/1kCuVIMAX7oUdn5dDctlpzpyxHGhR3krA",
        "remarks": "I played in Tamilnadu U17 divisional and some school and club matches in Tamilnadu and attended boost divisional camps"
    },
    {
        "id": "PL_091",
        "name": "Mohammed Farhan PP",
        "role": "All-rounder",
        "department": "Computer Science",
        "reg_num": "2600704027",
        "course": "BCA",
        "wicket_keeper": "No",
        "batting_style": "Left",
        "bowling_hand": "Right",
        "bowling_style": "Fast",
        "photo_url": "https://drive.google.com/open?id=1rhzcXT9W5Somsu9p1letjnrGm437Kpzk",
        "photo_direct": "https://lh3.googleusercontent.com/u/0/d/1rhzcXT9W5Somsu9p1letjnrGm437Kpzk",
        "remarks": None
    },
    {
        "id": "PL_092",
        "name": "Srirama Abith",
        "role": "All-rounder",
        "department": "Computer st",
        "reg_num": "2600704056",
        "course": "Bca",
        "wicket_keeper": "No",
        "batting_style": "Right",
        "bowling_hand": "Right",
        "bowling_style": "Medium Fast",
        "photo_url": "https://drive.google.com/open?id=12ePkioABpblLO2dCqAq79EWR-aJlk2y3",
        "photo_direct": "https://lh3.googleusercontent.com/u/0/d/12ePkioABpblLO2dCqAq79EWR-aJlk2y3",
        "remarks": None
    },
    {
        "id": "PL_093",
        "name": "V siddu Naik",
        "role": "All-rounder",
        "department": "MBA TTM",
        "reg_num": "2502605024",
        "course": "Travel and tourism management",
        "wicket_keeper": "No",
        "batting_style": "Right",
        "bowling_hand": "Right",
        "bowling_style": "Medium Fast",
        "photo_url": "https://drive.google.com/open?id=12Opy5GORf9ZqAzkRUU5wBXnHKSpaA-Y6",
        "photo_direct": "https://lh3.googleusercontent.com/u/0/d/12Opy5GORf9ZqAzkRUU5wBXnHKSpaA-Y6",
        "remarks": None
    },
    {
        "id": "PL_094",
        "name": "G.NAVEEN",
        "role": "Batter",
        "department": "public administration and policy studies",
        "reg_num": "2602005016",
        "course": "M.a public administration and policy studies",
        "wicket_keeper": "No",
        "batting_style": "Right",
        "bowling_hand": None,
        "bowling_style": None,
        "photo_url": "https://drive.google.com/open?id=1xEzyjmBZVdR15puXG8rXKwyPSdS9VQHP",
        "photo_direct": "https://lh3.googleusercontent.com/u/0/d/1xEzyjmBZVdR15puXG8rXKwyPSdS9VQHP",
        "remarks": "No"
    },
    {
        "id": "PL_095",
        "name": "Satyajeet Debnath",
        "role": "All-rounder",
        "department": "biochemistry and molecular biology",
        "reg_num": "2600305021",
        "course": "biochemistry",
        "wicket_keeper": "No",
        "batting_style": "Right",
        "bowling_hand": "Right",
        "bowling_style": "Fast",
        "photo_url": "https://drive.google.com/open?id=1MupFz9rGwS0tjVKGyhFbq8_ZYzHgOST9",
        "photo_direct": "https://lh3.googleusercontent.com/u/0/d/1MupFz9rGwS0tjVKGyhFbq8_ZYzHgOST9",
        "remarks": None
    },
    {
        "id": "PL_096",
        "name": "Sasi Pranesh",
        "role": "Bowler",
        "department": "Chemistry",
        "reg_num": "2501105041",
        "course": "M.Sc Chemistry",
        "wicket_keeper": "No",
        "batting_style": "Right",
        "bowling_hand": "Right",
        "bowling_style": "Fast",
        "photo_url": "https://drive.google.com/open?id=1ox08XJzOfgkxcXBNS_D91S8J9yl-ClUD",
        "photo_direct": "https://lh3.googleusercontent.com/u/0/d/1ox08XJzOfgkxcXBNS_D91S8J9yl-ClUD",
        "remarks": None
    },
    {
        "id": "PL_097",
        "name": "Ramesh",
        "role": "All-rounder",
        "department": "Itep,  education",
        "reg_num": "2301604308",
        "course": "B.A B.Ed English",
        "wicket_keeper": "No",
        "batting_style": "Right",
        "bowling_hand": "Right",
        "bowling_style": "Medium Fast",
        "photo_url": "https://drive.google.com/open?id=1x-5hKsvbnMq5bMZr3EFFc9QiVIgd6NvG",
        "photo_direct": "https://lh3.googleusercontent.com/u/0/d/1x-5hKsvbnMq5bMZr3EFFc9QiVIgd6NvG",
        "remarks": None
    },
    {
        "id": "PL_098",
        "name": "Nonedhakishore",
        "role": "Batter",
        "department": "Zoology",
        "reg_num": "2600405025",
        "course": "Msc zoology",
        "wicket_keeper": "No",
        "batting_style": "Right",
        "bowling_hand": None,
        "bowling_style": None,
        "photo_url": "https://drive.google.com/open?id=1xMjZYctaw2ckkU4TISLRXHawv88w-XMD",
        "photo_direct": "https://lh3.googleusercontent.com/u/0/d/1xMjZYctaw2ckkU4TISLRXHawv88w-XMD",
        "remarks": "No"
    },
    {
        "id": "PL_099",
        "name": "Sukhveer singh",
        "role": "Batter",
        "department": "Mathematics",
        "reg_num": "2600905025",
        "course": "M.Sc.(Mathematics)",
        "wicket_keeper": "No",
        "batting_style": "Right",
        "bowling_hand": None,
        "bowling_style": None,
        "photo_url": "https://drive.google.com/open?id=13eJnSqCxrXH7cJY1aEFSF5FsfbRHZyld",
        "photo_direct": "https://lh3.googleusercontent.com/u/0/d/13eJnSqCxrXH7cJY1aEFSF5FsfbRHZyld",
        "remarks": None
    },
    {
        "id": "PL_100",
        "name": "SreeHari",
        "role": "Batter",
        "department": "FiNonece",
        "reg_num": "Ent94",
        "course": None,
        "wicket_keeper": "Yes",
        "batting_style": "Right",
        "bowling_hand": None,
        "bowling_style": None,
        "photo_url": "https://drive.google.com/open?id=1h_lzNubZpIrk3xqMfLdPKNftPNwq273C",
        "photo_direct": "https://lh3.googleusercontent.com/u/0/d/1h_lzNubZpIrk3xqMfLdPKNftPNwq273C",
        "remarks": None
    },
    {
        "id": "PL_101",
        "name": "Rathin",
        "role": "Batter",
        "department": "ICT",
        "reg_num": "1102829",
        "course": "Techie",
        "wicket_keeper": "Yes",
        "batting_style": "Right",
        "bowling_hand": None,
        "bowling_style": None,
        "photo_url": "https://drive.google.com/open?id=10gapt7T1ZXsRURLubhcdFkTaT2QCTTB0",
        "photo_direct": "https://lh3.googleusercontent.com/u/0/d/10gapt7T1ZXsRURLubhcdFkTaT2QCTTB0",
        "remarks": "Any query call me 8943892428"
    },
    {
        "id": "PL_102",
        "name": "Shyam Balal",
        "role": "All-rounder",
        "department": "ICT",
        "reg_num": "Nil",
        "course": "Nil",
        "wicket_keeper": "No",
        "batting_style": "Right",
        "bowling_hand": "Right",
        "bowling_style": "Medium Fast",
        "photo_url": "https://drive.google.com/open?id=1ENurFWcj9rlk22LuXd8Kdo3Wlyqao-po",
        "photo_direct": "https://lh3.googleusercontent.com/u/0/d/1ENurFWcj9rlk22LuXd8Kdo3Wlyqao-po",
        "remarks": "Nil"
    },
    {
        "id": "PL_103",
        "name": "Aswin Hitheswar",
        "role": "All-rounder",
        "department": "Itep staff",
        "reg_num": "9495949227",
        "course": "Staff",
        "wicket_keeper": "No",
        "batting_style": "Right",
        "bowling_hand": "Right",
        "bowling_style": "Medium Fast",
        "photo_url": "https://drive.google.com/open?id=1Kljkg6l5tfVZ1mO1Ry6AsLJ1uHog8IqA",
        "photo_direct": "https://lh3.googleusercontent.com/u/0/d/1Kljkg6l5tfVZ1mO1Ry6AsLJ1uHog8IqA",
        "remarks": None
    },
    {
        "id": "PL_104",
        "name": "Akhilesh M K",
        "role": "All-rounder",
        "department": "VC Office",
        "reg_num": "ENT 54",
        "course": "Staff",
        "wicket_keeper": "No",
        "batting_style": "Right",
        "bowling_hand": "Right",
        "bowling_style": "Medium Fast",
        "photo_url": "https://drive.google.com/open?id=18YtshJovViKtFzZVlgRlFPeQZ0Mgizr8",
        "photo_direct": "https://lh3.googleusercontent.com/u/0/d/18YtshJovViKtFzZVlgRlFPeQZ0Mgizr8",
        "remarks": None
    },
    {
        "id": "PL_105",
        "name": "Sivaprasad T",
        "role": "All-rounder",
        "department": "Staff- Economics Dept",
        "reg_num": "40018- id card nmuber",
        "course": "Staff",
        "wicket_keeper": "No",
        "batting_style": "Right",
        "bowling_hand": "Right",
        "bowling_style": "Fast",
        "photo_url": "https://drive.google.com/open?id=1yNHEaWZBcrZjdB2FEeLeT4KM-mkop30_",
        "photo_direct": "https://lh3.googleusercontent.com/u/0/d/1yNHEaWZBcrZjdB2FEeLeT4KM-mkop30_",
        "remarks": None
    },
    {
        "id": "PL_106",
        "name": "Dr. KanNone A S",
        "role": "All-rounder",
        "department": "Health Center",
        "reg_num": "CUK NT 89",
        "course": "Senior Medical Officer",
        "wicket_keeper": "No",
        "batting_style": "Right",
        "bowling_hand": "Right",
        "bowling_style": "Medium Fast",
        "photo_url": "https://drive.google.com/open?id=11y1D2-X7ATCbWa66gJtp6tFadPBmy-Bs",
        "photo_direct": "https://lh3.googleusercontent.com/u/0/d/11y1D2-X7ATCbWa66gJtp6tFadPBmy-Bs",
        "remarks": "No"
    },
    {
        "id": "PL_107",
        "name": "Muraleedharan",
        "role": "All-rounder",
        "department": "Administration",
        "reg_num": "10",
        "course": "Estate",
        "wicket_keeper": "No",
        "batting_style": "Right",
        "bowling_hand": "Right",
        "bowling_style": "Leg Spin",
        "photo_url": "https://drive.google.com/open?id=1CHEn1irK8J9qPjeCobGqy72r0DfMcP0d",
        "photo_direct": "https://lh3.googleusercontent.com/u/0/d/1CHEn1irK8J9qPjeCobGqy72r0DfMcP0d",
        "remarks": None
    },
    {
        "id": "PL_108",
        "name": "Test2",
        "role": "Batter",
        "department": "Test2",
        "reg_num": "Test2",
        "course": "Test2",
        "wicket_keeper": "Yes",
        "batting_style": "Right",
        "bowling_hand": None,
        "bowling_style": None,
        "photo_url": "https://drive.google.com/open?id=1EJ21ttIvs8adwdUCLrftg4HfulCJ0E5L",
        "photo_direct": "https://lh3.googleusercontent.com/u/0/d/1EJ21ttIvs8adwdUCLrftg4HfulCJ0E5L",
        "remarks": None
    },
    {
        "id": "PL_109",
        "name": "Sujith kumar k v",
        "role": "Batter",
        "department": "Admin",
        "reg_num": "114",
        "course": "Admin",
        "wicket_keeper": "No",
        "batting_style": "Right",
        "bowling_hand": None,
        "bowling_style": None,
        "photo_url": "https://drive.google.com/open?id=1AHYLarcP50pHxl7h2VL0EtZBumuH8DmT",
        "photo_direct": "https://lh3.googleusercontent.com/u/0/d/1AHYLarcP50pHxl7h2VL0EtZBumuH8DmT",
        "remarks": None
    },
    {
        "id": "PL_110",
        "name": "G. Dinesh",
        "role": "All-rounder",
        "department": "Ir",
        "reg_num": "2501305005",
        "course": "IR",
        "wicket_keeper": "No",
        "batting_style": "Right",
        "bowling_hand": "Right",
        "bowling_style": "Medium Fast",
        "photo_url": "https://drive.google.com/open?id=1fdYKekFzvWNT1YsSQwH-Nb2AQ5ZiFRho",
        "photo_direct": "https://lh3.googleusercontent.com/u/0/d/1fdYKekFzvWNT1YsSQwH-Nb2AQ5ZiFRho",
        "remarks": None
    },
    {
        "id": "PL_111",
        "name": "SHASHIVADHAN",
        "role": "All-rounder",
        "department": "IR",
        "reg_num": "2601305037",
        "course": "IR",
        "wicket_keeper": "No",
        "batting_style": "Right",
        "bowling_hand": "Right",
        "bowling_style": "Medium Fast",
        "photo_url": "https://drive.google.com/open?id=1tJA79CLRkY7K-jslCyiPrQtcEqfw6gEu",
        "photo_direct": "https://lh3.googleusercontent.com/u/0/d/1tJA79CLRkY7K-jslCyiPrQtcEqfw6gEu",
        "remarks": None
    },
    {
        "id": "PL_112",
        "name": "Amaljith P K",
        "role": "All-rounder",
        "department": "Education",
        "reg_num": "2501607005",
        "course": "PhD",
        "wicket_keeper": "No",
        "batting_style": "Right",
        "bowling_hand": "Right",
        "bowling_style": "Medium Fast",
        "photo_url": "https://drive.google.com/open?id=1i57atehTDuRHJDrP7vxMzH_NjSgdSfsK",
        "photo_direct": "https://lh3.googleusercontent.com/u/0/d/1i57atehTDuRHJDrP7vxMzH_NjSgdSfsK",
        "remarks": None
    },
    {
        "id": "PL_113",
        "name": "Chitharanjan",
        "role": "All-rounder",
        "department": "Education",
        "reg_num": "2501607005",
        "course": "ITEP",
        "wicket_keeper": "No",
        "batting_style": "Right",
        "bowling_hand": "Right",
        "bowling_style": "Medium Fast",
        "photo_url": "https://drive.google.com/open?id=1i57atehTDuRHJDrP7vxMzH_NjSgdSfsK",
        "photo_direct": "https://lh3.googleusercontent.com/u/0/d/1i57atehTDuRHJDrP7vxMzH_NjSgdSfsK",
        "remarks": None
    },
    {
        "id": "PL_114",
        "name": "Dhananjay",
        "role": "Batter",
        "department": "ITEP",
        "reg_num": "125454545",
        "course": "ITEP",
        "wicket_keeper": "Yes",
        "batting_style": "Right",
        "bowling_hand": None,
        "bowling_style": None,
        "photo_url": "https://drive.google.com/open?id=1AHYLarcP50pHxl7h2VL0EtZBumuH8DmT",
        "photo_direct": "https://lh3.googleusercontent.com/u/0/d/1AHYLarcP50pHxl7h2VL0EtZBumuH8DmT",
        "remarks": None
    }
]

# ----------------------------------------
# 2. DATA LOAD & STATE INITIALIZATION
# ----------------------------------------
@st.cache_data
def get_initial_player_data():
    # Fallback to embedded players if no file is found
    if os.path.exists('cleaned-player-registry.csv'):
        try:
            return pd.read_csv('cleaned-player-registry.csv').to_dict(orient='records')
        except Exception:
            return EMBEDDED_PLAYERS
    return EMBEDDED_PLAYERS

def init_state():
    if 'players' not in st.session_state:
        # Load players list and convert status
        raw_players = get_initial_player_data()
        st.session_state.players = []
        for p in raw_players:
            st.session_state.players.append({
                "id": p["id"],
                "name": p["name"],
                "role": p["role"],
                "department": p.get("department", ""),
                "reg_num": p.get("reg_num", ""),
                "course": p.get("course", ""),
                "wicket_keeper": p.get("wicket_keeper", "No"),
                "batting_style": p.get("batting_style", "Right"),
                "bowling_hand": p.get("bowling_hand", "N/A"),
                "bowling_style": p.get("bowling_style", "N/A"),
                "photo_url": p.get("photo_url", ""),
                "photo_direct": p.get("photo_direct", ""),
                "remarks": p.get("remarks", ""),
                "status": "Available", # Available, Sold, Unsold
                "sold_team": None,
                "sold_price": 0
            })
            
    if 'teams' not in st.session_state:
        # Default teams for MHPL Cricket Tournament
        st.session_state.teams = {
            "The Bison XI": {"budget": 1000, "spent": 0, "players": []},
            "Titans CUK": {"budget": 1000, "spent": 0, "players": []},
            "Spartans": {"budget": 1000, "spent": 0, "players": []},
            "CUK Akatsuki": {"budget": 1000, "spent": 0, "players": []},
            "Elite XI": {"budget": 1000, "spent": 0, "players": []},
            "Falcons CUK": {"budget": 1000, "spent": 0, "players": []}
        }
        
    if 'current_player_id' not in st.session_state:
        st.session_state.current_player_id = None
        
    if 'bid_history' not in st.session_state:
        st.session_state.bid_history = []
        
    if 'current_bid' not in st.session_state:
        st.session_state.current_bid = 20 # Default base price
        
    if 'current_bidder' not in st.session_state:
        st.session_state.current_bidder = None
        
    if 'transaction_log' not in st.session_state:
        st.session_state.transaction_log = []
        
    if 'history_log' not in st.session_state:
        st.session_state.history_log = [] # For undo functionality

# Auto-save/load progress locally
def save_session_to_file():
    state_data = {
        "teams": st.session_state.teams,
        "players": [
            {
                "id": p["id"],
                "status": p["status"],
                "sold_team": p["sold_team"],
                "sold_price": p["sold_price"]
            } for p in st.session_state.players
        ],
        "current_player_id": st.session_state.current_player_id,
        "transaction_log": st.session_state.transaction_log,
        "history_log": st.session_state.history_log
    }
    with open('auction_state.json', 'w') as f:
        json.dump(state_data, f, indent=2)

def load_session_from_file():
    if os.path.exists('auction_state.json'):
        try:
            with open('auction_state.json', 'r') as f:
                state_data = json.load(f)
                
            # Restore teams
            st.session_state.teams = state_data["teams"]
            
            # Restore player statuses
            player_map = {p["id"]: p for p in state_data["players"]}
            for p in st.session_state.players:
                if p["id"] in player_map:
                    p["status"] = player_map[p["id"]]["status"]
                    p["sold_team"] = player_map[p["id"]]["sold_team"]
                    p["sold_price"] = player_map[p["id"]]["sold_price"]
                    
            # Restore control state
            st.session_state.current_player_id = state_data["current_player_id"]
            st.session_state.transaction_log = state_data["transaction_log"]
            st.session_state.history_log = state_data["history_log"]
            return True
        except Exception as e:
            st.error(f"Error loading auto-saved state: {e}")
    return False

# Initialize
init_state()
load_session_from_file()

# Helper to get current active player
def get_current_player():
    if st.session_state.current_player_id:
        for p in st.session_state.players:
            if p["id"] == st.session_state.current_player_id:
                return p
    return None

# Helper to log actions
def log_action(action_desc):
    st.session_state.transaction_log.append({
        "timestamp": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"),
        "description": action_desc
    })

# ----------------------------------------
# 3. SIDEBAR CONTROLS
# ----------------------------------------
with st.sidebar:
    st.markdown("<h1 style='text-align: center; color: #e0a96d;'>🏏 MHPL Auction</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-style: italic; color: #b0c4de;'>Cricket League Registration Registry Auction Center</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Live stats
    total_players = len(st.session_state.players)
    sold_players = sum(1 for p in st.session_state.players if p["status"] == "Sold")
    unsold_players = sum(1 for p in st.session_state.players if p["status"] == "Unsold")
    available_players = sum(1 for p in st.session_state.players if p["status"] == "Available")
    
    st.markdown("### 📊 Live Stats")
    col_stat1, col_stat2 = st.columns(2)
    with col_stat1:
        st.metric("Total Players", total_players)
        st.metric("Sold Players", sold_players)
    with col_stat2:
        st.metric("Available", available_players)
        st.metric("Unsold", unsold_players)
        
    st.markdown("---")
    
    # State Save/Restore
    st.markdown("### 💾 Backup & Sync")
    
    # Download JSON button
    full_state_json = json.dumps({
        "teams": st.session_state.teams,
        "players": st.session_state.players,
        "current_player_id": st.session_state.current_player_id,
        "transaction_log": st.session_state.transaction_log,
        "history_log": st.session_state.history_log
    }, indent=2)
    
    st.download_button(
        label="Download Auction State",
        data=full_state_json,
        file_name="mhpl_auction_state.json",
        mime="application/json",
        use_container_width=True
    )
    
    # Upload JSON
    uploaded_state = st.file_uploader("Upload Auction State to Resume", type="json")
    if uploaded_state is not None:
        try:
            uploaded_data = json.load(uploaded_state)
            st.session_state.teams = uploaded_data["teams"]
            st.session_state.players = uploaded_data["players"]
            st.session_state.current_player_id = uploaded_data["current_player_id"]
            st.session_state.transaction_log = uploaded_data["transaction_log"]
            st.session_state.history_log = uploaded_data["history_log"]
            st.success("Auction state successfully restored!")
            st.rerun()
        except Exception as e:
            st.error(f"Failed to parse state file: {e}")
            
    st.markdown("---")
    
    # Reset Button with confirmation
    st.markdown("### ⚙️ Reset Center")
    if st.checkbox("Enable Safe Reset"):
        if st.button("RESET ALL AUCTION DATA", type="primary", use_container_width=True):
            # Clear state
            if os.path.exists('auction_state.json'):
                os.remove('auction_state.json')
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.success("All auction data reset successfully!")
            st.rerun()

# ----------------------------------------
# 4. MAIN INTERFACE TABS
# ----------------------------------------
tab_arena, tab_rosters, tab_registry, tab_analytics, tab_logs = st.tabs([
    "🔨 Live Auction Arena", 
    "📋 Team Rosters & Budgets", 
    "🔍 Player Registry & Search", 
    "📊 Spending Analytics",
    "📝 Transaction Log"
])

# ----------------------------------------
# TAB 1: LIVE AUCTION ARENA
# ----------------------------------------
with tab_arena:
    # Get current active player first so we can use it in calculations/widgets
    current_p = get_current_player()
    available_player_options = [p for p in st.session_state.players if p["status"] == "Available"]

    # Top banner or quick metrics
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.markdown("### 🔨 Bidding Room")
    with col_b:
        # Configuration parameters
        base_price_val = st.number_input("Base Player Price (Points)", min_value=10, value=10, step=5)
        # Dynamic photo width controller
        photo_size = st.slider("Adjust Photo Width (px)", min_value=150, max_value=600, value=300, step=10)
    with col_c:
        st.markdown("##### 👤 Bring Player to Block")
        if available_player_options:
            default_idx = 0
            if current_p and current_p["status"] == "Available":
                for idx, opt in enumerate(available_player_options):
                    if opt["id"] == current_p["id"]:
                        default_idx = idx
                        break
            selected_to_bring = st.selectbox(
                "Select Player",
                options=available_player_options,
                index=default_idx,
                format_func=lambda x: f"[{x['id']}] {x['name']} ({x['role']})",
                key="arena_player_selector"
            )
            btn_col1, btn_col2 = st.columns(2)
            with btn_col1:
                if st.button("👉 Bring to Block", use_container_width=True):
                    st.session_state.current_player_id = selected_to_bring["id"]
                    st.session_state.current_bid = base_price_val
                    st.session_state.current_bidder = None
                    st.session_state.bid_history = []
                    save_session_to_file()
                    st.rerun()
            with btn_col2:
                if st.button("🎲 Draw Random", use_container_width=True):
                    drawn_player = random.choice(available_player_options)
                    st.session_state.current_player_id = drawn_player["id"]
                    st.session_state.current_bid = base_price_val
                    st.session_state.current_bidder = None
                    st.session_state.bid_history = []
                    save_session_to_file()
                    st.rerun()
        else:
            st.info("No more players available for bidding!")

    st.markdown("---")
    
    if current_p is None:
        # Suggesting drawing or selecting a player
        st.info("No player currently on the bidding block! Select a player from the dropdown above or click 'Draw Random'.")
        if not available_player_options:
            st.success("🎉 All players have been auctioned! Check out the Team Rosters tab for final squad details.")
    else:
        # Display the active bidding workspace
        col_profile, col_bidding = st.columns([1.2, 1])
        
        # 1. Left: Player Profile Card
        with col_profile:
            st.markdown(f"""
            <div class='player-card'>
                <div class='player-name'>{current_p['name']}</div>
                <div class='player-role'>{current_p['role']}</div>
                <div class='player-stat'><strong>ID:</strong> {current_p['id']}</div>
                <div class='player-stat'><strong>Department:</strong> {current_p['department']} ({current_p['course']})</div>
                <div class='player-stat'><strong>Batting Style:</strong> {current_p['batting_style']} Handed</div>
                <div class='player-stat'><strong>Bowling:</strong> {current_p['bowling_hand']} Hand - {current_p['bowling_style']}</div>
                <div class='player-stat'><strong>Wicket Keeper:</strong> {current_p['wicket_keeper']}</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Display Photo inside Streamlit directly if available, else a placeholder
            if current_p['photo_direct']:
                try:
                    # Fallback support
                    st.image(current_p['photo_direct'], caption=f"Profile of {current_p['name']}", width=photo_size)
                except Exception:
                    # If GDrive loading fails or direct link blocks, show standard text link or generic image
                    st.warning("Could not render Direct Drive Photo. View via standard URL:")
                    st.markdown(f"[🔗 View Player Registration Photo]({current_p['photo_url']})")
            elif current_p['photo_url']:
                st.markdown(f"[🔗 View Player Registration Photo]({current_p['photo_url']})")
                
            # Remarks
            if current_p['remarks']:
                st.markdown(f"""
                <div class='remarks-box'>
                    <strong>Remarks:</strong> {current_p['remarks']}
                </div>
                """, unsafe_allow_html=True)
                
        # 2. Right: Bidding Control Interface
        with col_bidding:
            st.markdown("### 🔨 Bid Desk")
            
            # Display active high bid
            if st.session_state.current_bidder:
                st.markdown(f"""
                <div style='background-color: #1b263b; border: 2px solid #52b788; border-radius: 10px; padding: 15px; text-align: center; margin-bottom: 20px;'>
                    <h4 style='color: #52b788; margin: 0;'>CURRENT HIGH BID</h4>
                    <p style='font-size: 2.5rem; font-weight: 900; margin: 5px 0; color: #ffffff;'>{st.session_state.current_bid} Points</p>
                    <p style='font-size: 1.2rem; margin: 0; color: #a2d2ff;'>by <strong>{st.session_state.current_bidder}</strong></p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style='background-color: #1b263b; border: 2px dashed #e0a96d; border-radius: 10px; padding: 15px; text-align: center; margin-bottom: 20px;'>
                    <h4 style='color: #e0a96d; margin: 0;'>BASE PRICE</h4>
                    <p style='font-size: 2.5rem; font-weight: 900; margin: 5px 0; color: #ffffff;'>{st.session_state.current_bid} Points</p>
                    <p style='font-size: 1.1rem; margin: 0; color: #b0c4de;'>Waiting for opening bid...</p>
                </div>
                """, unsafe_allow_html=True)
                
            # Quick Bidding Panel
            st.markdown("#### Raise Bid Amount")
            col_inc1, col_inc2, col_inc3, col_inc4 = st.columns(4)
            with col_inc1:
                if st.button("+5 pts", use_container_width=True):
                    st.session_state.current_bid += 5
                    st.rerun()
            with col_inc2:
                if st.button("+10 pts", use_container_width=True):
                    st.session_state.current_bid += 10
                    st.rerun()
            with col_inc3:
                if st.button("+25 pts", use_container_width=True):
                    st.session_state.current_bid += 25
                    st.rerun()
            with col_inc4:
                if st.button("+50 pts", use_container_width=True):
                    st.session_state.current_bid += 50
                    st.rerun()
                    
            # Custom Bid value input and Bidder Team
            st.markdown("---")
            bid_col1, bid_col2 = st.columns([1.5, 1])
            with bid_col1:
                bidder_team = st.selectbox(
                    "Selecting Bidding Team",
                    options=list(st.session_state.teams.keys()),
                    index=0
                )
            with bid_col2:
                custom_bid_price = st.number_input(
                    "Set Bid Price",
                    min_value=int(st.session_state.current_bid),
                    max_value=1000,
                    value=int(st.session_state.current_bid),
                    step=5
                )
                
            # Place Custom Bid Button
            if st.button("⚡ Place Bid", use_container_width=True, type="secondary"):
                # Validate team budget
                team_budget = st.session_state.teams[bidder_team]["budget"]
                team_spent = st.session_state.teams[bidder_team]["spent"]
                remaining = team_budget - team_spent
                
                if custom_bid_price > remaining:
                    st.error(f"🚨 Invalid Bid! {bidder_team} only has {remaining} points left.")
                else:
                    st.session_state.current_bid = custom_bid_price
                    st.session_state.current_bidder = bidder_team
                    st.session_state.bid_history.append({
                        "team": bidder_team,
                        "bid": custom_bid_price,
                        "timestamp": pd.Timestamp.now().strftime("%H:%M:%S")
                    })
                    st.success(f"Bid of {custom_bid_price} pts placed for {bidder_team}!")
                    st.rerun()
                    
            # SOLD & UNSOLD Controls
            st.markdown("---")
            action_col1, action_col2 = st.columns(2)
            with action_col1:
                # SOLD Button
                sold_enabled = st.session_state.current_bidder is not None
                if st.button("🤝 SOLD", type="primary", use_container_width=True, disabled=not sold_enabled):
                    buyer = st.session_state.current_bidder
                    price = st.session_state.current_bid
                    
                    # Store history for undo
                    undo_state = {
                        "action": "sold",
                        "player_id": current_p["id"],
                        "team": buyer,
                        "price": price
                    }
                    st.session_state.history_log.append(undo_state)
                    
                    # Update team roster and spending
                    st.session_state.teams[buyer]["spent"] += price
                    st.session_state.teams[buyer]["players"].append({
                        "id": current_p["id"],
                        "name": current_p["name"],
                        "role": current_p["role"],
                        "price": price
                    })
                    
                    # Update player status
                    for p in st.session_state.players:
                        if p["id"] == current_p["id"]:
                            p["status"] = "Sold"
                            p["sold_team"] = buyer
                            p["sold_price"] = price
                            
                    log_action(f"SOLD: {current_p['name']} ({current_p['role']}) to {buyer} for {price} points.")
                    st.success(f"🎉 SOLD! {current_p['name']} is bought by {buyer} for {price} pts!")
                    
                    # Move on
                    st.session_state.current_player_id = None
                    st.session_state.current_bidder = None
                    st.session_state.bid_history = []
                    save_session_to_file()
                    st.rerun()
                    
            with action_col2:
                # UNSOLD Button
                if st.button("❌ UNSOLD / PASS", use_container_width=True):
                    # Store history for undo
                    undo_state = {
                        "action": "unsold",
                        "player_id": current_p["id"],
                        "team": None,
                        "price": 0
                    }
                    st.session_state.history_log.append(undo_state)
                    
                    # Update player status
                    for p in st.session_state.players:
                        if p["id"] == current_p["id"]:
                            p["status"] = "Unsold"
                            
                    log_action(f"PASSED: {current_p['name']} ({current_p['role']}) went unsold.")
                    st.warning(f"{current_p['name']} marked as Unsold.")
                    
                    # Move on
                    st.session_state.current_player_id = None
                    st.session_state.current_bidder = None
                    st.session_state.bid_history = []
                    save_session_to_file()
                    st.rerun()
                    
            # Undo button
            if st.session_state.history_log:
                last_act = st.session_state.history_log[-1]
                p_obj = next((x for x in st.session_state.players if x["id"] == last_act["player_id"]), None)
                p_name = p_obj["name"] if p_obj else last_act["player_id"]
                if st.button(f"↩️ Undo Last Sale / Action ({p_name})", use_container_width=True):
                    # Pop history
                    last_action = st.session_state.history_log.pop()
                    p_id = last_action["player_id"]
                    
                    # Revert status
                    for p in st.session_state.players:
                        if p["id"] == p_id:
                            p["status"] = "Available"
                            p["sold_team"] = None
                            p["sold_price"] = 0
                            
                    if last_action["action"] == "sold":
                        t_name = last_action["team"]
                        p_price = last_action["price"]
                        
                        # Revert team squad
                        st.session_state.teams[t_name]["spent"] -= p_price
                        st.session_state.teams[t_name]["players"] = [
                            item for item in st.session_state.teams[t_name]["players"] if item["id"] != p_id
                        ]
                        
                    log_action(f"UNDO: Reverted auction result for player ID {p_id}.")
                    st.info(f"Reverted results for {p_name}. Placed back in the available list!")
                    
                    # Set as current player
                    st.session_state.current_player_id = p_id
                    st.session_state.current_bid = base_price_val
                    st.session_state.current_bidder = None
                    st.session_state.bid_history = []
                    save_session_to_file()
                    st.rerun()

            # Bid history for active player
            if st.session_state.bid_history:
                st.markdown("#### Bidding History")
                for bid_item in reversed(st.session_state.bid_history):
                    st.text(f"[{bid_item['timestamp']}] {bid_item['team']}: {bid_item['bid']} Points")

# ----------------------------------------
# TAB 2: TEAM ROSTERS & BUDGETS
# ----------------------------------------
with tab_rosters:
    st.markdown("### 📋 Team Squads Leaderboard")
    
    # Calculate leaderboard data
    leaderboard = []
    for t_name, t_data in st.session_state.teams.items():
        players_list = t_data["players"]
        batters_cnt = sum(1 for p in players_list if p["role"] == "Batter")
        bowlers_cnt = sum(1 for p in players_list if p["role"] == "Bowler")
        allrounders_cnt = sum(1 for p in players_list if p["role"] == "All-rounder")
        
        # Check wicketkeeper
        wk_cnt = 0
        for pl_bought in players_list:
            full_p = next((x for x in st.session_state.players if x["id"] == pl_bought["id"]), None)
            if full_p and full_p["wicket_keeper"] == "Yes":
                wk_cnt += 1
                
        leaderboard.append({
            "Team Name": t_name,
            "Total Budget (Pts)": t_data["budget"],
            "Budget Spent": t_data["spent"],
            "Remaining Budget": t_data["budget"] - t_data["spent"],
            "Squad Count": len(players_list),
            "Batters": batters_cnt,
            "Bowlers": bowlers_cnt,
            "All-Rounders": allrounders_cnt,
            "Wicket-Keepers": wk_cnt
        })
        
    lead_df = pd.DataFrame(leaderboard)
    st.dataframe(lead_df, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    st.markdown("### 👥 Detailed Roster View")
    
    # Grid of teams
    cols = st.columns(2)
    for idx, (t_name, t_data) in enumerate(st.session_state.teams.items()):
        col_idx = idx % 2
        with cols[col_idx]:
            with st.expander(f"💼 {t_name} (Squad: {len(t_data['players'])} | Rem: {t_data['budget'] - t_data['spent']} pts)", expanded=True):
                if t_data["players"]:
                    roster_df = pd.DataFrame(t_data["players"])
                    roster_df.columns = ["ID", "Player Name", "Role", "Buy Price (Pts)"]
                    st.dataframe(roster_df, use_container_width=True, hide_index=True)
                else:
                    st.info("No players purchased yet.")

# ----------------------------------------
# TAB 3: PLAYER REGISTRY & SEARCH
# ----------------------------------------
with tab_registry:
    st.markdown("### 🔍 Filter and Browse Player Registrations")
    
    # Filtering UI
    filter_col1, filter_col2, filter_col3 = st.columns(3)
    with filter_col1:
        search_q = st.text_input("Search Player by Name", value="")
    with filter_col2:
        role_filter = st.selectbox("Filter by Role", options=["All Roles", "Batter", "Bowler", "All-rounder"])
    with filter_col3:
        status_filter = st.selectbox("Filter by Auction Status", options=["All Statuses", "Available", "Sold", "Unsold"])
        
    # Build list of filtered players
    filtered_players = []
    for p in st.session_state.players:
        # Filter logic
        if search_q and search_q.lower() not in p["name"].lower():
            continue
        if role_filter != "All Roles" and p["role"] != role_filter:
            continue
        if status_filter != "All Statuses" and p["status"] != status_filter:
            continue
            
        filtered_players.append({
            "ID": p["id"],
            "Name": p["name"],
            "Role": p["role"],
            "Department": p["department"],
            "Course": p["course"],
            "Batting": p["batting_style"],
            "Bowling Hand": p["bowling_hand"],
            "Bowling Style": p["bowling_style"],
            "WK": p["wicket_keeper"],
            "Status": p["status"],
            "Bought By": p["sold_team"] if p["sold_team"] else "N/A",
            "Price": p["sold_price"] if p["status"] == "Sold" else 0,
            "Remarks": p["remarks"]
        })
        
    st.markdown(f"**Found {len(filtered_players)} matching players**")
    f_df = pd.DataFrame(filtered_players)
    st.dataframe(f_df, use_container_width=True, hide_index=True)
    
    # Admin Manual Override panel
    st.markdown("---")
    with st.expander("🛠️ Admin Override / Database Controls (Edit Player Status Manually)"):
        st.warning("Use this section only to correct mistakes or manually force a transaction.")
        override_col1, override_col2, override_col3 = st.columns(3)
        with override_col1:
            p_to_override = st.selectbox(
                "Select Player to Modify", 
                options=st.session_state.players,
                format_func=lambda x: f"[{x['id']}] {x['name']} ({x['role']}) - Status: {x['status']}"
            )
        with override_col2:
            new_status = st.selectbox("Set Status To", options=["Available", "Sold", "Unsold"])
            new_team = st.selectbox("Assign to Team (only for Sold)", options=[None] + list(st.session_state.teams.keys()))
        with override_col3:
            new_price = st.number_input("Set Price (only for Sold)", min_value=0, max_value=1000, value=20, step=5)
            
        if st.button("Apply Manual Override", type="primary", use_container_width=True):
            p_id = p_to_override["id"]
            orig_status = p_to_override["status"]
            orig_team = p_to_override["sold_team"]
            orig_price = p_to_override["sold_price"]
            
            # Revert any previous team associations first
            if orig_status == "Sold" and orig_team:
                st.session_state.teams[orig_team]["spent"] -= orig_price
                st.session_state.teams[orig_team]["players"] = [
                    item for item in st.session_state.teams[orig_team]["players"] if item["id"] != p_id
                ]
                
            # Apply new values
            for p in st.session_state.players:
                if p["id"] == p_id:
                    p["status"] = new_status
                    if new_status == "Sold" and new_team:
                        p["sold_team"] = new_team
                        p["sold_price"] = new_price
                        
                        # Add to new team
                        st.session_state.teams[new_team]["spent"] += new_price
                        st.session_state.teams[new_team]["players"].append({
                            "id": p_id,
                            "name": p["name"],
                            "role": p["role"],
                            "price": new_price
                        })
                    else:
                        p["sold_team"] = None
                        p["sold_price"] = 0
                        
            log_action(f"MANUAL OVERRIDE: Modified Player {p_to_override['name']} (ID {p_id}) to {new_status} (Team: {new_team}, Price: {new_price} pts).")
            st.success(f"Successfully modified database state for {p_to_override['name']}!")
            save_session_to_file()
            st.rerun()

# ----------------------------------------
# TAB 4: SPENDING ANALYTICS
# ----------------------------------------
with tab_analytics:
    st.markdown("### 📊 Live Auction Spend Visualization")
    
    if sold_players > 0:
        # Create visual charts
        analytics_df = pd.DataFrame(leaderboard)
        
        # Spent vs Remaining chart
        st.markdown("#### Budget Utilization by Team")
        chart_data = pd.DataFrame({
            "Remaining Budget": analytics_df["Remaining Budget"].values,
            "Spent Budget": analytics_df["Budget Spent"].values
        }, index=analytics_df["Team Name"].values)
        st.bar_chart(chart_data, height=400, color=["#52b788", "#d90429"])
        
        # Squad Roles breakdown
        st.markdown("#### Team Squad Composition")
        squad_comp = pd.DataFrame({
            "Batters": analytics_df["Batters"].values,
            "Bowlers": analytics_df["Bowlers"].values,
            "All-Rounders": analytics_df["All-Rounders"].values
        }, index=analytics_df["Team Name"].values)
        st.bar_chart(squad_comp, height=400, color=["#e0a96d", "#415a77", "#a2d2ff"])
        
        # High buys
        sold_list = [p for p in st.session_state.players if p["status"] == "Sold"]
        if sold_list:
            st.markdown("#### 🏆 Top Purchases of the Auction")
            sorted_sold = sorted(sold_list, key=lambda x: x["sold_price"], reverse=True)
            top_buys = [{
                "Player Name": p["name"],
                "Role": p["role"],
                "Department": p["department"],
                "Bought By": p["sold_team"],
                "Buy Price": p["sold_price"]
            } for p in sorted_sold[:10]]
            st.dataframe(pd.DataFrame(top_buys), use_container_width=True, hide_index=True)
    else:
        st.info("No players sold yet. Once bidding starts, beautiful live visualizations and spending analytics will populate here!")

# ----------------------------------------
# TAB 5: TRANSACTION LOG
# ----------------------------------------
with tab_logs:
    st.markdown("### 📝 Live Auction Event Log")
    if st.session_state.transaction_log:
        for idx, log_item in enumerate(reversed(st.session_state.transaction_log)):
            st.text(f"[{log_item['timestamp']}] {log_item['description']}")
    else:
        st.info("The auction has not started yet. Bidding events and player transactions will log here in real-time.")
