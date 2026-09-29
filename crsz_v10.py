#!/usr/bin/env python3
# CRSZ v10.0 - FULL OSINT + ANİMASYON

import os, sys, json, time, re, random, requests
from datetime import datetime
from colorama import init, Fore, Back, Style
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.align import Align
from rich.box import ROUNDED
from rich.progress import Progress, SpinnerColumn, TextColumn
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import instaloader
import whois
import socket
import subprocess

init(autoreset=True)
console = Console()
ua = UserAgent()

# ========== ANİMASYONLU ASCII BAŞLIK ==========
def animate_header():
    os.system('clear')
    ascii_art = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║    ██████╗ ██████╗ ███████╗███████╗                         ║
    ║   ██╔════╝██╔═══██╗╚══███╔╝╚══███╔╝                        ║
    ║   ██║     ██║   ██║  ███╔╝   ███╔╝                         ║
    ║   ██║     ██║   ██║ ███╔╝   ███╔╝                          ║
    ║   ╚██████╗╚██████╔╝███████╗███████╗                        ║
    ║    ╚═════╝ ╚═════╝ ╚══════╝╚══════╝                        ║
    ║                                                              ║
    ║         ██╗  ██╗ █████╗  ██████╗██╗  ██╗                   ║
    ║         ██║  ██║██╔══██╗██╔════╝██║ ██╔╝                   ║
    ║         ███████║███████║██║     █████╔╝                    ║
    ║         ██╔══██║██╔══██║██║     ██╔═██╗                    ║
    ║         ██║  ██║██║  ██║╚██████╗██║  ██╗                   ║
    ║         ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝                   ║
    ║                                                              ║
    ║              TAM OSINT - SIZINTI TAKIP                       ║
    ║                   v10.0 - CRSZ ULTRA                        ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    console.print(Align.center(ascii_art, style="bold red"))
    time.sleep(0.3)

# ========== SHERLOCK GERÇEK KAYIT ==========
def sherlock_scan_gercek(username):
    sites = {
        "github": f"https://github.com/{username}",
        "twitter": f"https://twitter.com/{username}",
        "reddit": f"https://www.reddit.com/user/{username}",
        "youtube": f"https://www.youtube.com/@{username}",
        "instagram": f"https://www.instagram.com/{username}",
        "tiktok": f"https://www.tiktok.com/@{username}",
        "facebook": f"https://www.facebook.com/{username}",
        "pinterest": f"https://www.pinterest.com/{username}",
        "tumblr": f"https://{username}.tumblr.com",
        "spotify": f"https://open.spotify.com/user/{username}",
        "twitch": f"https://www.twitch.tv/{username}",
        "steam": f"https://steamcommunity.com/id/{username}",
        "patreon": f"https://www.patreon.com/{username}",
        "medium": f"https://medium.com/@{username}",
        "devianart": f"https://www.deviantart.com/{username}",
        "vimeo": f"https://vimeo.com/{username}",
        "telegram": f"https://t.me/{username}",
        "linkedin": f"https://www.linkedin.com/in/{username}",
        "vk": f"https://vk.com/{username}"
    }
    found = []
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True) as progress:
        task = progress.add_task("[cyan]Platformlar taranıyor...", total=len(sites))
        for site, url in sites.items():
            try:
                r = requests.get(url, headers={"User-Agent": ua.random}, timeout=5)
                if r.status_code == 200 and username.lower() in r.text.lower():
                    found.append((site, url))
            except:
                pass
            progress.advance(task)
    return found

# ========== EMAIL SIZINTI KONTROL ==========
def check_email_breach(email):
    try:
        r = requests.get(f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}", timeout=10)
        if r.status_code == 200:
            return r.json()
    except:
        pass
    return []

# ========== IP KONUM ==========
def get_ip_info(ip):
    try:
        r = requests.get(f"http://ip-api.com/json/{ip}", timeout=8)
        data = r.json()
        if data.get("status") == "success":
            return {
                "ip": ip,
                "country": data.get("country"),
                "city": data.get("city"),
                "region": data.get("regionName"),
                "isp": data.get("isp"),
                "lat": data.get("lat"),
                "lon": data.get("lon")
            }
    except:
        pass
    return None

# ========== CHROME ARAMA ==========
def chrome_ara(username):
    sonuclar = []
    try:
        arama_url = f"https://www.google.com/search?q={username}&num=20"
        r = requests.get(arama_url, headers={"User-Agent": ua.random}, timeout=12)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html.parser')
            for link in soup.find_all('a'):
                href = link.get('href')
                if href and 'http' in href and '/url?q=' in href:
                    temiz = href.split('/url?q=')[1].split('&')[0]
                    if temiz and username.lower() in temiz.lower():
                        sonuclar.append(temiz)
    except:
        pass
    return sonuclar[:10]

# ========== TELEFON BULMA (sosyal medya bio) ==========
def telefon_bul(username):
    # Örnek: bio'da telefon arar
    try:
        url = f"https://www.instagram.com/{username}"
        r = requests.get(url, headers={"User-Agent": ua.random}, timeout=8)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html.parser')
            for script in soup.find_all('script'):
                if 'bio' in str(script):
                    # Basit telefon regex
                    import re
                    telefonlar = re.findall(r'(\+?\d{10,15})', str(script))
                    if telefonlar:
                        return telefonlar[0]
    except:
        pass
    return None

# ========== ANA FONKSIYON ==========
def main():
    while True:
        animate_header()
        username = input("\n[?] Kullanıcı adı (sorgulanacak kişi): ").strip()
        if not username:
            console.print("[red]Kullanıcı adı gerekli![/red]")
            time.sleep(1)
            continue

        console.clear()
        console.print(Panel(f"[bold cyan]🔍 {username} İÇİN TAM TARAMA[/bold cyan]", box=ROUNDED))

        # 1. Sherlock
        console.print("[cyan]📡 Platformlar taranıyor...[/cyan]")
        found = sherlock_scan_gercek(username)
        if found:
            console.print("[bold green]✓ BULUNAN PLATFORMLAR:[/bold green]")
            for site, url in found:
                console.print(f"  [cyan]•[/cyan] {site}: {url}")
        else:
            console.print("[red]✗ Hiçbir platformda kayıt yok[/red]")

        # 2. Chrome arama
        console.print("\n[cyan]🌐 Chrome ile arama...[/cyan]")
        chrome_sonuc = chrome_ara(username)
        if chrome_sonuc:
            console.print("[bold yellow]✓ CHROME SONUÇLARI:[/bold yellow]")
            for url in chrome_sonuc:
                console.print(f"  [cyan]•[/cyan] {url}")
        else:
            console.print("[red]✗ Chrome sonucu yok[/red]")

        # 3. Email bulmaya çalış
        console.print("\n[cyan]📧 Email sızıntı kontrolü...[/cyan]")
        # Örnek email bulma - kullanıcı adı + @gmail.com
        muhtemel_email = f"{username}@gmail.com"
        breaches = check_email_breach(muhtemel_email)
        if breaches:
            console.print(f"[bold red]✓ EMAIL SIZINTISI:[/bold red]")
            for b in breaches[:5]:
                console.print(f"  [red]•[/red] {b.get('Name', 'Bilinmiyor')}")
        else:
            console.print("[green]✗ Email sızıntıda bulunamadı[/green]")

        # 4. Telefon bul
        console.print("\n[cyan]📱 Telefon aranıyor...[/cyan]")
        tel = telefon_bul(username)
        if tel:
            console.print(f"[bold yellow]✓ TELEFON BULUNDU:[/bold yellow] {tel}")
        else:
            console.print("[red]✗ Telefon bulunamadı[/red]")

        # 5. IP bilgisi (kendi IP)
        try:
            ip = requests.get("https://api.ipify.org", timeout=5).text
            ip_info = get_ip_info(ip)
            if ip_info:
                console.print("\n[bold blue]🌍 IP BİLGİLERİ (kendi IP):[/bold blue]")
                console.print(f"  IP: {ip_info['ip']}")
                console.print(f"  Ülke: {ip_info['country']}")
                console.print(f"  Şehir: {ip_info['city']}")
                console.print(f"  İSP: {ip_info['isp']}")
        except:
            pass

        # 6. WHOIS
        try:
            if '.' in username:
                w = whois.whois(username)
                console.print("\n[bold magenta]🌐 WHOIS:[/bold magenta]")
                console.print(f"  Domain: {username}")
                console.print(f"  Kayıtçı: {w.registrar}")
        except:
            pass

        console.print("\n[bold green]✓ TARAMA TAMAMLANDI![/bold green]")
        console.print("[dim]Ana menü için 'exit' yazın, devam için Enter'a basın...[/dim]")
        cikis = input().strip().lower()
        if cikis == "exit":
            break

if __name__ == "__main__":
    main()
