""" 台科圖書館館藏借閱_自動爬蟲程式 """
from selenium import webdriver as wd
from selenium.webdriver.chrome.options import Options
import time
from module.NTUST_lib_cfg_reader import read_cfg
from module.file_helper import FileHelper

class Webdriver():
    def get_webdriver(self, headless):
        chrome_options = Options()
        if headless == True:
            chrome_options.add_argument("--headless")
            #chrome_options.headless = True # also works
        wd_path = r"D:\geckodriver\chromedriver.exe"
        driver = wd.Chrome(wd_path, options=chrome_options)
        driver.implicitly_wait(10)
        return driver
        
class NTUST_lib_crawler():
    """ 初始化webdriver """
    def __init__(self, headless=True):
        webdriver = Webdriver()
        self.driver = webdriver.get_webdriver(headless)
        
    """ 依序運行主爬蟲程序: 自動登入 => 獲取借閱資訊 => 存檔 """
    def NTUST_lib_crawling(self):
        self.auto_login_NTUST_lib()
        self.scrapy_bookInfo()
        
    """ 自動登入台科圖書館網頁 """
    def auto_login_NTUST_lib(self):
        """ Get the login info """
        lib_account, lib_pwd = read_cfg()
        #print(f"lib_account: {lib_account}")
        #print(f"lib_pwd: {lib_pwd}")
        
        """ Automatically login NTUST library with login info """
        print("請稍等，正在自動登入台科圖書館網站...")
        self.driver.get("https://sierra.lib.ntust.edu.tw/patroninfo*cht")
        self.driver.find_element_by_name("code").send_keys(lib_account)
        self.driver.find_element_by_name("pin").send_keys(lib_pwd)
        
        btnLogin = self.driver.find_element_by_class_name("submitHidden")
        time.sleep(0.5)
        btnLogin.click()
        print("登入成功！")
        
    """ 自動續借符合 '指定日期' 的所有書目 """
    def auto_borrowing(self, specific_date):
        self.auto_login_NTUST_lib() # 先登入
        print("2-4.等待畫面載入")
        time.sleep(3)
        
        # checkBoxes | xpath: "//*[@class='patFuncMark']"
        checkBoxes = self.driver.find_elements_by_xpath("//*[@class='patFuncMark']/input")
        # 狀態(借閱期限)(預設已排序) | xpath:"//*[@class='patFuncStatus']"
        dueTimes = self.driver.find_elements_by_class_name("patFuncStatus")
        
        specific_date = f"到期 {specific_date}"
        for i in range(len(checkBoxes)):
            if dueTimes[i].text == specific_date:
                #print(f"{i+1} ok\n")
                checkBox = checkBoxes[i]#.find_element_by_xpath("//input")
                checkBox.click()
                
        # 左側選單 | xpath: "//div[@id='rightSideCont']"
        menu = self.driver.find_element_by_xpath("//div[@id='rightSideCont']")
        # 續借已選館藏按鈕
        btnBorrow = menu.find_elements_by_tag_name("a")[-1]
        btnBorrow.click()
        print("2-5.等待頁面跳轉")
        time.sleep(3)
        
        #print("2-6.完成自動續借流程")
        #print("="*30, end="\n\n")
        
        # //*[@name='renewsome']: 按鈕'是' //*[@name='donothing']: 按鈕'否'
        #btnOk = self.driver.find_element_by_xpath("//*[@name='renewsome']")
        #btnOk.click()
        btnCancel = self.driver.find_element_by_xpath("//*[@name='donothing']")
        btnCancel.click()
        
    def scrapy_bookInfo(self):
        """ 爬蟲 """
        print("1-2.請稍等，正在獲取借閱資訊...")
        # 條碼 | xpath: "//*[@class='patFuncBarcode']"
        barCode = self.driver.find_elements_by_class_name("patFuncBarcode")
        # 狀態(借閱期限)(預設已排序) | xpath:"//*[@class='patFuncStatus']"
        dueTimes = self.driver.find_elements_by_class_name("patFuncStatus")
        # 書名 | xpath:"//*[@class='patFuncTitleMain']"
        title = self.driver.find_elements_by_class_name("patFuncTitleMain")
        print("1-3.借閱資訊獲取成功！\n")
        
        """ 資料清洗 """
        book_count = len(title)
        print(f"1-4.共有 {book_count} 件借閱\n")
        book_info = [] # json
        book_msg = "" # txt
        for i in range(book_count):
            tmpTitle = title[i].text
            tmpDueTime = dueTimes[i].text
            tmpBarCode = barCode[i].text
            book_msg += f"{i+1} {tmpTitle}\n{tmpDueTime}\n\n"
            book_info.append({"bar_code": tmpBarCode, "title":tmpTitle, "due_time":tmpDueTime.split(" ")[-1]})
        #print(book_msg)
        #print(book_info)
        
        """ 存成文字檔，供使用者查看 """
        print("1-5.", end='')
        self.file_storing(data=book_msg, store_type="txt")
        
        """ 存成 json 檔，便於後續處理 """
        print("1-6.", end='')
        self.file_storing(data=book_info, store_type="json")
        
        print("1-7.借閱資訊爬蟲完畢~~~")
        print("="*30, end="\n\n")
        
    def file_storing(self, data, store_type):
        fileHelper = FileHelper()
        if store_type == "txt":
            fileHelper.save_to_txt(data)
        elif store_type == "json":
            fileHelper.save_to_json(data)
            
if __name__ == "__main__":
    """
    crawler = NTUST_lib_crawler()
    crawler.auto_login_NTUST_lib()
    crawler.scrapy_bookInfo()
    """
    crawler = NTUST_lib_crawler()
    crawler.NTUST_lib_crawling()
    
