from transitions.extensions import GraphMachine

from utils import send_text_message

money = {}
date = ''
number = ''
memo = ''
class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(
            model=self,
            **machine_configs
        )
    def is_going_to_user(self, event):
        if event.get("message"):
            text = event['message']['text']
            return text.lower() == '..'
        return False
    def is_going_to_delete(self, event):
        if event.get("message"):
            text = event['message']['text']
            return text.lower() == '刪除'
        return False

    def is_going_to_save(self, event):
        if event.get("message"):
            text = event['message']['text']
            return text.lower() == '存檔'
        return False
    def is_going_to_other(self, event):
        if event.get("message"):
            text = event['message']['text']
            return text.lower() == '備忘錄'
        return False
    def is_going_to_load(self, event):
        if event.get("message"):
            text = event['message']['text']
            return text.lower() == '讀檔'
        return False
    def is_going_to_read(self, event):
        if event.get("message"):
            text = event['message']['text']
            return text.lower() != '..' and text.lower() != ''
        return False
    def is_going_to_check(self, event):
        if event.get("message"):
            text = event['message']['text']
            return text.lower() == '確認'
        return False
    def is_going_to_retrun(self, event):
        if event.get("message"):
            text = event['message']['text']
            return text.lower() != '..' and text.lower() != '確認'
        return False
    def is_going_to_data(self, event):
        global date
        if event.get("message"):
            sender_id = event['sender']['id']
            date = event['message']['text']
            flag = str(date) in money
            if(date != '..' and flag == False):
                send_text_message(sender_id, "無此輸入資料\n請輸入日期(MM/DD)")
            return flag
        return False
    def on_enter_user(self, event):
        sender_id = event['sender']['id']
        send_text_message(sender_id, "請選擇存檔或讀檔或刪除或備忘錄")
    def on_enter_save(self, event):
        sender_id = event['sender']['id']
        send_text_message(sender_id, "請輸入日期(MM/DD)")
    def on_enter_readdate(self, event):
        global date
        sender_id = event['sender']['id']
        date = event['message']['text']
        send_text_message(sender_id, "請輸入支出金額")
    def on_enter_readnumber(self, event):
        global number
        sender_id = event['sender']['id']
        number = event['message']['text']
        temp = "%s 支出 %s\n請確認資料無誤"%(date,number)
        send_text_message(sender_id, temp)
    def on_enter_check(self, event):
        sender_id = event['sender']['id']
        money[date] = number
        send_text_message(sender_id, "存檔成功")
        send_text_message(sender_id, "請選擇存檔或讀檔或刪除或備忘錄")
        self.go_to_initial()
    def on_enter_load(self, event):
        sender_id = event['sender']['id']
        temp = "目前紀錄 %s"%(money.keys())
        send_text_message(sender_id, temp)
        send_text_message(sender_id, "請輸入日期(MM/DD)")
    def on_enter_getdata(self, event):
        sender_id = event['sender']['id']
        temp = "%s 支出 %s"%(date,money[date])
        send_text_message(sender_id, temp)
        send_text_message(sender_id, "請選擇存檔或讀檔或刪除或備忘錄")
        self.go_to_initial()
    def on_enter_delete(self, event):
        sender_id = event['sender']['id']
        temp = "目前紀錄 %s"%(money.keys())
        send_text_message(sender_id, temp)
        send_text_message(sender_id, "請輸入日期(MM/DD)")
    def on_enter_deletedata(self, event):
        sender_id = event['sender']['id']
        del money[date]
        send_text_message(sender_id, "刪除成功")
        send_text_message(sender_id, "請選擇存檔或讀檔或刪除或備忘錄")
        self.go_to_initial()
    def on_enter_other(self, event):
        sender_id = event['sender']['id']
        send_text_message(sender_id, "存檔或讀檔")
    def on_enter_domemo(self, event):
        sender_id = event['sender']['id']
        send_text_message(sender_id, "請輸入內容")
    def on_enter_memosave(self, event):
        global memo
        sender_id = event['sender']['id']
        memo = event['message']['text']
        send_text_message(sender_id, "請選擇存檔或讀檔或刪除或備忘錄")
        self.go_to_initial()
    def on_enter_memoload(self, event):
        sender_id = event['sender']['id']
        send_text_message(sender_id, memo)


