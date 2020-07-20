import json
class FileHelper():
    def __init__(self):
        self.txt_path = r"res\台科大圖書館_借閱資訊.txt"
        self.json_path = r"res\lib_info.json"
        
    def save_to_txt(self, book_msg):
        try:
            with open(self.txt_path, 'w', encoding="utf-8") as fp:
                fp.write(book_msg)
            print("記事本文件： 台科大圖書館_借閱資訊.txt 儲存成功！\n請至 res 目錄下查看~\n")
        except:
            print("記事本文件： lib_info.txt 儲存失敗\n")
        
    def save_to_json(self, book_info):
        try:
            with open(self.json_path, 'w', encoding="utf-8") as fp:
                json.dump(book_info, fp, indent=2, sort_keys=True, ensure_ascii=False)
            print("json文件： lib_info.json 儲存成功！\n")
        except:
            print("json文件： lib_info.json 儲存失敗\n")
    
    def load_json(self):
        with open(self.json_path, 'r') as fp:
            data = json.load(fp)
        return data # type: list
