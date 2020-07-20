from apscheduler.schedulers.blocking import BlockingScheduler 
import datetime
import time
from module.NTUST_lib_crawler import NTUST_lib_crawler
from module.file_helper import FileHelper

class AutoBorrower():
    def __init__(self):
        """ 依序運行主爬蟲程序: 自動登入 => 獲取借閱資訊 => 存檔 """
        self.crawler = NTUST_lib_crawler(False)
        print("1-1.")
        self.crawler.NTUST_lib_crawling()
        
        fileHelper = FileHelper()
        self.book_list = fileHelper.load_json()
        #print(self.book_list) # list already sorted by due_time
    
    def get_dueTimes(self):
        dueTimes = [info["due_time"] for info in self.book_list]
        tmpDueTimes = sorted(list(set(dueTimes)))
        return tmpDueTimes
    
    def auto_borrow(self, specific_date):
        print("2-3.", end='')
        self.crawler.auto_borrowing(specific_date)
        
    def scheduling(self):
        dueTimes = self.get_dueTimes()
        #  scheduler = BlockingScheduler()
        # 設定: 自動續借資訊
        ########################
        HH = 12; MM = 0; SS = 0   # 中午12點整
        ########################
        for dueTime in dueTimes:
            # 設定: run_date
            date = dueTime.split("-")
            year = int(f"20{date[0]}"); month = int(date[1])
            '''
            run_day = day - 1  # 續借日期為到期日的前一天
            run_dt = datetime.datetime(year, month, run_day, hour=HH, minute=MM, second=SS)
            '''
            # print(f"年/月/日:{year}/{month}/{day}")
            #scheduler.add_job(self.auto_borrow(dt), 'date', run_date=dt, args=[])
            #scheduler.start()
            print("2-1.開始自動續借\n")
            time.sleep(1)
            print(f"2-2.續借書目之應還日期： {dueTime}\n")
            self.auto_borrow(dueTime)
            
            print(f"2-6.完成應還日期為：{dueTime}\n之所有圖書的自動續借流程")
            print("="*30, end="\n\n")
    
if __name__ == "__main__":
    '''
    # 測試: 自動登入 => 獲取借閱資訊 => 存檔
    borrower = AutoBorrower()
    tidy_book_list = borrower.get_tidy_lists()
    print(tidy_book_list)
    '''
    # ----------------------------------------------------
    '''
    # 測試: 自動勾選指定日期的借閱紀錄並續借
    crawler = NTUST_lib_crawler(False)
    crawler.auto_borrowing("20-08-05")
    '''
    # ----------------------------------------------------
    # 測試: 返回所有借閱不重覆的到期日
    '''
    borrower = AutoBorrower()
    dueTimes = borrower.get_dueTimes()
    #print(dueTimes)
    '''
    # ----------------------------------------------------
    # 測試：(1) 圖書借閱資訊爬蟲/儲存
    # 　　　(2) 自動借閱(按'否'離開,僅測試功能)
    borrower = AutoBorrower()
    borrower.scheduling()
    
    
