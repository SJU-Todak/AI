from pymongo import MongoClient
from datetime import datetime
from config import load_config

# 🔹 YAML 설정 파일에서 MongoDB URI 불러오기
config = load_config()
mongo_uri = config["mongodb"]["uri"]

# 🔹 MongoDB 연결 및 컬렉션 정의
client = MongoClient(mongo_uri)
db = client['mindAI']

chat_collection = db['chat_logs']           # 상담 대화 로그
user_collection = db['users']               # 사용자 정보
analysis_collection = db['analysis_reports']  # 분석 리포트 저장용

# ✅ 채팅 로그 저장 함수
def save_chat_log(userId, chatId, user_message, bot_response):
    """
    사용자의 메시지와 챗봇의 응답을 채팅 로그에 저장
    """
    chat_collection.update_one(
        {"chatId": chatId, "userId": userId},
        {
            "$push": {
                "messages": {
                    "$each": [user_message, bot_response]
                }
            }
        },
        upsert=True
    )
    print(f"[chat_logs] Chat log saved for chatId={chatId}, userId={userId}")

# ✅ 채팅 로그 불러오기
def get_chat_log(chatId):
    """
    특정 chat_id에 대한 채팅 로그를 불러옴
    """
    chat_doc = chat_collection.find_one({"chatId": chatId})
    if chat_doc:
        return chat_doc.get("messages", [])
    return None

# ✅ 사용자 정보 저장
def save_user_info(userId, name, age, gender):
    """
    사용자 정보를 DB에 저장
    """
    userInfo = {
        "userId": userId,
        "name": name,
        "age": age,
        "gender": gender
    }
    user_collection.update_one(
        {"userId": userId},
        {"$set": userInfo},
        upsert=True
    )
    print(f"[users] User info saved for userId={userId}")

# ✅ 사용자 정보 불러오기
def get_user_info(userId):
    """
    특정 user_id에 대한 사용자 정보를 불러옴
    """
    return user_collection.find_one({"userId": userId})

# ✅ 분석 리포트 저장
def save_analysis_report(report: dict):
    """
    분석 레포트를 analysis_reports 컬렉션에 저장
    """
    report["timestamp"] = datetime.now().isoformat()
    analysis_collection.insert_one(report)
    print(f"[analysis_reports] Report saved for chatId={report.get('chatId')}, userId={report.get('userId')}")
