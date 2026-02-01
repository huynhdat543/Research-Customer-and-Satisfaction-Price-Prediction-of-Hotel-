import numpy as np
import time
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import pandas as pd
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from urllib.parse import urlparse, parse_qs
from datetime import datetime, timedelta
import os


# Tạo đối tượng Service với đường dẫn đến chromedriver
service = Service('C:/Users/PC/Documents/WebDriver/chromedriver.exe')

# Khởi tạo trình duyệt với Service
driver = webdriver.Chrome(service=service)

# Hàm cuộn trang xuống cuối trang
def scroll_to_bottom():
    last_height = driver.execute_script('return document.body.scrollHeight')
    while True: 
        # Cuộn xuống cuối
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        sleep(2)  # chờ trang load
        
        new_height = driver.execute_script('return document.body.scrollHeight')
        if new_height == last_height:
            break
        last_height = new_height

# Hàm cuộn trang nhẹ
def scroll_down_gently():
    pixels = 200
    driver.execute_script(f'window.scrollBy(0, {pixels});')
    sleep(1)

# Hàm bấm vào nút tải thêm cho đến khi không còn dữ liệu
def click_to_gen_all():
    click_count = 0
    while True:
        try:
            # Cuộn xuống cuối trang
            scroll_to_bottom()
            gen_more = driver.find_element(By.XPATH, '//button[.//span[contains(text(), "Tải thêm kết quả")]]')
            gen_more.click()
            print(f'[{click_count+1}] Đã bấm "Tải thêm kết quả"...')
            sleep(4)
            click_count += 1
        except NoSuchElementException:
            print("Không tìm thấy nút 'Tải thêm kết quả'.")
            print('Hết dữ liệu để tải thêm.')
            break
        except ElementClickInterceptedException:
            print('Không thể click vào nút. Có thể bị che hoặc lỗi layout.')
            break

# Hàm bấm vào nút tải thêm (đầu vào là số lần bấm tối đa)
def click_to_gen(max_clicks: int):
    click_count = 0
    while click_count < max_clicks:
        try:
            scroll_to_bottom()
            gen_more = driver.find_element(By.XPATH, '//button[.//span[contains(text(), "Tải thêm kết quả")]]')
            gen_more.click()
            print(f'[{click_count+1}] Đã bấm "Tải thêm kết quả"...')
            sleep(4)
            click_count += 1
        except NoSuchElementException:
            print("Không tìm thấy nút 'Tải thêm kết quả'.")
            break
        except ElementClickInterceptedException:
            print('Không thể click vào nút. Có thể bị che hoặc lỗi layout.')
            break

# Hàm reset lại ChromeDriver
def reset_driver():
    global driver
    try:
        driver.quit()
        sleep(np.random.uniform(1, 1.5))
        driver = webdriver.Chrome(service=service)
        print('\nDriver đã được reset thành công.')
    except:
        print('\nĐã xảy ra lỗi khi reset driver')
        driver = webdriver.Chrome(service=service)  # Khởi tạo lại driver mặc định trong trường hợp lỗi.
        print('Khởi tạo lại driver mới.')
    return driver

def return_none_crawl_in_1Hotel():
    df = pd.DataFrame([{
        "view_to_beach": None,
        "view_to_city": None,
        "view_to_mountain": None,
        "view_to_river": None,
        "eaves": None,
        "pool": None,
        "parking": None,
        "tourist_spot": None,
        "eat_drink_spot": None,
        "beachs": None,
        "staff": None,
        "convenient": None,
        "clean": None,
        "comfort": None,
        "worthwhile": None,
        "destination": None,
        "distance_to_airport": None,
        "airport_shuttle": None
    }])
    return df

# Hàm crawl thông tin chi tiết trong trang khách sạn (đầu vào là url đến trang khách sạn)
def crawl_in_1Hotel(url: str):
    global driver
    # Kiểm tra driver có còn sống không
    try:
        _ = driver.title
    except:
        print("Driver không còn hoạt động. Đang reset lại...")
        reset_driver()
    retry1 = 0
    while retry1 < 3:
        try:
            driver.get(url)
            scroll_down_gently()
            #time.sleep(np.random.uniform(0.8, 1))
            sleep(1)
            
            break
        except:
            print('Lỗi truy cập link hotel!')
            retry1 += 1
            if retry1 < 3:
                print(f'Đang thử truy cập lần {retry1} vào link hotel')
                reset_driver()
                #sleep(1)
            else:
                print('Không thể truy cập link hotel')
    if retry1 >= 3:
        return return_none_crawl_in_1Hotel()
    
    # tiện ích tổng quát nhất
    try:
        highlight_div = driver.find_element(By.CSS_SELECTOR, '.property_hightlights_wrapper')
    except NoSuchElementException:
        highlight_div = None

    def check_icon(selector):
        if not highlight_div:
            return 0
        try:
            highlight_div.find_element(By.CSS_SELECTOR, selector)
            return 1
        except NoSuchElementException:
            return 0

    view_to_beach = check_icon('svg.bk-icon.-streamline-sea_view')
    view_to_city = check_icon('svg.bk-icon.-streamline-city')
    view_to_mountain = check_icon('svg.bk-icon.-streamline-mountains')
    view_to_river = check_icon('svg.bk-icon.-streamline-lake_view')
    eaves = check_icon('svg.bk-icon.-streamline-resort')
    pool = check_icon('svg.bk-icon.-streamline-pool')
    if pool==0:
        try:
            div = driver.find_element(By.CSS_SELECTOR, '[data-testid="property-most-popular-facilities-wrapper"]')
            spans = div.find_elements(By.TAG_NAME, 'span')
            for span in spans:
                if ("hồ" in span.text) or ("bơi" in span.text):
                    pool = 1 
                    break
        except:
            pass
    parking = check_icon('svg.bk-icon.-streamline-parking_sign.ph-icon')
    
    # xe đưa đón sân bay
    airport_shuttle = 0
    try:
        div = driver.find_element(By.CSS_SELECTOR, '[data-testid="property-most-popular-facilities-wrapper"]')
        #spans = div.find_elements(By.TAG_NAME, 'span')
        spans = div.find_elements(By.CSS_SELECTOR, 'span.f6b6d2a959')
        for span in spans:
            if ("đưa" in span.text) or ("đón" in span.text):
                airport_shuttle = 1
                break
    except NoSuchElementException:
        pass

    conv_block = driver.find_elements(By.CSS_SELECTOR, '.d208d2153d')
    len_block = len(conv_block)
    
    # số lượng địa điểm tham quan
    tourist_spot = 0
    try:
        One = conv_block[0].find_element(By.CSS_SELECTOR, '.e9f7361569.a735063bc6.a0cf1e6d94.b049f18dec')
        tourist_spot += len(One.find_elements(By.TAG_NAME, 'li'))
    except NoSuchElementException:
        pass
    if len_block >= 5:
        try:
            Three = conv_block[2].find_element(By.CSS_SELECTOR, '.e9f7361569.a735063bc6.a0cf1e6d94.b049f18dec')
            tourist_spot += len(Three.find_elements(By.TAG_NAME, 'li'))
            if len_block > 5:
                Four = conv_block[3].find_element(By.CSS_SELECTOR, '.e9f7361569.a735063bc6.a0cf1e6d94.b049f18dec')
                tourist_spot += len(Four.find_elements(By.TAG_NAME, 'li'))
        except NoSuchElementException:
            pass
    
    #  số lượng địa điểm ăn uống
    eat_drink_spot = 0
    try:
        Two = conv_block[1].find_element(By.CSS_SELECTOR, '.e9f7361569.a735063bc6.a0cf1e6d94.b049f18dec')
        eat_drink_spot += len(Two.find_elements(By.TAG_NAME, 'li'))
    except NoSuchElementException:
        pass
    
    # số bãi biển lân cận
    beachs_num = 0
    try:
        content1 = conv_block[len_block-2].find_element(By.CSS_SELECTOR, '.e7addce19e.f546354b44.cc045b173b').text
        content2 = conv_block[len_block-3].find_element(By.CSS_SELECTOR, '.e7addce19e.f546354b44.cc045b173b').text
        if ("bãi" in content1) and ("biển" in content1):
            beach = conv_block[len_block-2].find_element(By.CSS_SELECTOR, '.e9f7361569.a735063bc6.a0cf1e6d94.b049f18dec')
            beachs_num += len(beach.find_elements(By.TAG_NAME, 'li'))
        elif ("bãi" in content2) and ("biển" in content2):
            beach = conv_block[len_block-3].find_element(By.CSS_SELECTOR, '.e9f7361569.a735063bc6.a0cf1e6d94.b049f18dec')
            beachs_num += len(beach.find_elements(By.TAG_NAME, 'li'))
    except:
        pass
    
    # sân bay
    distance_to_airport = None
    try:
        content = conv_block[len_block-1].find_element(By.CSS_SELECTOR, '.e7addce19e.f546354b44.cc045b173b').text
        if ("sân" in content) and ("bay" in content):
            airport = conv_block[len_block-1].find_element(By.CSS_SELECTOR, '.e9f7361569.a735063bc6.a0cf1e6d94.b049f18dec')
            li_tags = airport.find_elements(By.TAG_NAME, 'li')
            texts = [' - '.join(li.text.splitlines()) for li in li_tags]
            #texts = [li.text for li in li_tags]
            distance_to_airport = '\n'.join(texts) if texts else None
    except:
        pass
    # các điểm đánh giá chi tiết của khách hàng
    point_list = driver.find_elements(By.CSS_SELECTOR, '.afd3558156.ac28d37f07')
    # nhân viên
    try:
        staff = point_list[0].find_element(By.CSS_SELECTOR, '.a9918d47bf.f87e152973').text
    except:
        staff = None
    # tiện nghi
    try:
        convenient = point_list[1].find_element(By.CSS_SELECTOR, '.a9918d47bf.f87e152973').text
    except:
        convenient = None
    # sạch sẽ
    try:
        clean = point_list[2].find_element(By.CSS_SELECTOR, '.a9918d47bf.f87e152973').text
    except:
        clean = None
    # thoải mái
    try:
        comfort = point_list[3].find_element(By.CSS_SELECTOR, '.a9918d47bf.f87e152973').text
    except:
        comfort = None
    # đáng tiền
    try:
        worthwhile = point_list[4].find_element(By.CSS_SELECTOR, '.a9918d47bf.f87e152973').text
    except:
        worthwhile = None
    # địa điểm
    try:
        destination = point_list[5].find_element(By.CSS_SELECTOR, '.a9918d47bf.f87e152973').text
    except:
        destination = None


    df = pd.DataFrame([{
        "view_to_beach": view_to_beach,
        "view_to_city": view_to_city,
        "view_to_mountain": view_to_mountain,
        "view_to_river": view_to_river,
        "eaves": eaves,
        "pool": pool,
        "parking": parking,
        "tourist_spot": tourist_spot,
        "eat_drink_spot": eat_drink_spot,
        "beachs": beachs_num,
        "staff": staff,
        "convenient": convenient,
        "clean": clean,
        "comfort": comfort,
        "worthwhile": worthwhile,
        "destination": destination,
        "distance_to_airport": distance_to_airport,
        "airport_shuttle": airport_shuttle
    }])
    return df

# Hàm crawl trang chứa danh sách các khách sạn của 1 địa điểm (đầu vào là url đến địa điểm)
def crawl_in_1City(url: str):
    # Phân tích URL và lấy query string
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    
    # Lấy các thông số cần
    checkin = query_params.get('checkin', [''])[0]
    checkout = query_params.get('checkout', [''])[0]
    adults = query_params.get('group_adults', [''])[0]
    children = query_params.get('group_children', [''])[0]
    
    try:
        driver.get(url)
        scroll_to_bottom()
    except:
        print('Lỗi không truy cập được link địa điểm bên trong')

    hotel_link = []

    name = []
    address = []
    distance_to_downtown = []
    distance_to_beach = []
    price = []
    taxes = []
    kind = []
    point = []
    eveluate = []
    rates = []
    full_review = []
    star = []
    
    print('Crawling Data...')
    hotel_cards = driver.find_elements(By.CSS_SELECTOR, '[data-testid="property-card-container"]')
    
    for idx, card in enumerate(hotel_cards):
        # Tên khách sạn
        try:
            n = card.find_element(By.CSS_SELECTOR, '[data-testid="title"]').text
            name.append(n)
        except:
            name.append(None)
    
        # Địa chỉ
        try:
            addr = card.find_element(By.CSS_SELECTOR, '[data-testid="address"]').text
            address.append(addr)
        except:
            address.append(None)
    
        # Khoảng cách đến trung tâm thành phố
        try:
            dist = card.find_element(By.CSS_SELECTOR, '[data-testid="distance"]').text
            distance_to_downtown.append(dist)
        except:
            distance_to_downtown.append(None)
            
        # Khoảng cách đến biển
        try:
            dist_beach = card.find_element(By.CSS_SELECTOR,'.fff1944c52.d4d73793a3').text
            distance_to_beach.append(dist_beach)
        except:
            distance_to_beach.append(None)
    
        # Giá
        try:
            pr = card.find_element(By.CSS_SELECTOR, '[data-testid="price-and-discounted-price"]').text
            price.append(pr)
        except:
            price.append(None)
    
        # Thuế và phụ phí
        try:
            tax = card.find_element(By.CSS_SELECTOR, '[data-testid="taxes-and-charges"]').text
            taxes.append(tax)
        except:
            taxes.append(None)
    
        # Loại chỗ nghỉ
        try:
            k = card.find_element(By.CSS_SELECTOR, '.dc7b6a60a4 .fff1944c52.f254df5361').text
            kind.append(k)
        except:
            kind.append(None)
    
        # Điểm, đánh giá, Số lượng đánh giá của khách hàng
        try:
            full_rev = card.find_element(By.CSS_SELECTOR, '[data-testid="review-score"]').text
            full_review.append(full_rev)
            lines = full_rev.split('\n')
            point.append(lines[1] if len(lines) > 1 else None)
            
            if len(lines) > 3:
                eveluate.append(lines[2])
                rates.append(lines[3])
            elif (len(lines) <= 3):
                parts = lines[2].split('·')
                eveluate.append(parts[0] if len(parts) > 0 else None)
                rates.append(parts[1].strip() if len(parts) > 1 else None)
            else:
                eveluate.append(None)
                rates.append(None)
            
            '''pt = card.find_element(By.CSS_SELECTOR,'.a3b8729ab1.d86cee9b25 .ac4a7896c7').text
            point.append(pt)
            point_idx.append(idx+1)'''
        except:
            '''point.append(None)
            point_idx.append(idx+1)'''
            full_review.append(None)
            point.append(None)
            eveluate.append(None)
            rates.append(None)
        
        try:
            stars_container = None
            try:
                stars_container = card.find_element(By.CSS_SELECTOR, '[data-testid="rating-stars"]')
            except:
                stars_container = card.find_element(By.CSS_SELECTOR, '[data-testid="rating-squares"]')
            
            stars = stars_container.find_elements(By.TAG_NAME, 'span')
            star.append(len(stars)) 
        except:
            star.append(None)
               
        try:    
            link = card.find_element(By.CSS_SELECTOR, '[data-testid="property-card-desktop-single-image"]').get_attribute('href')
            hotel_link.append(link)
        except:
            try:
                link = card.find_element(By.CSS_SELECTOR, '[data-testid="title-link"]').get_attribute('href')
            except:
                link = None
            hotel_link.append(link)
    
    df = pd.DataFrame({
        'Name': name,
        'Address': address,
        'Distance_to_DownTown': distance_to_downtown,
        'Distance_to_Beach': distance_to_beach,
        'Price': price,
        'Taxes': taxes,
        'Kind': kind,
        'Point': point,
        'Evaluate': eveluate,
        #'Full_Review': full_review,
        'Stars': star,
        'Rates_Quantity': rates
    })
    print('Crawl Data Outside Completed!')
    
    # Crawl inside (thông tin chi tiết của khách sạn)
    detail_df = []
    for idx, link in enumerate(hotel_link):
        print(f'Crawling data hotel link {idx+1}...')
        retry2 = 0 
        while retry2 < 4:
            try:
                detail_dfs = crawl_in_1Hotel(link)
                detail_df.append(detail_dfs)
                break
            except:
                print(f'Lỗi khi crawl hotel link {idx+1}')
                retry2 += 1
                if retry2 < 4:
                    print(f'Đang thử reset Chrome lần {retry2} để crawl hotel link {idx+1}')
                    reset_driver()
                    sleep(1.4)
                else:
                    print(f'Không thể crawl hotel link {idx+1}')
        if retry2 >= 4:
            detail_df.append(return_none_crawl_in_1Hotel())
            continue
    print('Crawl Data Inside Completed!')
    
    # Gộp DataFrame tổng
    df_full_detail = pd.concat(detail_df, ignore_index=True)
    df = pd.concat([df.reset_index(drop=True), df_full_detail.reset_index(drop=True)], axis=1)
    
    # Thêm thông tin query từ URL vào DataFrame
    df['Adults'] = adults
    df['Children'] = children
    df['Checkin'] = pd.to_datetime(checkin, errors='coerce').strftime('%d/%m/%Y')
    df['Checkout'] = pd.to_datetime(checkout, errors='coerce').strftime('%d/%m/%Y')
    df['Crawl_date'] = datetime.now().strftime('%d/%m/%Y')  # Thêm ngày cào

    
    # Ghi tạm dữ liệu vào file CSV có tên 'temp_result.csv' để tránh mất dữ liệu đã cào do yếu tố khách quan
    if not os.path.exists('temp_result_inside.csv'):
        df.to_csv('temp_result_inside.csv', mode='w', header=True, index=False, encoding='utf-8-sig')
    else:
        df.to_csv('temp_result_inside.csv', mode='a', header=False, index=False, encoding='utf-8-sig')

    print('Crawl Data Completed!')
    return df

# Hàm để tạo danh sách các ngày từ start_date đến end_date
def generate_date_ranges(start_date, end_date):
    # Chuyển đổi ngày tháng thành đối tượng datetime
    start = datetime.strptime(start_date, '%d-%m-%Y')
    end = datetime.strptime(end_date, '%d-%m-%Y')
    
    # Tạo danh sách các ngày trong khoảng từ start_date đến end_date
    date_ranges = []
    current_date = start
    while current_date <= end:
        checkin = current_date.strftime('%Y-%m-%d')
        checkout = (current_date + timedelta(days=1)).strftime('%Y-%m-%d')  # Checkout là ngày kế tiếp
        date_ranges.append((checkin, checkout))
        current_date += timedelta(days=1)
    
    return date_ranges

# Hàm crawl chính (tổng hợp các bước)
def crawl_combination(date_range: range, adults_range: range, children_range: range):
    df = []
    for checkin_date, checkout_date in date_range:
        for adults in adults_range:
            for children in children_range:
                url = f'https://www.booking.com/searchresults.vi.html?ss=Vi%C3%AA%CC%A3t+Nam&ssne=Vi%C3%AA%CC%A3t+Nam&ssne_untouched=Vi%C3%AA%CC%A3t+Nam&label=vi-vn-booking-desktop-AxU5O2rjfNPjsB0NBbA7cAS652796014482%3Apl%3Ata%3Ap1%3Ap2%3Aac%3Aap%3Aneg%3Afi%3Atikwd-370167515186%3Alp9198353%3Ali%3Adec%3Adm&aid=2311236&lang=vi&sb=1&src_elem=sb&src=index&dest_id=230&dest_type=country&checkin={checkin_date}&checkout={checkout_date}&group_adults={adults}&no_rooms=1&group_children={children}&age=9'
                retry = 0
                while retry < 4:
                    try:
                        driver.get(url)
                        scroll_down_gently()
                        #time.sleep(np.random.uniform(0.8, 1))
                        break
                    except:
                        print(f'\nLỗi không thể truy cập được link VietNam ngày {checkin_date} đến {checkout_date}, phòng {adults} người lớn, {children} trẻ em')  
                        retry += 1
                        if retry < 4:
                            print('Đang thử truy cập lần {retry} vào link VietNam ngày {checkin_date} đến {checkout_date}, phòng {adults} người lớn, {children} trẻ em')    
                            reset_driver()
                            sleep(1.5)
                        else:
                            print('Không thể truy cập link VietNam ngày {checkin_date} đến {checkout_date}, phòng {adults} người lớn, {children} trẻ em')
                if retry >= 4:
                    continue
                
                button = driver.find_element(By.XPATH, "//button[.//span[contains(text(), 'Bãi biển')]]")
                button.click()
                time.sleep(np.random.uniform(0.8, 1.2))
                destination_cards = driver.find_elements(By.CSS_SELECTOR, 'a[data-testid="DestinationCard"]')
                link_list = [card.get_attribute('href') for card in destination_cards]

                for i, link in enumerate(link_list):
                    print(f'\nCrawling thành phố {i+1}/{len(link_list)}, ngày {checkin_date} đến {checkout_date}, phòng {adults} người lớn, {children} trẻ em...')
                    retry_count = 0
                    while retry_count < 4:
                        try:
                            df_city = crawl_in_1City(link)
                            df.append(df_city)
                            break
                        except:
                            print(f'Lỗi khi crawl thành phố {i+1}, ngày {checkin_date} đến {checkout_date}, phòng {adults} người lớn, {children} trẻ em')
                            retry_count += 1
                            if retry_count < 4:
                                print(f'Đang thử reset Chrome lần {retry_count} để truy cập link và crawl thành phố {i+1}, ngày {checkin_date} đến {checkout_date}, phòng {adults} người lớn, {children} trẻ em')
                                reset_driver()
                                sleep(1.5)
                            else:
                                print(f'Không thể crawl thành phố {i+1}, ngày {checkin_date} đến {checkout_date}, phòng {adults} người lớn, {children} trẻ em')
                    if retry_count >= 4:
                        continue
                    
            reset_driver()

    # Gộp tất cả các df
    df_final = pd.concat(df, axis=0, ignore_index=True)
    
    if not os.path.exists('data_final_result_inside.csv'):
        df_final.to_csv('data_final_result_inside.csv', mode='w', header=True, index=True, encoding='utf-8-sig')
    else:
        df_old = pd.read_csv('data_final_result_inside.csv', encoding='utf-8-sig')
        df_new = pd.concat([df_old, df_final], axis=0, ignore_index=True)
        df_new.to_csv('data_final_result_inside.csv', mode='w', header=True, index=False, encoding='utf-8-sig')

    return df_final

if __name__ == '__main__':
    # Tạo các giá trị cho tổ hợp người lớn và trẻ em
    adult_range = range(1, 5)  # 1-4 người lớn
    child_range = range(0, 3)  # 0-2 trẻ em

    # Tạo các cặp ngày checkin và checkout
    date_ranges = generate_date_ranges('14-05-2025', '14-08-2025')

    df_final = crawl_combination(date_ranges, adult_range, child_range)
















