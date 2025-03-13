
import os
import requests

# Stampa i valori delle variabili di ambiente
print("TELEGRAM_CHAT_ID:", os.getenv('TELEGRAM_CHAT_ID'))
print("TELEGRAM_BOT_TOKEN:", os.getenv('TELEGRAM_BOT_TOKEN'))
print("FOOTBALL_DATA_API_KEY:", os.getenv('FOOTBALL_DATA_API_KEY'))

# Codice esistente...
import os
import json
import logging
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup
import pytz
import re

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def fetch_raiplay_schedule():
    """Fetch football matches from RaiPlay guide"""
    try:
        url = "https://www.raiplay.it/guidatv"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        programs = []
        
        # Find program cards for RAI 1 and RAI 2
        for channel in ['Rai 1', 'Rai 2']:
            channel_section = soup.find('section', {'data-channel': channel})
            if channel_section:
                for program in channel_section.find_all('li', class_='program'):
                    title = program.find('h3', class_='program-title')
                    time = program.find('p', class_='program-time')
                    
                    if title and time:
                        title_text = title.text.strip()
                        time_text = time.text.strip()
                        
                        # Check if it's a football program
                        if any(keyword in title_text.lower() 
                              for keyword in ['calcio', 'serie a', 'champions', 'europa', 'coppa italia']):
                            
                            programs.append({
                                'channel': channel.upper(),
                                'time': time_text,
                                'program': title_text,
                                'description': 'Diretta su ' + channel
                            })
        
        return programs
    except Exception as e:
        logging.error(f"Error fetching RaiPlay schedule: {e}")
        return []

def fetch_mediaset_schedule():
    """Fetch football matches from Mediaset guide"""
    try:
        url = "https://www.mediaset.it/guidatv"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        programs = []
        
        # Find program listings for Canale 5 and Italia 1
        channels = {
            'Canale 5': 'CANALE 5',
            'Italia 1': 'ITALIA 1'
        }
        
        for channel_name, channel_id in channels.items():
            channel_section = soup.find('div', {'data-channel': channel_id})
            if channel_section:
                for program in channel_section.find_all('div', class_='program'):
                    title = program.find('h3', class_='program-title')
                    time = program.find('span', class_='time')
                    
                    if title and time:
                        title_text = title.text.strip()
                        time_text = time.text.strip()
                        
                        # Check if it's a football program
                        if any(keyword in title_text.lower() 
                              for keyword in ['calcio', 'serie a', 'champions', 'europa', 'coppa italia']):
                            
                            programs.append({
                                'channel': channel_name,
                                'time': time_text,
                                'program': title_text,
                                'description': 'Diretta su ' + channel_name
                            })
        
        return programs
    except Exception as e:
        logging.error(f"Error fetching Mediaset schedule: {e}")
        return []

def fetch_sky_sport_schedule():
    """Fetch football matches from Sky Sport guide"""
    try:
        # Using Sky Sport's football section which shows today's matches
        url = "https://sport.sky.it/calcio"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        programs = []
        
        # Find today's matches section
        matches_section = soup.find('div', class_='matches-today')
        if matches_section:
            for match in matches_section.find_all('div', class_='match'):
                time = match.find('span', class_='match-time')
                teams = match.find('div', class_='match-teams')
                competition = match.find('div', class_='match-competition')
                
                if time and teams:
                    time_text = time.text.strip()
                    teams_text = teams.text.strip()
                    competition_text = competition.text.strip() if competition else ''
                    
                    programs.append({
                        'channel': 'Sky Sport',
                        'time': time_text,
                        'program': f"{competition_text}: {teams_text}",
                        'description': 'Diretta su Sky Sport'
                    })
        
        return programs
    except Exception as e:
        logging.error(f"Error fetching Sky Sport schedule: {e}")
        return []

def fetch_dazn_schedule():
    """Fetch football matches from DAZN"""
    try:
        # Since DAZN requires authentication, we'll use their public schedule page
        url = "https://www.dazn.com/it-IT/news/calcio"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        programs = []
        
        # Find today's matches section (this is a simplified version as DAZN's actual structure might be different)
        matches_section = soup.find('section', class_='today-matches')
        if matches_section:
            for match in matches_section.find_all('div', class_='match-card'):
                time = match.find('span', class_='match-time')
                teams = match.find('div', class_='match-teams')
                competition = match.find('div', class_='competition')
                
                if time and teams:
                    time_text = time.text.strip()
                    teams_text = teams.text.strip()
                    competition_text = competition.text.strip() if competition else ''
                    
                    programs.append({
                        'channel': 'DAZN',
                        'time': time_text,
                        'program': f"{competition_text}: {teams_text}",
                        'description': 'In streaming su DAZN'
                    })
        
        return programs
    except Exception as e:
        logging.error(f"Error fetching DAZN schedule: {e}")
        return []

def update_tv_schedule():
    """Update the TV schedule data"""
    schedule = {}
    
    # Fetch RAI schedules
    rai_programs = fetch_raiplay_schedule()
    for program in rai_programs:
        channel = program['channel']
        if channel not in schedule:
            schedule[channel] = []
        schedule[channel].append(program)
    
    # Fetch Mediaset schedules
    mediaset_programs = fetch_mediaset_schedule()
    for program in mediaset_programs:
        channel = program['channel']
        if channel not in schedule:
            schedule[channel] = []
        schedule[channel].append(program)
    
    # Fetch Sky Sport schedule
    sky_programs = fetch_sky_sport_schedule()
    if sky_programs:
        schedule['Sky Sport'] = sky_programs
    
    # Fetch DAZN schedule
    dazn_programs = fetch_dazn_schedule()
    if dazn_programs:
        schedule['DAZN'] = dazn_programs
    
    # Sort programs by time for each channel
    for channel in schedule:
        schedule[channel].sort(key=lambda x: x['time'])
    
    # Save the schedule
    with open('tv_schedule.json', 'w', encoding='utf-8') as f:
        json.dump(schedule, f, ensure_ascii=False, indent=2)
    
    logging.info("TV schedule updated successfully")
    return schedule

if __name__ == "__main__":
    update_tv_schedule()
