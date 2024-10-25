import subprocess
import sys
import pkg_resources

required_packages = [
    'requests',
    'instaloader',
    'facebook-sdk',
    'stem',
    'beautifulsoup4',
    'whois'
]

def install_packages(packages):
    
    for package in packages:
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
        except subprocess.CalledProcessError as e:
            print(f"Paket yüklenirken bir hata oluştu: {e}")

def check_and_install_packages():
    
    installed_packages = {pkg.key for pkg in pkg_resources.working_set}
    missing_packages = [pkg for pkg in required_packages if pkg not in installed_packages]

    if missing_packages:
        print("Eksik paketler tespit edildi. Yükleniyor...")
        install_packages(missing_packages)
    else:
        print("Tüm gerekli paketler mevcut.")

t
check_and_install_packages()

import requests
import instaloader
import subprocess
import facebook
from stem import Signal
from stem.control import Controller
import binascii
import os
import whois
import socket
from bs4 import BeautifulSoup 
TEMPMAIL_API_BASE = "https://api.temp-mail.org/request/"

def search_google(query, api_key, cx):
    url = f"https://www.googleapis.com/customsearch/v1"
    params = {
        'key': api_key,
        'cx': cx,
        'q': query
    }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        results = response.json()
        search_info = []
        for item in results.get('items', []):
            search_info.append({
                'Title': item.get('title', 'Bilgi yok'),
                'Snippet': item.get('snippet', 'Bilgi yok'),
                'URL': item.get('link', 'Bilgi yok')
            })
        return search_info
    else:
        return "Google API isteği başarısız oldu."

def search_social_media(username):
    return "Sosyal medya araması fonksiyonu henüz tamamlanmamış."

def search_instagram(username):
    L = instaloader.Instaloader()

    try:
        profile = instaloader.Profile.from_username(L.context, username)
        profile_info = {
            'Username': profile.username,
            'Full Name': profile.full_name,
            'Bio': profile.biography,
            'Followers': profile.followers,
            'Following': profile.followees,
            'Posts': profile.mediacount,
            'Profile Pic URL': profile.profile_pic_url,
        }
        return profile_info
    except Exception as e:
        return str(e)

def search_github(keyword):
    url = f"https://api.github.com/search/repositories?q={keyword}"
    response = requests.get(url)

    if response.status_code == 200:
        results = response.json().get('items', [])
        github_info = []
        for repo in results:
            github_info.append({
                'Name': repo['name'],
                'URL': repo['html_url'],
                'Description': repo['description'],
                'Stars': repo['stargazers_count'],
                'Language': repo['language'],
            })
        return github_info
    else:
        return "GitHub API isteği başarısız oldu."

def display_github_results(results):
    for repo in results:
        print(f"Repo Adı: {repo['Name']}")
        print(f"URL: {repo['URL']}")
        print(f"Açıklama: {repo['Description']}")
        print(f"Yıldız: {repo['Stars']}")
        print(f"Dil: {repo['Language']}")
        print("-" * 40)

def search_dark_web(query):
    with Controller.from_port(port=9051) as controller:
        controller.authenticate()
        results = []
        results.append(f"example.onion/{query.replace(' ', '_')}")
        return results

def search_ip_info(ip_address):
    url = f"http://ip-api.com/json/{ip_address}"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        return "IP API isteği başarısız oldu."

def get_mac_address(ip_address):
    try:
        result = subprocess.run(['arp', '-n', ip_address], capture_output=True, text=True)
        output = result.stdout
        lines = output.split('\n')
        for line in lines:
            if ip_address in line:
                parts = line.split()
                if len(parts) >= 4:
                    return parts[3]
        return "MAC adresi bulunamadı."
    except Exception as e:
        return str(e)

def search_facebook(profile_id, access_token):
    try:
        graph = facebook.GraphAPI(access_token)
        profile = graph.get_object(id=profile_id, fields='id,name,bio,link,picture')
        profile_info = {
            'ID': profile.get('id', 'Bilgi yok'),
            'Name': profile.get('name', 'Bilgi yok'),
            'Bio': profile.get('bio', 'Bilgi yok'),
            'Link': profile.get('link', 'Bilgi yok'),
            'Profile Pic URL': profile.get('picture', {}).get('data', {}).get('url', 'Bilgi yok'),
        }
        return profile_info
    except facebook.GraphAPIError as e:
        return str(e)

def get_facebook_id(username, access_token):
    try:
        graph = facebook.GraphAPI(access_token)
        user = graph.get_object(username)
        user_id = user.get('id', 'Bilgi yok')
        return {'Facebook ID': user_id}
    except facebook.GraphAPIError as e:
        return str(e)

def hex_encode_message(message):
    try:
        return binascii.hexlify(message.encode()).decode()
    except Exception as e:
        return str(e)

def hex_decode_message(hex_message):
    try:
        return binascii.unhexlify(hex_message).decode()
    except Exception as e:
        return str(e)

def create_wordlist(words, file_path):
    try:
        with open(file_path, 'w') as file:
            for word in words:
                file.write(word + '\n')
        return f"Wordlist '{file_path}' dosyasına başarıyla yazıldı."
    except Exception as e:
        return str(e)

def find_admin_panels(url):
    admin_paths = [
        'admin', 'admin.php', 'login', 'wp-admin', 'administrator', 'admin_area',
        'controlpanel', 'cpanel', 'manager', 'webadmin', 'admin_login', 'admin_area'
    ]
    found_panels = []
    for path in admin_paths:
        full_url = f"{url.rstrip('/')}/{path}"
        try:
            response = requests.get(full_url, timeout=5)
            if response.status_code == 200:
                found_panels.append(full_url)
        except requests.RequestException:
            continue
    return found_panels

def whois_lookup(domain):
    try:
        domain_info = whois.whois(domain)
        return domain_info
    except Exception as e:
        return str(e)

def simple_port_scan(target, ports):
    open_ports = []
    for port in ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((target, port))
        if result == 0:
            open_ports.append(port)
        sock.close()
    return open_ports

def get_ip_from_website(url):
    try:
        ip_address = socket.gethostbyname(url)
        return ip_address
    except socket.error as e:
        return str(e)

def fetch_website_script(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        file_path = input("HTML içeriğinin kaydedileceği dosya yolunu girin (örneğin, site.html): ")
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(response.text)
        return f"HTML içeriği '{file_path}' dosyasına kaydedildi."
    except Exception as e:
        return str(e)

def generate_temp_email():
    response = requests.get(f"{TEMPMAIL_API_BASE}mailbox/format/json/")
    if response.status_code == 200:
        return response.json().get('email', 'E-posta adresi alınamadı.')
    else:
        return "Geçici e-posta API isteği başarısız oldu."

def get_temp_email_inbox(email):
    """Geçici e-posta gelen kutusunu kontrol eder."""
    response = requests.get(f"{TEMPMAIL_API_BASE}email/{email}/inbox/")
    if response.status_code == 200:
        return response.json()
    else:
        return "Geçici e-posta gelen kutusu API isteği başarısız oldu."

def get_instagram_user_id(username):
    try:
        url = f"https://www.instagram.com/{username}/?__a=1"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            user_id = data['graphql']['user']['id']
            return user_id
        else:
            return "Instagram API isteği başarısız oldu."
    except Exception as e:
        return str(e)

def check_internet_connection():
    try:
        response = requests.get("http://www.google.com", timeout=5)
        return True
    except requests.ConnectionError:
        return False

def main():
    if not check_internet_connection():
        print("İnternet bağlantısı sağlanamıyor. Lütfen bağlantınızı kontrol edin.")
        return

        print("Google araması:")
    print(search_google("Python programlama", "YOUR_API_KEY", "YOUR_CX"))

    print("Instagram araması:")
    print(search_instagram("instagram_username"))

    print("GitHub araması:")
    github_results = search_github("Python")
    display_github_results(github_results)

    print("Karanlık web araması:")
    print(search_dark_web("example_query"))

    print("IP bilgileri:")
    print(search_ip_info("8.8.8.8"))

    print("MAC adresi:")
    print(get_mac_address("192.168.1.1"))

    print("Facebook araması:")
    print(search_facebook("facebook_profile_id", "YOUR_ACCESS_TOKEN"))

    print("Facebook ID:")
    print(get_facebook_id("facebook_username", "YOUR_ACCESS_TOKEN"))

    print("Hex kodlama:")
    print(hex_encode_message("Merhaba"))

    print("Hex çözme:")
    print(hex_decode_message(hex_encode_message("Merhaba")))

    print("Wordlist oluşturma:")
    print(create_wordlist(["admin", "password", "123456"], "wordlist.txt"))

    print("Admin panelleri araması:")
    print(find_admin_panels("http://example.com"))

    print("Whois sorgulama:")
    print(whois_lookup("example.com"))

    print("Basit port taraması:")
    print(simple_port_scan("example.com", [80, 443]))

    print("IP alma:")
    print(get_ip_from_website("example.com"))

    print("Web sitesi scriptini alma:")
    print(fetch_website_script("http://example.com"))

    print("Geçici e-posta oluşturma:")
    print(generate_temp_email())

    print("Geçici e-posta gelen kutusu:")
    print(get_temp_email_inbox("your_temp_email"))

    print("Instagram kullanıcı ID'si:")
    print(get_instagram_user_id("instagram_username"))

if __name__ == "__main__":
    main()
