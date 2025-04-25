from DB import delete_user_info

# 삭제할 user_id를 지정합니다.
user_id_to_delete = "user123"

# 사용자 정보 및 채팅 로그 삭제 함수 호출
delete_user_info(user_id_to_delete)

from DB import delete_chat_log

# 삭제할 chat_id를 지정합니다.
chat_id_to_delete = "chat123"

# 채팅 로그 삭제 함수 호출
delete_chat_log(chat_id_to_delete)