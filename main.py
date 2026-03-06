import feedparser
import smtplib
import os
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# ==========================================
# [기능 1] 🎰 무한 뮤지컬 운세 데이터
# ==========================================
adjectives = [
    "고음을 찌르는", "웅장한 오케스트라 같은", "재즈풍의 시카고 같은", 
    "아르데코 스타일의", "락 스피릿 넘치는", "신비로운", "치명적인 매력의", 
    "앙상블처럼 조화로운", "커튼콜 박수처럼 뜨거운", "인터미션 없이 달리는",
    "지킬처럼 이중적인", "혁명가 앙졸라 같은", "자유로운 보헤미안 같은"
]

characters = [
    "엘파바", "글린다", "타마라", "라파엘라", "죽음(토드)", "지킬 앤 하이드", 
    "장발장", "팬텀", "롤라", "록시 하트", "모차르트", "스위니 토드",
    "마리 앙투아네트", "드라큘라"
]

items = [
    "오페라 글라스", "1열 중앙석 티켓", "프로그램 북", "캐스팅 보드 인증샷", 
    "할인 쿠폰", "티켓 봉투", "초록색 마법 물약", "붉은색 립스틱", 
    "반짝이는 킹키부츠", "따뜻한 유자차", "배우 퇴근길 선물"
]

actions = [
    "피켓팅에 성공하여 1열을 잡으세요!", "관크 없는 클린한 하루를 보내세요.", 
    "레전드 회차를 갱신하는 하루 되세요.", "인터미션 때 화장실 1등으로 가세요!", 
    "퇴근길에서 최애 배우와 눈이 마주칠 거예요.", "오늘 부르는 노래가 3단 고음으로!", 
    "MD 부스 줄이 기적처럼 짧을 거예요.", "취소표를 줍는(취줍) 행운이 따를 거예요!"
]

def get_musical_luck():
    adj = random.choice(adjectives)
    char = random.choice(characters)
    item = random.choice(items)
    act = random.choice(actions)
    
    # 디자인: 황금 티켓 스타일
    luck_msg = f"""
    <div style='color: #5c4033; font-weight: bold; font-size: 16px; margin-bottom: 5px;'>✨ 오늘의 컨셉: {adj} {char}</div>
    <div style='color: #333; font-size: 15px;'>
        행운템 <b>[{item}]</b>(와)과 함께,<br>
        <span style='background-color: #fff; padding: 2px 8px; border-radius: 10px; color: #d35400; font-weight: bold;'>{act}</span>
    </div>
    """
    return luck_msg

# ==========================================
# [기능 2] 디자인된 뉴스레터 만들기 (HTML)
# ==========================================
def get_news_html():
    my_keywords = ['뮤지컬 캐스팅', '공연 마케팅', '대학로 연극']
    competitor_keywords = ['오디컴퍼니', 'EMK뮤지컬컴퍼니', '신시컴퍼니', 'CJ ENM 뮤지컬', '롯데컬처웍스']
    alert_words = ['티켓', '오픈', '캐스팅', '라인업', '공개', '선예매']
    today_luck = get_musical_luck()

    # 전체 배경 및 헤더 (미드나잇 블루 & 골드 테마)
    html = """
    <html>
    <body style="margin:0; padding:0; background-color: #f4f4f4; font-family: 'Apple SD Gothic Neo', 'Malgun Gothic', sans-serif;">
        <div style="max-width: 600px; margin: 0 auto; background-color: #ffffff; overflow: hidden; box-shadow: 0 10px 20px rgba(0,0,0,0.05);">
            
            <div style="background-color: #16213e; padding: 40px 20px; text-align: center;">
                <h1 style="color: #c5a059; margin: 0; font-size: 24px; letter-spacing: 2px; border-bottom: 2px solid #c5a059; display: inline-block; padding-bottom: 10px;">
                    PLAYBILL
                </h1>
                <p style="color: #ffffff; margin-top: 15px; font-size: 16px; font-weight: 300;">
                    정연 님의 모닝 브리핑
                </p>
                <p style="color: #7f8fa6; font-size: 12px; margin: 0;">""" + datetime.now().strftime('%Y.%m.%d %A') + """</p>
            </div>
            
            <div style="padding: 30px 20px;">
            
                <div style="background: linear-gradient(135deg, #fdfbf1 0%, #f1eacc 100%); border: 1px solid #e0d0a0; border-radius: 12px; padding: 20px; text-align: center; margin-bottom: 40px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); position: relative;">
                    <div style="position: absolute; top: -10px; left: 50%; transform: translateX(-50%); background-color: #c5a059; color: white; padding: 4px 15px; border-radius: 20px; font-size: 12px; font-weight: bold;">LUCKY TICKET</div>
                    """ + today_luck + """
                </div>
    """

    # --- 함수: 뉴스 섹션 만들기 ---
    def make_news_section(title, keywords_list, icon):
        section_html = f"""
        <div style="margin-bottom: 40px;">
            <h3 style="color: #16213e; font-size: 18px; border-left: 4px solid #c5a059; padding-left: 12px; margin-bottom: 20px;">
                {icon} {title}
            </h3>
        """
        
        for keyword in keywords_list:
            encoded = keyword.replace(" ", "%20")
            url = f"https://news.google.com/rss/search?q={encoded}&hl=ko&gl=KR&ceid=KR:ko"
            feed = feedparser.parse(url)
            
            if not feed.entries: continue # 기사 없으면 생략
            
            section_html += f"""
            <div style="margin-bottom: 25px;">
                <div style="background-color: #f1f2f6; color: #57606f; font-size: 12px; font-weight: bold; padding: 4px 10px; border-radius: 4px; display: inline-block; margin-bottom: 8px;">
                    # {keyword}
                </div>
            """
            
            for entry in feed.entries[:3]:
                title_text = entry.title
                title_color = "#2f3542"
                bg_color = "#ffffff"
                border_style = "1px solid #eee"
                badge = ""
                
                # 🚨 알림 키워드 강조 (빨간 테두리 + 뱃지)
                for alert in alert_words:
                    if alert in title_text:
                        title_color = "#d63031" # 빨간 글씨
                        bg_color = "#fff0f0" # 연한 빨간 배경
                        border_style = "1px solid #ffcccc"
                        badge = "<span style='color:red; font-size:10px; border:1px solid red; border-radius:3px; padding:1px 3px; margin-right:5px;'>HOT</span>"
                        break
                
                section_html += f"""
                <a href="{entry.link}" style="display: block; text-decoration: none; background-color: {bg_color}; border: {border_style}; padding: 15px; border-radius: 8px; margin-bottom: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.03);">
                    <div style="color: {title_color}; font-size: 15px; font-weight: bold; line-height: 1.4;">
                        {badge}{title_text}
                    </div>
                    <div style="color: #a4b0be; font-size: 11px; margin-top: 8px; text-align: right;">
                        기사 원문 보기 ›
                    </div>
                </a>
                """
            section_html += "</div>"
        section_html += "</div>"
        return section_html

    # 섹션 조립
    html += make_news_section("오늘의 헤드라인", my_keywords, "🔥")
    html += make_news_section("경쟁사 브리핑", competitor_keywords, "🕵️‍♀️")

    # 푸터
    html += """
                <div style="text-align: center; margin-top: 50px; padding-top: 20px; border-top: 1px solid #eee; color: #bdc3c7; font-size: 11px;">
                    Designed by Jeong-yeon | Powered by GitHub Actions
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    return html

# 이메일 전송 함수 (기존과 동일)
def send_email():
    sender = os.environ['MY_EMAIL']
    password = os.environ['MY_PASSWORD']
    receiver = sender

    subject = f"🎟️ {datetime.now().strftime('%m/%d')} 뮤지컬 모닝 브리핑 (Premium Ver.)"
    
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = receiver
    
    html_content = get_news_html()
    part = MIMEText(html_content, 'html')
    msg.attach(part)

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender, password)
        server.send_message(msg)
        server.quit()
        print("✅ 이메일 전송 성공!")
    except Exception as e:
        print(f"❌ 이메일 전송 실패: {e}")

if __name__ == "__main__":
    send_email()
