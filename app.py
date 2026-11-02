import streamlit as st
from googleapiclient.discovery import build
import re

# API 키 설정 (스트림릿 클라우드 환경 vs 코랩 로컬 테스트)
try:
    API_KEY = st.secrets["YOUTUBE_API_KEY"]
except:
    from google.colab import userdata
    API_KEY = userdata.get('YOUTUBE_API_KEY')

youtube = build('youtube', 'v3', developerKey=API_KEY)

def get_video_id(url):
    match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", url)
    return match.group(1) if match else None

def search_comments(video_id, keyword):
    comments = []
    # 최대 100개 댓글만 가져오는 기본 설정
    request = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        maxResults=100,
        textFormat="plainText"
    )
    response = request.execute()
    
    for item in response.get("items", []):
        comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
        if keyword in comment:
            comments.append(comment)
    return comments

st.title("유튜브 댓글 키워드 검색기 🔍")

url = st.text_input("유튜브 링크를 넣어줘")
keyword = st.text_input("찾을 단어를 입력해")

if st.button("검색"):
    if url and keyword:
        video_id = get_video_id(url)
        if video_id:
            with st.spinner("댓글 검색 중..."):
                results = search_comments(video_id, keyword)
                if results:
                    st.success(f"'{keyword}' 포함 댓글 {len(results)}개 발견!")
                    for res in results:
                        st.write(f"- {res}")
                else:
                    st.warning("검색된 댓글이 없어.")
        else:
            st.error("잘못된 유튜브 링크야.")
    else:
        st.warning("링크와 검색어를 모두 입력해줘.")
