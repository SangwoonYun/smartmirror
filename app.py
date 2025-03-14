import re

from datetime import datetime
from bs4 import BeautifulSoup
from flask import Flask, render_template, jsonify
import requests


app = Flask(__name__)

# 한양대학교 웹페이지 URL
HANYANG_BI_URL = "https://www.hanyang.ac.kr/web/www/re15"
HANYANG_SC_URL = "https://www.hanyang.ac.kr/web/www/re11"

def get_meal_bi_info():
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(HANYANG_BI_URL, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        meal_section = soup.select_one("#_foodView_WAR_foodportlet_tab_2 > div.box.tables-board-wrap > table > tbody > tr:nth-child(1)")
        
        if meal_section:
            meal_data = []
            cols = meal_section.find_all("td")
            for col_section in cols[1:-1]:
                col_group = col_section.find_all("li")
                meal_list = [re.sub(r'^\[[^]]+\]\s*', '', col.get_text(strip=True)) for col in col_group]
                meal_data.append(meal_list)
            return meal_data
        else:
            return []
    except Exception as e:
        print("Meal Info Error:", e)
        return []

def get_meal_sc_info():
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(HANYANG_SC_URL, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        meal_section = soup.select_one("#_foodView_WAR_foodportlet_tab_2 > div.box.tables-board-wrap > table > tbody > tr:nth-child(3)")
        
        if meal_section:
            meal_data = []
            cols = meal_section.find_all("td")
            for col_section in cols[1:-1]:
                col_group = col_section.find_all("li")
                meal_list = [re.sub(r'^\[[^]]+\]\s*', '', col.get_text(strip=True)) for col in col_group]
                meal_data.append(meal_list)
            return meal_data
        else:
            return []
    except Exception as e:
        print("Meal Info Error:", e)
        return []

@app.route('/')
def index():
    weekday_dict = {
        0: '월요일',
        1: '화요일',
        2: '수요일',
        3: '목요일',
        4: '금요일',
        5: '토요일',
        6: '일요일'
    }
    meridiem_dict = {
        'AM': '오전',
        'PM': '오후'
    }
    now = datetime.now()
    current_date = f'{now.strftime("%Y년 %-m월 %d일")} {weekday_dict[now.weekday()]}'
    current_time = f'{meridiem_dict[now.strftime("%p")]} {now.strftime("%I:%M:%S")}'

    meal_bi_info = get_meal_bi_info()
    meal_sc_info = get_meal_sc_info()

    return render_template('index.html', date=current_date, time=current_time, meal_bi_info=meal_bi_info, meal_sc_info=meal_sc_info)


@app.route('/api/meal-data')
def meal_data():
    meal_bi_info = get_meal_bi_info()
    meal_sc_info = get_meal_sc_info()
    
    return jsonify({
        "meal_bi_info": meal_bi_info,
        "meal_sc_info": meal_sc_info
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
    
