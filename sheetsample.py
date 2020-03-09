import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time
from datetime import datetime


def setData(TYPE):
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']

    # 認証情報設定
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        'line-sample-sheet-a57309179265.json', scope)

    # OAuth2の資格情報を使用してGoogleAPIにログイン
    gc = gspread.authorize(credentials)
    time.sleep(1)
    # 共有設定したスプレッドシートキーを変数[SPREADSHEET_KEY]に格納する。
    SPREADSHEET_KEY = '1NsffW_m8PkfyJ1fp3ILfcPT8NHGP_RE3f8bkCR6bk2c'

    # wkss := worksheets
    wkss = gc.open_by_key(SPREADSHEET_KEY)
    time.sleep(1)
    wkss_list = wkss.worksheets()
    wks_1 = wkss_list[0]  # sheet1
    wks_2 = wkss_list[1]  # sheet2
    wks_3 = wkss_list[2]  # sheet3

    pre_t = datetime.now().strftime("%H:%M")
    if TYPE == 1:
        return wks_1.cell(2, 1).value
    elif TYPE = 2:
        return wks_1.cell(2, 1).value
    elif TYPE = 3:
        return wks_1.cell(2, 1).value
    elif TYPE = 4:
        return wks_1.cell(2, 1).value
    else:
        return '該当の情報がありません。もう一度お試しください'


'''
以下SHEET生成プログラム
'''
# sheet2でリンクを生成
# for i in range(2, 10):
#     t = '=IMPORTXML(A$2,' + 'C' + str(i) + ')'
#     wks_2.update_cell(i, 4, t)

# セルの空白判定
# i = 2
# while (len(wks_2.cell(i, 6).value) != 0):
#     print(wks_2.cell(i, 6).value)
#     i += 1
# base_url = '"' + wks_2.cell(3, 6).value + '"'

# 土曜運行
# for j in range(1, 30):
#     # 八王子みなみ野行
#     tx = '"//*[@id=' + "'main-wrapper'" + ']/div/div/div/table[1]/tbody/tr[' + \
#         str(j) + ']"'
#     t = '=IMPORTXML(' + base_url + ',' + tx + ')'
#     wks_1.update_cell(j, '1', t)
#
#     # 八王子行
#     tx = '"//*[@id=' + "'main-wrapper'" + ']/div/div/div/table[2]/tbody/tr[' + \
#         str(j) + ']"'
#     t = '=IMPORTXML(' + base_url + ',' + tx + ')'
#     wks_1.update_cell(j, '6', t)

# 平日運行
# base_url = '"' + wks_2.cell(2, 6).value + '"'
# for j in range(1, 60):
#     tx = '"//*[@id=' + "'main-wrapper'" + ']/div/div/div/table[1]/tbody/tr[' + \
#         str(j) + ']"'
#     t = '=IMPORTXML(' + base_url + ',' + tx + ')'
#     wks_3.update_cell(j, '1', t)
#
#     # 八王子行
#     tx = '"//*[@id=' + "'main-wrapper'" + ']/div/div/div/table[2]/tbody/tr[' + \
#         str(j) + ']"'
#     t = '=IMPORTXML(' + base_url + ',' + tx + ')'
#     wks_3.update_cell(j, '6', t)
