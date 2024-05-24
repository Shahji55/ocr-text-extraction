from google.cloud import vision
import re

def detect_text(path):
    """Detects text in the file."""
    
    client = vision.ImageAnnotatorClient()

    with open(path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.text_detection(image=image)

    # json_response = MessageToJson(response._pb)

    # # save response_json as a .json file
    # with open('response.json', 'w') as json_file:
    #     json_file.write(json_response)
        
    texts = response.text_annotations

    texts = texts[0].description
    texts = texts.split('\n')
    print(texts)

    text_list = []
    for text in texts:
        print("text: ", text)
        text_list.append(text)
        #print(". ", text.description)
        #text_list.append(text.description)
        #print(f'\n"{text.description}"')
        
    if response.error.message:
        raise Exception(
            "{}\nFor more info on error messages, check: "
            "https://cloud.google.com/apis/design/errors".format(response.error.message)
        )
    
    return text_list

def prepare_data(text_list):

    card_data = {}
    card_number = ""
    card_expiry = ""
    card_cvv_number = ""
    #full_name = ""

    # 04/27
    card_expiry_re1 = "^(0[1-9]|1[0-2])\/([0-9]{2})$"

    # (GOOD|Good|VALID|Valid|THRU|Thru) 04/27
    card_expiry_re2 = "^(GOOD|Good|VALID|Valid|THRU|Thru) (0[1-9]|1[0-2])\/([0-9]{2})$"

    # 5156 7699 4462 6689
    card_number_re = "^([0-9]{4}) ([0-9]{4}) ([0-9]{4}) ([0-9]{4})$"

    # 630
    cvv_number_re = "^[0-9]{3}$"

    try:
        for i, text in enumerate(text_list):

            #print(text)

            # Extract card number
            if len(text) == 19 and " " in text:
                c_num = re.match(card_number_re, text)
                #print(c_num)

                if c_num is not None:
                    card_number = c_num.group()
                    print(card_number)
                    card_data['card_number'] = card_number

            # Extract card expiry
            exp_date = re.match(card_expiry_re1, text)
            #print(exp_date, type(exp_date))

            if exp_date is not None:
                card_expiry = exp_date.group()
                print(card_expiry)
                card_data['card_expiry'] = card_expiry

            else:
                exp_date = re.match(card_expiry_re2, text)
                #print(exp_date, type(exp_date))

                if exp_date is not None:
                    data = exp_date.group()
                    data = data.split(" ")
                    if len(data) == 2:
                        card_expiry = data[1]
                        print(card_expiry)
                        card_data['card_expiry'] = card_expiry

            '''
            if "GOOD" in text or "Good" in text or "VALID" in text or "Valid" in text:
                print("Good|Valid found")
                if "THRU" in text_list[i+1] or "Thru" in text_list[i+1]:
                    print("Thru found")
                    #exp_date = re.findall(expiry_re, text_list[i+1])
                    if len(text_list[i+2]) == 5:
                        exp_date = re.match(card_expiry_re, text_list[i+2])
                        #print(exp_date, type(exp_date))

                        if exp_date is not None:
                            print("0")
                            card_expiry = exp_date.group()
                            print(card_expiry)
                            card_data['card_expiry'] = card_expiry
            '''

            # Extract card cvv number
            if len(text) == 3:
                cvv_num = re.match(cvv_number_re, text)
                #print(cvv_num)

                if cvv_num is not None:
                    card_cvv_number = cvv_num.group()
                    print(card_cvv_number)
                    card_data['card_cvv'] = card_cvv_number


    except Exception as e:
        print(str(e))

    dict_keys = ['card_number', 'card_expiry', 'card_cvv']
    
    for key in dict_keys:
        if key not in card_data:
            #print("Setting key empty: ", key)
            card_data[key] = ""

    return card_data

if __name__ == "__main__":
    # image_path = "1-1.jpeg"
    #image_path = "1-2.jpeg"
    #image_path = "2-1.jpeg"
    # image_path = "2-2.jpeg"

    #image_path = "3-1.jpg"
    image_path = "3-2.jpg"
    #image_path = "4-1.jpg"
    #image_path = "4-2.jpg"

    #image_path = "5-1.jpg"
    #image_path = "6-1.png"

    text_list = detect_text(image_path)

    print("\nText list: ", text_list)
    print("\n")

    card_data = prepare_data(text_list)

    print("\nCard data: ", card_data)