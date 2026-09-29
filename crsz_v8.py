#!/usr/bin/env python3
# CRSZ HACK PANEL v8.0 - Gelişmiş Sherlock + Chrome Arama

import os, sys, json, time, re, requests
from datetime import datetime
from colorama import init
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.align import Align
from rich.progress import Progress, SpinnerColumn, TextColumn
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import instaloader
import whois

init(autoreset=True)
console = Console()
ua = UserAgent()

# ========== KİMLİK VERİTABANI (demo) ==========
VERI_TABANI = [
    {"ad": "Ahmet", "soyad": "Yılmaz", "il": "İstanbul", "ilce": "Kadıköy", "tc": "12345678901", "telefon": "05551234567", "adres": "Kadıköy, İstanbul", "dogum_yili": "1985"},
    {"ad": "Mehmet", "soyad": "Demir", "il": "Ankara", "ilce": "Çankaya", "tc": "10987654321", "telefon": "05321234567", "adres": "Çankaya, Ankara", "dogum_yili": "1990"},
    {"ad": "Ayşe", "soyad": "Kaya", "il": "İzmir", "ilce": "Bornova", "tc": "11223344556", "telefon": "05431234567", "adres": "Bornova, İzmir", "dogum_yili": "1995"}
]

# ========== SHERLOCK SİTELERİ (sadece gerçek kayıtları gösterir) ==========
def sherlock_scan_gercek(username):
    """Sadece kullanıcı adının gerçekten kayıtlı olduğu siteleri bulur"""
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
        "soundcloud": f"https://soundcloud.com/{username}",
        "steam": f"https://steamcommunity.com/id/{username}",
        "twitch": f"https://www.twitch.tv/{username}",
        "patreon": f"https://www.patreon.com/{username}",
        "medium": f"https://medium.com/@{username}",
        "devianart": f"https://www.deviantart.com/{username}",
        "vimeo": f"https://vimeo.com/{username}",
        "etsy": f"https://www.etsy.com/shop/{username}",
        "telegram": f"https://t.me/{username}",
        "linkedin": f"https://www.linkedin.com/in/{username}",
        "vk": f"https://vk.com/{username}",
        "flickr": f"https://www.flickr.com/people/{username}",
        "pastebin": f"https://pastebin.com/u/{username}",
        "hackernews": f"https://news.ycombinator.com/user?id={username}",
        "keybase": f"https://keybase.io/{username}",
        "gitlab": f"https://gitlab.com/{username}",
        "bitbucket": f"https://bitbucket.org/{username}",
        "sourceforge": f"https://sourceforge.net/u/{username}",
        "replit": f"https://replit.com/@{username}",
        "codepen": f"https://codepen.io/{username}",
        "npm": f"https://www.npmjs.com/~{username}",
        "pypi": f"https://pypi.org/user/{username}",
        "dockerhub": f"https://hub.docker.com/u/{username}",
        "wordpress": f"https://{username}.wordpress.com",
        "blogger": f"https://{username}.blogspot.com",
        "githubio": f"https://{username}.github.io"
    }
    found = []
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True) as progress:
        task = progress.add_task("[cyan]Gerçek kayıtlar taranıyor...", total=len(sites))
        for site, url in sites.items():
            try:
                r = requests.get(url, headers={"User-Agent": ua.random}, timeout=8)
                if r.status_code == 200:
                    # Sayfada kullanıcı adı geçiyor mu kontrol et (gerçek kayıt)
                    if username.lower() in r.text.lower():
                        found.append((site, url))
            except:
                pass
            progress.advance(task)
    return found

# ========== CHROME ARAMA (tüm sitelerde) ==========
def chrome_ara(username):
    """Google Chrome üzerinden tüm sitelerde ara"""
    console.print("[cyan]🌐 Chrome ile tüm internet taranıyor...[/cyan]")
    sonuclar = []
    try:
        # Google arama sorgusu - tüm sitelerde username ara
        arama_url = f"https://www.google.com/search?q={username}&num=50"
        headers = {"User-Agent": ua.random}
        r = requests.get(arama_url, headers=headers, timeout=15)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html.parser')
            # Google sonuç linklerini çek
            for link in soup.find_all('a'):
                href = link.get('href')
                if href and 'http' in href and '/url?q=' in href:
                    temiz = href.split('/url?q=')[1].split('&')[0]
                    if temiz and username.lower() in temiz.lower():
                        sonuclar.append(temiz)
    except:
        pass
    return sonuclar[:20]  # İlk 20 sonuç

# ========== OSINT MODU ==========
def osint_modu():
    console.clear()
    console.print("[bold cyan]=== OSINT MODU ===[/bold cyan]")
    username = input("[?] Kullanıcı adı: ").strip()
    if not username:
        console.print("[red]Kullanıcı adı gerekli![/red]")
        input("Enter'a bas...")
        return
    
    # Sherlock - Gerçek kayıtlı siteler
    found = sherlock_scan_gercek(username)
    if found:
        console.print("[bold green]✓ GERÇEK KAYITLI SİTELER:[/bold green]")
        for site, url in found:
            console.print(f"  [cyan]• {site}:[/cyan] {url}")
    else:
        console.print("[red]✗ Hiçbir sitede gerçek kayıt bulunamadı[/red]")
    
    # Chrome arama
    chrome_sonuclari = chrome_ara(username)
    if chrome_sonuclari:
        console.print("\n[bold yellow]🌐 CHROME ARAMA SONUÇLARI:[/bold yellow]")
        for url in chrome_sonuclari:
            console.print(f"  [cyan]•[/cyan] {url}")
    
    # TikTok (isteğe bağlı)
    console.print("\n[cyan]🐧 TikTok taranıyor...[/cyan]")
    try:
        url = f"https://www.tiktok.com/@{username}"
        r = requests.get(url, headers={"User-Agent": ua.random}, timeout=10)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html.parser')
            script = soup.find("script", id="__NEXT_DATA__")
            if script:
                data = json.loads(script.string)
                user = data.get("props", {}).get("pageProps", {}).get("userInfo", {})
                if user:
                    console.print("[bold magenta]📱 TIKTOK:[/bold magenta]")
                    console.print(f"  Kullanıcı: @{username}")
                    console.print(f"  Takipçi: {user.get('stats', {}).get('followerCount', 0)}")
                    console.print(f"  Bio: {user.get('user', {}).get('bioDescription', '')[:100]}")
    except:
        console.print("[red]TikTok taranamadı[/red]")
    
    input("\n[bold yellow]Devam için Enter'a bas...[/bold yellow]")

# ========== KİMLİK MODU ==========
def kimlik_modu():
    console.clear()
    console.print("[bold yellow]=== KİMLİK SORGULAMA ===[/bold yellow]")
    ad = input("Ad: ").strip()
    soyad = input("Soyad: ").strip()
    il = input("İl: ").strip()
    ilce = input("İlçe: ").strip()
    
    sonuc = None
    for kisi in VERI_TABANI:
        if (kisi["ad"].lower() == ad.lower() and 
            kisi["soyad"].lower() == soyad.lower() and
            kisi["il"].lower() == il.lower() and
            kisi["ilce"].lower() == ilce.lower()):
            sonuc = kisi
            break
    
    if sonuc:
        console.print("[bold green]✅ KAYIT BULUNDU:[/bold green]")
        table = Table(style="cyan")
        table.add_column("Alan", style="yellow")
        table.add_column("Değer", style="white")
        for k, v in sonuc.items():
            table.add_row(k, str(v))
        console.print(table)
    else:
        console.print("[red]❌ Veri bulunamadı![/red]")
    
    input("\nEnter'a bas...")

# ========== ANA MENÜ ==========
def main():
    while True:
        console.clear()
        header = """
    ╔═══════════════════════════════════════════════════╗
    ║   CRSZ PANEL v8.0 - GELİŞMİŞ SHERLOCK           ║
    ║   [osint] - Gerçek kayıtlı siteler + Chrome     ║
    ║   [kimlik] - Ad-soyad sorgulama                 ║
    ║   [exit] - Çıkış                                ║
    ╚═══════════════════════════════════════════════════╝
        """
        console.print(Align.center(header, style="bold red"))
        komut = input("\n[?] Komut: ").strip().lower()
        if komut == "osint":
            osint_modu()
        elif komut == "kimlik":
            kimlik_modu()
        elif komut == "exit":
            console.print("[red]Çıkılıyor...[/red]")
            sys.exit()
        else:
            console.print("[red]Geçersiz komut![/red]")
            time.sleep(1)

if __name__ == "__main__":
    main()
