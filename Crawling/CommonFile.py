

import os
import re
from datetime import datetime, date, time, timedelta, timezone
import openpyxl
from openpyxl.styles import Alignment


# 버전 체크 테스트
# ============================================================
# 정규표현식 사용 - 더 가벼움
def remove_html_tags_regex(text):

    # 1. HTML 태그 제거
    clean_tags = re.compile('<.*?>')
    text_no_tags = re.sub(clean_tags, '', text)

    # 2. "&quot;" 문자열 제거
    final_clean_text = text_no_tags.replace("&quot;", "")
    return final_clean_text
# ============================================================


# ============================================================
# 날짜 데이터 변경
def data_type_check(pubDate):

    try:
        # 문자열의 마지막 6글자 (' +0900')를 제거
        pub_date_no_tz = pubDate[:-6].strip()
        # datetime 객체로 파싱
        date_obj = datetime.strptime(pub_date_no_tz, "%a, %d %b %Y %H:%M:%S")
    
        # 2. datetime 객체에서 원하는 형식으로 문자열 추출
        # %Y: 4자리 연도 (2025)
        # %m: 2자리 월 (06)
        # %d: 2자리 일 (15)
        formatted_date = date_obj.strftime("%Y%m%d")
    
        # print(f"원본 날짜 문자열: {pub_date_str}")
        # print(f"변환된 날짜: {formatted_date}") # 출력: 20250615
        # print(f"formatted_date의 타입: {type(formatted_date)}") # <class 'str'> 출력

        return formatted_date
    
    except ValueError as e:
        print(f"날짜 문자열 파싱 오류: {e}")
        print("날짜 형식 '%a, %d %b %Y %H:%M:%S +0900'이 정확한지 확인하거나,")
        print("dateutil 라이브러리를 사용해 보세요. (pip install python-dateutil)")
# ============================================================


# ============================================================
# Create Excel File
def create_excel_file(filename, sheetname, datalists, folder_path):

    # Null Check Datalists 
    if not datalists:
        print("No Save Data");
        return

    try:

        # Data 폴더가 없으면 생성
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            print(f"'{folder_path}' 폴더가 생성되었습니다.")


         # 파일 경로 설정
        if not filename.endswith('.xlsx'):
            filename += '.xlsx'
        
        file_path = os.path.join(folder_path, filename)
        print(file_path)
        
        excel_file = openpyxl.Workbook()
        excel_sheet = excel_file.active
    
        # 가운데 정렬 스타일 적용
        center_alignment = Alignment(horizontal='center', vertical='center')
    
        # excel title, width, alignment Set Up 
        # sheet name check
        if not sheetname:
            excel_sheet.title = "네이버 뉴스"
        else:
            excel_sheet.title = sheetname
            
        excel_sheet.column_dimensions['A'].width = 10
        excel_sheet.column_dimensions['B'].width = 80
        excel_sheet.column_dimensions['C'].width = 80
        excel_sheet.column_dimensions['D'].width = 15
    
        # put first row this row title name
        excel_sheet.append(['랭킹', '제목', '링크', '날짜'])
    
        for item in datalists:
            # print(item);
            excel_sheet.append(item)
    
        # Only first row
        for cell in excel_sheet[1]:  
            cell.alignment = center_alignment
    
        print(f"저장 완료: {file_path} ({len(datalists)}개 항목)")
        excel_file.save(file_path)
        excel_file.close()

    except PermissionError:
        print(f"파일 저장 실패: {filename}이 열려있을 수 있습니다.")
    except FileNotFoundError:
        print(f"경로를 찾을 수 없습니다: {filename}")
    except OSError as e:
        print(f"파일 시스템 에러: {e}")        
    except Exception as e:
        print(f"엑셀 저장 에러: {e}")

# ============================================================