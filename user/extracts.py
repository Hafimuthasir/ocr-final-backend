import re
import os
from passporteye import read_mrz
from datetime import date
from datetime import datetime

def extract_from_licence(text):
    data_list = text.split('\n')
    name = None
    dob = None

    # extract name
    for string in data_list:
        if "Name" in string:
            name_sentance = string
            name = name_sentance.replace("Name", "").strip()
            name = ''.join(char for char in name if char.isalpha() or char.isspace()).strip()

        if "Birth" in string:
            date_regex = r'\d{2}[/\\,-]\d{2}[/\\,-]\d{4}'
            match = re.search(date_regex, string)
            if match:
                dob = match.group()
    return (name, dob)


def extract_name_from_adhaar(text):
    data_list = text.split('\n')
    name_regex = r"[A-Z][a-z]*\s[A-Z][a-z]*"
    name_str = ""

    for i in range(0,len(data_list)-1):
        if "Name" in data_list[i]:
            print('kkkk',data_list)
            name_str = data_list[i+1]
            break
    
    if name_str != "":
        str_match = re.match(name_regex, name_str)
        if str_match :
            matched_name = str_match.group()
            return matched_name
        else : 
            formated_string = name_str.title()
            return formated_string
        
    else:
        for string in data_list:
            str_match = re.match(name_regex, string)
            if str_match:
                matched_name = str_match.group()
                return matched_name
                break
        

def extract_idno_from_adhaar(text):
    data_list = text.split('\n')
    print(data_list)
    id_regex = r"\b\d{4} \d{4} \d{4}\b"
    matched_id=""
    for string in data_list:
        str_match = re.search(id_regex, string)
        if str_match:
            matched_id = str_match.group()
            print(str_match)
            break
    return matched_id


def extract_dob_from_adhaar(text):
    data_list = text.split('\n')
    dob_regex = r""
    dob = ""
    for string in data_list:
        if "Birth" in string or "DOB" in string:
            date_regex = r'\d{2}[/\\,-]\d{2}[/\\,-]\d{4}'
            match = re.search(date_regex, string)
            if match:
                dob = match.group()
    return dob


def extract_data_from_passport(image_file):
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
            
    file_path = os.path.join('uploads', image_file.name)

    with open(file_path, 'wb') as f:
        for chunk in image_file.chunks():
            f.write(chunk)

    try:
        mrz = read_mrz(file_path)
        namers = mrz.names
        # print("rrrrrrrrrrrrr",mrz.names)
        extracted_name = namers.strip().split()[0] + " " + namers.strip().split()[1]

        extracted_id = re.sub('[^A-Za-z0-9]+', '', mrz.number)
        
        # print(mrz.date_of_birth)
        dob = mrz.date_of_birth

        if int(dob[:2]) >= 24:
            year =  "19"+dob[:2]
        else:
            year = "20"+dob[:2]
        month = dob[2:4]
        day = dob[4:6]
        formated_dob = date(year=int(year),month=int(month),day=int(day))
        return extracted_name, extracted_id, formated_dob
    

    except Exception as e:
        print("Error while reading MRZ:", e)
        return "error","error","error"
    
        # return Response({"message":"failed reading the document. Check the document type","status":False},status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
    
        

    