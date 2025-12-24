# ================== IMPORT ==================
import time, random, string, re, asyncio, traceback, requests, json, os, base64, subprocess, stat
from io import BytesIO
from datetime import datetime
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

# ================== CONFIG ==================
BOT_TOKEN = "8553180279:AAF40CyLsHirZfeEoAxsaTmLUKX_IbF4Acg"

FIREFOX_BIN = "/data/data/com.termux/files/usr/bin/firefox"
GECKO_PATH  = "/data/data/com.termux/files/usr/bin/geckodriver"
MAIL_API = "https://hunght1890.com/"

# ================== FIX FIREFOX PERMISSIONS ==================
def fix_firefox_permissions():
    """Cấp quyền cho Firefox trên Termux"""
    print("🔧 Đang cấp quyền cho Firefox...")
    
    try:
        # Cấp quyền thực thi
        if os.path.exists(FIREFOX_BIN):
            os.chmod(FIREFOX_BIN, stat.S_IRWXU | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH)
            print(f"✅ Đã cấp quyền cho Firefox")
        
        if os.path.exists(GECKO_PATH):
            os.chmod(GECKO_PATH, stat.S_IRWXU | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH)
            print(f"✅ Đã cấp quyền cho geckodriver")
        
        # Tạo thư mục profile
        profile_dir = "/data/data/com.termux/files/home/.mozilla/firefox"
        os.makedirs(profile_dir, exist_ok=True)
        os.chmod(profile_dir, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
        
        return True
        
    except Exception as e:
        print(f"⚠️ Lỗi cấp quyền: {e}")
        return False

# ================== TÊN VIỆT NAM ==================
HO_NAM = ["Nguyễn", "Trần", "Lê", "Phạm", "Hoàng", "Huỳnh", "Phan", "Vũ", "Võ", "Đặng", "Bùi", "Đỗ", "Hồ", "Ngô", "Dương", "Lý"]
HO_NU = ["Nguyễn", "Trần", "Lê", "Phạm", "Hoàng", "Huỳnh", "Phan", "Vũ", "Võ", "Đặng", "Bùi", "Đỗ", "Hồ", "Ngô", "Dương", "Lý", "Đào", "Mai"]

TEN_DEM_NAM = ["Văn", "Đình", "Minh", "Quang", "Hữu", "Công", "Thanh", "Xuân", "Ngọc", "Đức", "Tiến", "Thành", "Bá", "Gia", "Hoàng", "Anh", "Tuấn", "Hải", "Trung", "Phú"]
TEN_DEM_NU = ["Thị", "Ngọc", "Thu", "Minh", "Thanh", "Hồng", "Kim", "Bích", "Diễm", "Kiều", "Mỹ", "Phương", "Ánh", "Linh", "Khánh", "Như", "Ý", "Huyền", "Thảo", "Quỳnh"]

TEN_NAM = ["An", "Bình", "Bảo", "Cường", "Dũng", "Đạt", "Hải", "Hiếu", "Hoàng", "Huy", "Khải", "Khoa", "Long", "Minh", "Nam", "Phong", "Quang", "Sơn", "Thành", "Trung", "Tuấn", "Việt"]
TEN_NU = ["An", "Anh", "Chi", "Diễm", "Giang", "Hà", "Hân", "Hiền", "Hoa", "Hồng", "Lan", "Linh", "Mai", "My", "Nga", "Ngân", "Nhi", "Phương", "Thảo", "Trang", "Uyên", "Vy", "Yến"]

# ================== PROXY SETTINGS ==================
PROXY_LIST = []
USER_PROXIES = {}
PROXY_FILE = "user_proxies.json"

# ================== AVATAR GIRL URLS ==================
AVATAR_GIRL_URLS = [
    "https://i.pinimg.com/736x/a1/b2/c3/a1b2c3a1b2c3a1b2c3a1b2c3a1b2c3a1.jpg",
    "https://i.pinimg.com/736x/b2/c3/d4/b2c3d4b2c3d4b2c3d4b2c3d4b2c3d4b2.jpg",
    "https://i.pinimg.com/736x/c3/d4/e5/c3d4e5c3d4e5c3d4e5c3d4e5c3d4e5c3.jpg",
    "https://i.pinimg.com/736x/d4/e5/f6/d4e5f6d4e5f6d4e5f6d4e5f6d4e5f6d4.jpg",
    "https://i.pinimg.com/736x/e5/f6/07/e5f607e5f607e5f607e5f607e5f607e5.jpg",
    "https://i.pinimg.com/736x/f6/07/18/f60718f60718f60718f60718f60718f6.jpg",
    "https://i.pinimg.com/736x/07/18/29/07182907182907182907182907182907.jpg",
    "https://i.pinimg.com/736x/18/29/3a/18293a18293a18293a18293a18293a18.jpg",
    "https://i.pinimg.com/736x/29/3a/4b/293a4b293a4b293a4b293a4b293a4b29.jpg",
    "https://i.pinimg.com/736x/3a/4b/5c/3a4b5c3a4b5c3a4b5c3a4b5c3a4b5c3a.jpg",
    "https://i.pinimg.com/736x/4b/5c/6d/4b5c6d4b5c6d4b5c6d4b5c6d4b5c6d4b.jpg",
    "https://i.pinimg.com/736x/5c/6d/7e/5c6d7e5c6d7e5c6d7e5c6d7e5c6d7e5c.jpg",
]

# ================== GLOBAL ==================
USER_LOCK = {}

# ================== LOG ==================
def log(m): print(m, flush=True)
def sep(): log("="*50)

# ================== PROXY MANAGEMENT ==================
def save_proxies():
    try:
        with open(PROXY_FILE, 'w') as f:
            json.dump(USER_PROXIES, f, indent=2)
        log(f"✅ Đã lưu {len(USER_PROXIES)} proxy của người dùng")
    except Exception as e:
        log(f"❌ Lỗi lưu proxy: {e}")

def load_proxies():
    global USER_PROXIES
    try:
        if os.path.exists(PROXY_FILE):
            with open(PROXY_FILE, 'r') as f:
                USER_PROXIES = json.load(f)
            log(f"✅ Đã tải {len(USER_PROXIES)} proxy của người dùng")
    except Exception as e:
        log(f"❌ Lỗi tải proxy: {e}")
        USER_PROXIES = {}

def add_user_proxy(user_id, proxy_str):
    try:
        parts = proxy_str.split(':')
        
        if len(parts) == 2:
            ip, port = parts
            proxy_url = f"http://{ip}:{port}"
            proxy_auth = None
        elif len(parts) == 4:
            ip, port, user, password = parts
            proxy_url = f"http://{ip}:{port}"
            proxy_auth = f"{user}:{password}"
        else:
            return False, "❌ Định dạng proxy không đúng. Dùng: ip:port hoặc ip:port:user:pass"
        
        USER_PROXIES[str(user_id)] = {
            'proxy_url': proxy_url,
            'proxy_auth': proxy_auth,
            'added_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        save_proxies()
        return True, f"✅ Đã thêm proxy: {proxy_url}"
        
    except Exception as e:
        return False, f"❌ Lỗi thêm proxy: {str(e)}"

def remove_user_proxy(user_id):
    try:
        user_id_str = str(user_id)
        if user_id_str in USER_PROXIES:
            removed_proxy = USER_PROXIES.pop(user_id_str)
            save_proxies()
            return True, f"✅ Đã xóa proxy: {removed_proxy.get('proxy_url', 'Unknown')}"
        else:
            return False, "❌ Bạn chưa có proxy nào được thiết lập"
    except Exception as e:
        return False, f"❌ Lỗi xóa proxy: {str(e)}"

def get_user_proxy(user_id):
    user_id_str = str(user_id)
    return USER_PROXIES.get(user_id_str)

# ================== DRIVER WITH PERMISSIONS ==================
def cleanup_profile(profile_dir):
    try:
        # Kill firefox & geckodriver trước
        os.system("pkill -9 firefox >/dev/null 2>&1")
        os.system("pkill -9 geckodriver >/dev/null 2>&1")
        time.sleep(2)

        if os.path.exists(profile_dir):
            import shutil
            shutil.rmtree(profile_dir, ignore_errors=True)

    except Exception as e:
        log(f"⚠️ Cleanup profile lỗi: {e}")
        
def new_driver(user_id):
    """Tạo driver với quyền đầy đủ"""
    # Cấp quyền trước khi tạo driver
    fix_firefox_permissions()
    
    opt = Options()
    opt.binary_location = FIREFOX_BIN
    
    # Thêm options để bypass permission
    opt.add_argument("--headless")
    opt.add_argument("--no-sandbox")
    opt.add_argument("--disable-dev-shm-usage")
    opt.add_argument("--disable-gpu")
    opt.add_argument("--disable-software-rasterizer")
    
    # User agent mới nhất
    opt.set_preference("general.useragent.override", 
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36")
    
    # Cấu hình để bypass proxy permission
    opt.set_preference("network.proxy.type", 0)  # No proxy mặc định
    opt.set_preference("security.fileuri.strict_origin_policy", False)
    opt.set_preference("dom.webdriver.enabled", False)
    opt.set_preference("useAutomationExtension", False)
    
    # Profile tạm
    profile_dir = f"/data/data/com.termux/files/home/temp_profile_{user_id}"
    cleanup_profile(profile_dir)
    os.makedirs(profile_dir, exist_ok=True)
    os.chmod(profile_dir, 0o777)
    # Tạo prefs.js
    prefs_file = os.path.join(profile_dir, "prefs.js")
    prefs_content = '''
user_pref("network.proxy.type", 0);
user_pref("security.fileuri.strict_origin_policy", false);
user_pref("dom.webdriver.enabled", false);
user_pref("useAutomationExtension", false);
user_pref("media.peerconnection.enabled", false);
user_pref("webgl.disabled", true);
user_pref("permissions.default.image", 2);
user_pref("javascript.enabled", true);
user_pref("network.cookie.cookieBehavior", 0);
'''
    
    with open(prefs_file, "w") as f:
        f.write(prefs_content)
    
    # Nếu user có proxy, thêm vào
    user_proxy = get_user_proxy(user_id)
    if user_proxy:
        proxy_url = user_proxy['proxy_url']
        proxy_auth = user_proxy.get('proxy_auth')
        
        log(f"🌐 Sử dụng proxy của user: {proxy_url}")
        
        from urllib.parse import urlparse
        parsed = urlparse(proxy_url)
        host = parsed.hostname
        port = parsed.port or 8080
        
        # Thêm proxy vào prefs
        with open(prefs_file, "a") as f:
            f.write(f'user_pref("network.proxy.type", 1);\n')
            f.write(f'user_pref("network.proxy.http", "{host}");\n')
            f.write(f'user_pref("network.proxy.http_port", {port});\n')
            f.write(f'user_pref("network.proxy.ssl", "{host}");\n')
            f.write(f'user_pref("network.proxy.ssl_port", {port});\n')
            
            if proxy_auth:
                user, password = proxy_auth.split(':')
                f.write(f'user_pref("network.proxy.username", "{user}");\n')
                f.write(f'user_pref("network.proxy.password", "{password}");\n')
    
    opt.add_argument(f"-profile")
    opt.add_argument(profile_dir)
    
    # Tạo driver
    try:
        driver = webdriver.Firefox(
            service=Service(GECKO_PATH),
            options=opt
        )
        
        driver.set_page_load_timeout(40)
        driver.set_script_timeout(30)
        
        # Ẩn automation
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        log("✅ Driver đã được tạo với quyền đầy đủ")
        return driver
        
    except Exception as e:
        log(f"❌ Lỗi tạo driver: {e}")
        raise

# ================== RANDOM NAME ==================
def random_name_gender():
    is_female = random.choice([True, False])
    
    if is_female:
        ho = random.choice(HO_NU)
        ten_dem = random.choice(TEN_DEM_NU) if random.random() > 0.3 else ""
        ten_chinh = random.choice(TEN_NU)
        gender = "Nữ"
        gender_value = "1"
    else:
        ho = random.choice(HO_NAM)
        ten_dem = random.choice(TEN_DEM_NAM) if random.random() > 0.3 else ""
        ten_chinh = random.choice(TEN_NAM)
        gender = "Nam"
        gender_value = "2"
    
    if ten_dem:
        full_name = f"{ho} {ten_dem} {ten_chinh}"
    else:
        full_name = f"{ho} {ten_chinh}"
    
    return ho, ten_chinh, full_name, gender, gender_value

def random_email():
    return f"letien09.{random.randint(100000,999999)}@hunght1890.com"

def random_pass():
    return "@Letien09"# + "".join(random.choices(string.digits, k=4))

def random_avatar():
    return random.choice(AVATAR_GIRL_URLS)

# ================== HUMAN ACTIONS ==================
def human_type(driver, element, text, min_delay=0.08, max_delay=0.25):
    try:
        element.click()
        time.sleep(random.uniform(0.2, 0.5))
        
        for char in text:
            element.send_keys(char)
            delay = random.uniform(min_delay, max_delay)
            if random.random() < 0.2:
                delay = random.uniform(0.05, 0.15)
            time.sleep(delay)
            
            if random.random() < 0.03:
                time.sleep(random.uniform(0.1, 0.3))
                element.send_keys(Keys.BACK_SPACE)
                time.sleep(random.uniform(0.1, 0.2))
                element.send_keys(char)
                time.sleep(random.uniform(0.1, 0.2))
        
        if random.random() < 0.15:
            time.sleep(random.uniform(0.3, 1.0))
            
    except Exception as e:
        try:
            element.clear()
            element.send_keys(text)
        except:
            pass

def human_click(driver, element):
    try:
        element.click()
        time.sleep(random.uniform(0.1, 0.3))
    except:
        pass

# ================== FORM HANDLING ==================
def wait_for_new_form(driver):
    log("🔍 Đang tìm form đăng ký...")
    
    urls_to_try = [
        "https://www.facebook.com/reg/",
        "https://www.facebook.com/r.php",
        "https://m.facebook.com/reg/",
        "https://en-gb.facebook.com/reg/",
    ]
    
    for url in urls_to_try:
        try:
            log(f"🔄 Thử URL: {url}")
            driver.get(url)
            time.sleep(random.uniform(3, 5))
            
            try:
                element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.NAME, "firstname"))
                )
                if element:
                    log(f"✅ Tìm thấy form")
                    return True
            except:
                continue
                    
        except Exception as e:
            continue
    
    log("❌ Không tìm thấy form")
    return False

def find_form_elements(driver):
    elements = {}
    
    field_selectors = {
        'firstname': [(By.NAME, "firstname")],
        'lastname': [(By.NAME, "lastname")],
        'email': [(By.NAME, "reg_email__")],
        'password': [(By.NAME, "reg_passwd__")],
        'birthday_day': [(By.NAME, "birthday_day")],
        'birthday_month': [(By.NAME, "birthday_month")],
        'birthday_year': [(By.NAME, "birthday_year")],
        'gender_male': [(By.XPATH, "//input[@value='2']")],
        'submit': [(By.NAME, "websubmit")],
    }
    
    for field_name, selectors in field_selectors.items():
        for by, selector in selectors:
            try:
                element = driver.find_element(by, selector)
                if element and element.is_displayed():
                    elements[field_name] = element
                    break
            except:
                continue
    
    return elements

def fill_new_form(driver, ho, ten, email, pwd, gender_value, form_elements):
    log("📝 Đang điền form...")
    
    if 'firstname' in form_elements:
        try:
            human_type(driver, form_elements['firstname'], ho)
            time.sleep(random.uniform(0.3, 0.7))
        except:
            pass
    
    if 'lastname' in form_elements:
        try:
            human_type(driver, form_elements['lastname'], ten)
            time.sleep(random.uniform(0.3, 0.7))
        except:
            pass
    
    if 'email' in form_elements:
        try:
            human_type(driver, form_elements['email'], email)
            time.sleep(random.uniform(0.3, 0.7))
        except:
            pass
    
    if 'password' in form_elements:
        try:
            human_type(driver, form_elements['password'], pwd)
            time.sleep(random.uniform(0.3, 0.7))
        except:
            pass
    
    birth_fields = ['birthday_day', 'birthday_month', 'birthday_year']
    birth_values = ['11', '12', '2009']
    
    for i, field in enumerate(birth_fields):
        if field in form_elements:
            try:
                select = Select(form_elements[field])
                select.select_by_value(birth_values[i])
                time.sleep(random.uniform(0.2, 0.4))
            except:
                pass
    
    if 'gender_male' in form_elements:
        try:
            human_click(driver, form_elements['gender_male'])
            time.sleep(random.uniform(0.3, 0.6))
        except:
            pass
    
    if 'submit' in form_elements:
        try:
            human_click(driver, form_elements['submit'])
            log("✅ Đã submit form")
        except:
            pass
    
    return True

# ================== EMAIL VERIFICATION ==================
def get_fb_code(email):
    for _ in range(40):
        try:
            data = requests.get(MAIL_API + email, timeout=10).json()
            if data:
                m = re.search(r"FB-(\d{5,6})", data[0].get("body",""))
                if m:
                    return m.group(1)
                
                m2 = re.search(r"Confirmation code:\s*(\d{5,6})", data[0].get("body",""), re.IGNORECASE)
                if m2:
                    return m2.group(1)
        except:
            pass
        time.sleep(3)
    return None

def find_and_enter_verification_code(driver, code):
    try:
        selectors = [
            (By.NAME, "code"),
            (By.XPATH, "//input[@placeholder='Enter code']"),
        ]
        
        for by, selector in selectors:
            try:
                code_input = driver.find_element(by, selector)
                if code_input.is_displayed():
                    human_type(driver, code_input, code)
                    return True
            except:
                continue
        
        return False
        
    except Exception as e:
        return False

def click_continue_button(driver):
    try:
        continue_texts = ["Continue", "Tiếp tục", "Xác nhận"]
        
        for text in continue_texts:
            try:
                continue_buttons = driver.find_elements(By.XPATH, f"//button[contains(., '{text}')]")
                
                for btn in continue_buttons:
                    try:
                        if btn.is_displayed() and btn.is_enabled():
                            human_click(driver, btn)
                            return True
                    except:
                        continue
            except:
                continue
        
        return False
        
    except Exception as e:
        return False

# ================== CHECKPOINT ==================
def is_checkpoint(driver):
    """Kiểm tra checkpoint"""
    try:
        current_url = driver.current_url.lower()
        page_source = driver.page_source.lower()
        
        checkpoint_keywords = [
            "checkpoint", 
            "security check", 
            "confirm identity",
            "xác minh danh tính"
        ]
        
        for keyword in checkpoint_keywords:
            if keyword in current_url or keyword in page_source:
                log(f"⚠️ Phát hiện checkpoint: {keyword}")
                return True
        
        return False
    except Exception as e:
        log(f"❌ Lỗi kiểm tra checkpoint: {e}")
        return False

# ================== UPLOAD AVATAR ==================
def upload_avatar_to_fb(driver):
    """Upload avatar lên Facebook"""
    try:
        log("🖼️ Đang tìm nút đổi ảnh đại diện...")
        time.sleep(random.uniform(2, 3))
        
        # Thử tìm profile picture
        try:
            profile_pics = driver.find_elements(By.XPATH, 
                "//img[contains(@src, 'profile') or contains(@alt, 'profile')]")
            
            for pic in profile_pics[:2]:
                try:
                    pic.click()
                    time.sleep(2)
                    log("✅ Click vào ảnh profile")
                    break
                except:
                    continue
        except:
            pass
        
        # Tìm input file upload
        time.sleep(2)
        file_inputs = driver.find_elements(By.XPATH, "//input[@type='file']")
        
        if file_inputs:
            log(f"✅ Tìm thấy input file upload")
            
            # Tải ảnh từ URL
            avatar_url = random_avatar()
            log(f"🖼️ Đang tải ảnh từ: {avatar_url}")
            
            response = requests.get(avatar_url, timeout=30, headers={
                'User-Agent': 'Mozilla/5.0'
            })
            
            if response.status_code == 200:
                # Lưu ảnh vào file tạm
                import tempfile
                
                with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmp:
                    tmp.write(response.content)
                    tmp_path = tmp.name
                
                try:
                    # Upload ảnh
                    file_inputs[0].send_keys(tmp_path)
                    log("✅ Đã upload ảnh")
                    time.sleep(random.uniform(3, 5))
                    
                    # Tìm và click nút Save
                    try:
                        save_btn = driver.find_element(By.XPATH,
                            "//button[contains(text(), 'Save') or contains(text(), 'Lưu')]")
                        save_btn.click()
                        time.sleep(random.uniform(5, 8))
                        return True
                    except:
                        pass
                            
                finally:
                    # Xóa file tạm
                    try:
                        os.unlink(tmp_path)
                    except:
                        pass
        
        log("⚠️ Không thể upload avatar")
        return False
        
    except Exception as e:
        log(f"❌ Lỗi upload avatar: {e}")
        return False

# ================== REG ONE ==================
async def reg_one(bot, chat_id, user, idx, total, user_id):
    ho, ten_chinh, full_name, gender, gender_value = random_name_gender()
    email = random_email()
    pwd = random_pass()

    sep()
    log(f"👤 User {user} đang tạo {idx}/{total} acc")
    log(f"📝 Tên: {full_name}")
    log(f"👫 Giới tính: {gender}")
    log(f"📧 Email: {email}")
    log(f"🔑 Pass: {pwd}")
    sep()

    msg = await bot.send_message(
        chat_id,
        f"""👤 `{full_name}`
📧 `{email}`
🔑 `{pwd}`
🌐 Đang khởi tạo...""",
        parse_mode="Markdown"
    )
    status_alive = True

    driver = None
    try:
        driver = new_driver(user_id)
        
        if status_alive:
            await msg.edit_text(f"""👤 `{full_name}`
📧 `{email}`
🔑 `{pwd}`
🔍 Đang tìm form...""", parse_mode="Markdown")
        
        if not wait_for_new_form(driver):
            raise Exception("Không tìm thấy form")
        
        form_elements = find_form_elements(driver)
        
        if not form_elements:
            raise Exception("Không tìm thấy element")
        
        if status_alive:
            await msg.edit_text(f"""👤 `{full_name}`
📧 `{email}`
🔑 `{pwd}`
📝 Đang điền thông tin...""", parse_mode="Markdown")
        
        fill_new_form(driver, ho, ten_chinh, email, pwd, gender_value, form_elements)
        
        wait_time = random.uniform(20, 30)
        log(f"⏳ Chờ {wait_time:.1f} giây...")
        time.sleep(wait_time)

        # ===== KIỂM TRA VÀ NHẬP MÃ XÁC MINH =====
        need_verification = False
        
        try:
            code_selectors = [
                (By.NAME, "code"),
                (By.XPATH, "//input[@placeholder='Enter code']"),
            ]
            
            for by, selector in code_selectors:
                try:
                    driver.find_element(by, selector)
                    need_verification = True
                    break
                except:
                    continue
        except:
            pass
        
        if need_verification:
            if status_alive:
                await msg.edit_text(f"""👤 `{full_name}`
📧 `{email}`
🔑 `{pwd}`
📧 Đang check mail...""", parse_mode="Markdown")

            code = get_fb_code(email)
            if code:
                if status_alive:
                    try:
                        await msg.delete()
                    except:
                        pass
                    status_alive = False

                code_msg = await bot.send_message(
                    chat_id,
                    f"🔢 Mã xác minh\n`{code}`",
                    parse_mode="Markdown"
                )
                await asyncio.sleep(5)
                try:
                    await code_msg.delete()
                except:
                     pass

                # Nhập mã xác minh
                if find_and_enter_verification_code(driver, code):
                    time.sleep(random.uniform(1, 2))
                    
                    # Click Continue
                    if click_continue_button(driver):
                        log("✅ Đã click Continue")
                        
                        # ĐỢI 6 GIÂY SAU KHI CLICK CONTINUE
                        log("⏳ Đợi 8 giây sau khi Continue...")
                        time.sleep(8)
                        
                        # KIỂM TRA CHECKPOINT SAU KHI CONTINUE (TRƯỚC KHI VÀO PROFILE)
                        if is_checkpoint(driver):
                            log(f"❌ Tài khoản {full_name} bị checkpoint sau khi xác minh")
                            
                            # GỬI THÔNG BÁO CHECKPOINT
                            checkpoint_msg = await bot.send_message(
                                chat_id,
                                f"Acc {full_name} Bị Checkpoint"
                            )
                            
                            # XÓA SAU 120 GIÂY
#                            await asyncio.sleep(120)
#                            try:
#                                await checkpoint_msg.delete()
 #                           except:
#                                pass
#                            
#                            if status_alive:
#                                try:
#                                    await msg.delete()
#                                except:
#                                    pass
                            
                            sep()
                            log(f"❌ User {user} tài khoản {idx}/{total} bị checkpoint")
                            sep()
                            return
                        
                        # Tiếp tục chờ thêm
                        time.sleep(random.uniform(10, 15))
                    else:
                        log("⚠️ Không click được Continue")
                else:
                    log("⚠️ Không nhập được mã xác minh")

        # ===== VÀO PROFILE ĐỂ KIỂM TRA CHECKPOINT =====
        if status_alive:
            await msg.edit_text(f"""👤 `{full_name}`
📧 `{email}`
🔑 `{pwd}`
👤 Đang vào trang cá nhân...""", parse_mode="Markdown")

        # VÀO PROFILE
        driver.get("https://m.facebook.com/me")
        time.sleep(random.uniform(5, 8))

        # KIỂM TRA CHECKPOINT SAU KHI VÀO PROFILE
        if is_checkpoint(driver):
            log(f"❌ Tài khoản {full_name} bị checkpoint sau khi vào profile")
            
            # GỬI THÔNG BÁO CHECKPOINT
            checkpoint_msg = await bot.send_message(
                chat_id,
                f"Acc {full_name} Bị Checkpoint"
            )
            
            # XÓA SAU 15 GIÂY
            await asyncio.sleep(15)
            try:
                await checkpoint_msg.delete()
            except:
                pass
            
            if status_alive:
                try:
                    await msg.delete()
                except:
                    pass
            
            sep()
            log(f"❌ User {user} tài khoản {idx}/{total} bị checkpoint")
            sep()
            return

        # ===== UPLOAD AVATAR (CHỈ KHI KHÔNG CÓ CHECKPOINT) =====
        if status_alive:
            await msg.edit_text(f"""👤 `{full_name}`
📧 `{email}`
🔑 `{pwd}`
🖼️ Đang upload avatar...""", parse_mode="Markdown")
        
        avatar_uploaded = upload_avatar_to_fb(driver)
        
        if avatar_uploaded:
            log("✅ Đã upload avatar thành công")
            time.sleep(random.uniform(3, 5))
        else:
            log("⚠️ Không upload được avatar")

        # ===== GỬI KẾT QUẢ THÀNH CÔNG =====
        if status_alive:
            await msg.edit_text(f"""👤 `{full_name}`
📧 `{email}`
🔑 `{pwd}`
📸 Đang chụp ảnh...""", parse_mode="Markdown")

        shot_time = datetime.now().strftime("%d/%m/%Y - %H:%M:%S")
        img = BytesIO(driver.get_screenshot_as_png())
        img.name = "fb.png"

        avatar_status = "✅ Có avatar" if avatar_uploaded else "⚠️ Chưa có avatar"
        
        await bot.send_photo(
            chat_id,
            photo=img,
            caption=f"""🎉 TẠO TÀI KHOẢN THÀNH CÔNG

👤 Thông tin cá nhân:
• Họ tên: {full_name}
• Giới tính: {gender}
• Năm sinh: 2009

🔐 Thông tin đăng nhập:
• Email: {email}
• Mật khẩu: {pwd}

{avatar_status}
⏰ Thời gian: {shot_time}

⚠️ Lưu ý: Giữ thông tin này an toàn""",
            parse_mode=None
        )

        if status_alive:
            try:
                await msg.delete()
            except:
                pass

        sep()
        log(f"✅ User {user} đã tạo xong {idx}/{total} acc")
        sep()

    except Exception as e:
        log(f"[REG ERROR] {e}")
        traceback.print_exc()
        if status_alive:
            try:
                await msg.edit_text(f"❌ Lỗi: {str(e)[:100]}...")
            except:
                pass
    finally:
        if driver:
          try:
             driver.quit()
          except:
               pass
        profile_dir = f"/data/data/com.termux/files/home/temp_profile_{user_id}"
        cleanup_profile(profile_dir)

    
# ================== COMMANDS ==================
async def setproxy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    if not context.args:
        await update.message.reply_text(
            "📝 **Sử dụng:** `/setproxy <proxy>`\n\n"
            "💡 **Ví dụ:**\n"
            "• `/setproxy 123.45.67.89:8080`\n"
            "• `/setproxy 123.45.67.89:8080:username:password`\n\n"
            "ℹ️ Proxy sẽ được dùng cho tất cả lệnh /reg sau này",
            parse_mode="Markdown"
        )
        return
    
    proxy_str = context.args[0]
    success, message = add_user_proxy(user_id, proxy_str)
    
    await update.message.reply_text(message)

async def huyproxy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    success, message = remove_user_proxy(user_id)
    
    await update.message.reply_text(message)

async def myproxy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_proxy = get_user_proxy(user_id)
    
    if user_proxy:
        proxy_url = user_proxy['proxy_url']
        proxy_auth = user_proxy['proxy_auth']
        added_time = user_proxy['added_time']
        
        message = f"🔧 **Proxy của bạn:**\n\n"
        message += f"• **URL:** `{proxy_url}`\n"
        if proxy_auth:
            message += f"• **Auth:** `{proxy_auth}`\n"
        message += f"• **Thêm lúc:** `{added_time}`\n\n"
        message += "Để xóa proxy, dùng lệnh: `/huyproxy`"
    else:
        message = "❌ Bạn chưa thiết lập proxy.\n\n"
        message += "Thiết lập proxy bằng lệnh: `/setproxy <proxy>`"
    
    await update.message.reply_text(message, parse_mode="Markdown")

async def reg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    if uid not in USER_LOCK:
        USER_LOCK[uid] = asyncio.Lock()

    if USER_LOCK[uid].locked():
        await update.message.reply_text("⏳ Đang chạy reg khác")
        return

    total = int(context.args[0]) if context.args else 1
    user = update.effective_user.full_name
    chat_id = update.effective_chat.id
    bot = context.bot

    async def wrap():
        async with USER_LOCK[uid]:
            user_proxy = get_user_proxy(uid)
            proxy_status = "🔧 Có proxy" if user_proxy else "🌐 Không dùng proxy"
            
            start_msg = await update.message.reply_text(
                f"🚀 Bắt đầu tạo {total} tài khoản Facebook...\n\n"
                f"{proxy_status}\n"
                "⏳ Mỗi acc mất khoảng 2-3 phút\n"
                "👤 Tên được tạo tự nhiên\n"
                "📧 Email hợp lý\n"
                "🔑 Mật khẩu dễ nhớ\n"
                "🔄 Có retry khi click nút Sign up"
            )
            
            await asyncio.sleep(10)
            try:
                await start_msg.delete()
            except:
                pass
            
            for i in range(1, total + 1):
                await reg_one(bot, chat_id, user, i, total, uid)

    context.application.create_task(wrap())

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 **Bot Tạo Facebook với Proxy**\n\n"
        "📝 **Lệnh cơ bản:**\n"
        "• `/reg [số_lượng]` - Tạo tài khoản\n"
        "• `/setproxy <proxy>` - Thiết lập proxy\n"
        "• `/huyproxy` - Xóa proxy\n"
        "• `/myproxy` - Xem proxy hiện tại\n\n"
        "🔧 **Định dạng proxy:**\n"
        "• `ip:port`\n"
        "• `ip:port:user:pass`\n\n"
        "💡 **Ví dụ:**\n"
        "• `/reg 1`\n"
        "• `/setproxy 123.45.67.89:8080`",
        parse_mode="Markdown"
    )

# ================== MAIN ==================
def main():
    # Cấp quyền khi khởi động
    fix_firefox_permissions()
    
    # Tải proxy
    load_proxies()
    
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("reg", reg))
    app.add_handler(CommandHandler("setproxy", setproxy))
    app.add_handler(CommandHandler("huyproxy", huyproxy))
    app.add_handler(CommandHandler("myproxy", myproxy))
    
    log("🤖 BOT STARTED - Đã fix quyền Firefox và checkpoint logic")
    log(f"👤 Đã tải {len(USER_PROXIES)} user có proxy")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()