import feedparser
import smtplib
import os
import random  # <--- 1. 랜덤 도구 추가!
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# 2. 정연 님의 감성을 담은 행운 메시지들
lucky_messages = [
    "🍀 오늘의 행운 컬러는 '위키드 그린'입니다. 초록색 소품을 챙겨보세요!",
    "🎭 오늘의 추천 넘버: 'Defying Gravity' - 중력을 거스르는 하루 보내세요!",
    "🎨 타마라 드 렘피카처럼, 당신의 삶을 예술로 만드는 하루가 되길!",
    "🎫 오늘은 티켓팅 용병운이 좋은 날입니다. 도전해보세요!",
    "☕️ 아메리카노보다는 따뜻한 라떼가 어울리는 날입니다.",
    "✨ 당신은 무대 위 주인공입니다. 어깨 펴고 당당하게!"
]

def get_news_html():
    keywords = ['뮤지컬 캐스팅', '공연 마케팅', '대학로 연극', 'CJ ENM 뮤지컬'] # 경쟁사 키워드도 슬쩍 추가
    
    # 오늘의 운세 뽑기
    today_luck = random.choice(lucky_messages)

    html = """
    <html>
    <body style="font-family: 'Apple SD Gothic Neo', sans-serif; background-color: #f4f4f4; padding: 20px;">
        <div style="max-width: 600px; margin: 0 auto; background-color: #ffffff; padding: 30px; border-radius: 15px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
            <h2 style="color: #2c3e50; border-bottom: 3px solid #e67e22; padding-bottom: 15px; text-align: center;">
                🎭 정연 님의 모닝 브리핑
            </h2>
            <p style="text-align: right; color: #666; font-size: 12px;">""" + datetime.now().strftime('%Y년 %m월 %d일') + """</p>
            
            <div style="background-color: #e8f8f5; padding: 15px; border-radius: 10px; text-align: center; margin-bottom: 30px; border: 1px dashed #1abc9c;">
                <strong>""" + today_luck + """</strong>
            </div>
    """

    for keyword in keywords:
        encoded = keyword.replace(" ", "%20")
        url = f"https://news.google.com/rss/search?q={encoded}&hl=ko&gl=KR&ceid=KR:ko"
        feed = feedparser.parse(url)
        
        html += f"""
        <div style="margin-top: 30px; margin-bottom: 15px;">
            <span style="background-color: #2c3e50; color: #ffffff; padding: 8px 15px; border-radius: 20px; font-weight: bold; font-size: 14px;">
                # {keyword}
            </span>
        </div>
        """

        if not feed.entries:
            html += "<div style='color: #999; padding: 10px;'>새로운 소식이 없습니다.</div>"
        
        for entry in feed.entries[:3]:
            html += f"""
            <div style="background-color: #f9f9f9; padding: 15px; margin-bottom: 10px; border-radius: 8px; border-left: 5px solid #e67e22;">
                <a href="{entry.link}" style="text-decoration: none; color: #333; font-weight: bold; font-size: 16px; display: block; margin-bottom: 5px;">
                    {entry.title}
                </a>
                <a href="{entry.link}" style="color: #e67e22; font-size: 12px; text-decoration: none; font-weight: bold;">
                    👉 기사 원문 보러가기
                </a>
            </div>
            """

    html += """
            <div style="margin-top: 40px; text-align: center; color: #999; font-size: 12px; border-top: 1px solid #eee; padding-top: 20px;">
                이 메일은 GitHub Actions가 매일 아침 자동으로 발송합니다 🤖
            </div>
        </div>
    </body>
    </html>
    """
    return html

# (이메일 보내는 부분은 아까랑 똑같습니다!)
def send_email():
    sender = os.environ['MY_EMAIL']
    password = os.environ['MY_PASSWORD']
    receiver = sender

    subject = f"📢 {datetime.now().strftime('%m/%d')} 공연 뉴스 & 오늘의 운세 도착!"
    
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
