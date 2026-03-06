import feedparser
import smtplib
import os
from email.mime.text import MIMEText
from datetime import datetime

# 1. 뉴스 가져오기 함수
def get_news():
    keywords = ['뮤지컬 캐스팅', '공연 마케팅', '대학로 연극'] # 키워드 수정 가능
    news_content = f"🎭 {datetime.now().strftime('%Y-%m-%d')} 공연 뉴스 요약\n\n"
    
    for keyword in keywords:
        encoded = keyword.replace(" ", "%20")
        url = f"https://news.google.com/rss/search?q={encoded}&hl=ko&gl=KR&ceid=KR:ko"
        feed = feedparser.parse(url)
        
        news_content += f"[{keyword}]\n"
        if not feed.entries:
            news_content += "  - 새로운 소식이 없습니다.\n"
        
        for entry in feed.entries[:3]: # 3개씩만
            news_content += f"  - {entry.title}\n    ({entry.link})\n"
        news_content += "\n"
    
    return news_content

# 2. 이메일 보내기 함수
def send_email(subject, content):
    sender = os.environ['MY_EMAIL']    # 깃허브 비밀금고에서 꺼내씀
    password = os.environ['MY_PASSWORD'] # 깃허브 비밀금고에서 꺼내씀
    receiver = sender # 나에게 보내기

    msg = MIMEText(content)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = receiver

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
    news_text = get_news()
    print(news_text) # 로그 확인용
    send_email("📢 오늘의 공연 뉴스 도착!", news_text)
