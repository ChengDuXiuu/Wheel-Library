# coding=utf-8
import jpush


def sent_message(message):
    # message ="hello jpush"  # 推送内容

    # app_key和master_secret
    app_key = '95d86bb17d4a326289e77e0f'
    master_secret = '3dcde73f0fc65184f6e82971'

    _jpush = jpush.JPush(app_key, master_secret)
    push = _jpush.create_push()
    push.audience = jpush.all_
    push.notification = jpush.notification(alert=message)
    # push.message=jpush.message(msg_content="hello  world jpush!!!",title="jpush消息",)
    push.platform = jpush.all_
    try:
        res = push.send()
    except Exception:
        print( '推送失败')
    return print( '推送成功')

if __name__=="__main__":
    sent_message()