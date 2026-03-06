import feedparser
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# 1. 예쁜 뉴스레터(HTML) 만들기
def get_news_html():
    keywords = ['뮤지컬 캐스팅', '공연 마케팅', '대학로 연극']
    
    # 이메일 디자인 (HTML)
    html = """
    <html>
    <body style="font-family: 'Apple SD Gothic Neo', sans-serif; background-color: #f4f4f4; padding: 20px;">
        <div style="max-width: 600px; margin: 0 auto; background-color: #ffffff; padding: 30px; border-radius: 15px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
            <h2 style="color: #2c3e50; border-bottom: 3px solid #e67e22; padding-bottom: 15px; text-align: center;">
                🎭 오늘의 공연 마케팅 리포트
            </h2>
            <p style="text-align: right; color: #666; font-size: 12px;">""" + datetime.now().strftime('%Y년 %m월 %d일') + """</p>
    """

    for keyword in keywords:
        encoded = keyword.replace(" ", "%20")
        url = f"https://news.google.com/rss/search?q={encoded}&hl=ko&gl=KR&ceid=KR:ko"
        feed = feedparser.parse(url)
        
        # 키워드 제목
        html += f"""
        <div style="margin-top: 30px; margin-bottom: 15px;">
            <span style="background-color: #2c3e50; color: #ffffff; padding: 8px 15px; border-radius: 20px; font-weight: bold; font-size: 14px;">
                # {keyword}
            </span>
        </div>
        """

        if not feed.entries:
            html += "<div style='color: #999; padding: 10px;'>새로운 소식이 없습니다.</div>"
        
        # 뉴스 리스트 (카드 형태)
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

# 2. 이메일 보내기
def send_email():
    sender = os.environ['MY_EMAIL']
    password = os.environ['MY_PASSWORD']
    receiver = sender

    # 메일 제목 설정
    subject = f"📢 {datetime.now().strftime('%m/%d')} 공연 뉴스 브리핑 도착!"
    
    # 메일 내용 설정 (HTML 방식)
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = receiver
    
    html_content = get_news_html()
    part = MIMEText(html_content, 'html')
    msg.attach(part)

    # 전송
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender, password)
        server.send_message(msg)
        server.quit()
        print("✅ 이메일 전송 성공!")
    except Exception as e:
        print(f"❌ 이메일 전송 실패: {e}")

# 3. 실행
if __name__ == "__main__":
    send_email()
