#!/usr/bin/env python3
# CRSZ HACK PANEL v9.0 - UI Güncellendi, exit ile menü dönüşü

import os, sys, json, time, re, requests
from datetime import datetime
from colorama import init, Fore, Back, Style
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.align import Align
from rich.box import ROUNDED
from rich.layout import Layout
from rich.live import Live
from rich.text import Text
from rich.progress import Progress, SpinnerColumn, TextColumn
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import instaloader
import whois
import random

init(autoreset=True)
console = Console()
ua = UserAgent()

# ========== KİMLİK VERİTABANI ==========
VERI_TABANI = [
    {"ad": "Ahmet", "soyad": "Yılmaz", "il": "İstanbul", "ilce": "Kadıköy", "tc": "12345678901", "telefon": "05551234567", "adres": "Kadıköy, İstanbul", "dogum_yili": "1985"},
    {"ad": "Mehmet", "soyad": "Demir", "il": "Ankara", "ilce": "Çankaya", "tc": "10987654321", "telefon": "05321234567", "adres": "Çankaya, Ankara", "dogum_yili": "1990"},
    {"ad": "Ayşe", "soyad": "Kaya", "il": "İzmir", "ilce": "Bornova", "tc": "11223344556", "telefon": "05431234567", "adres": "Bornova, İzmir", "dogum_yili": "1995"}
]

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
        "replit": f"https://replit.com/@{username}",
        "codepen": f"https://codepen.io/{username}",
        "npm": f"https://www.npmjs.com/~{username}",
        "pypi": f"https://pypi.org/user/{username}",
        "dockerhub": f"https://hub.docker.com/u/{username}",
        "wordpress": f"https://{username}.wordpress.com",
        "blogger": f"https://{username}.blogspot.com"
    }
    found = []
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True) as progress:
        task = progress.add_task("[cyan]Taranıyor...", total=len(sites))
        for site, url in sites.items():
            try:
                r = requests.get(url, headers={"User-Agent": ua.random}, timeout=6)
                if r.status_code == 200 and username.lower() in r.text.lower():
                    found.append((site, url))
            except:
                pass
            progress.advance(task)
    return found

# ========== CHROME ARAMA ==========
def chrome_ara(username):
    console.print("[cyan]🌐 Chrome ile tüm internet taranıyor...[/cyan]")
    sonuclar = []
    try:
        arama_url = f"https://www.google.com/search?q={username}&num=30"
        r = requests.get(arama_url, headers={"User-Agent": ua.random}, timeout=15)
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
    return sonuclar[:15]

# ========== OSINT MODU ==========
def osint_modu():
    while True:
        console.clear()
        console.print(Panel("[bold cyan]🔍 OSINT - KULLANICI ARA[/bold cyan]", box=ROUNDED))
        console.print("[yellow]1[/yellow] - Kullanıcı adı ile ara")
        console.print("[yellow]exit[/yellow] - Ana menüye dön")
        secim = input("\n[?] Seçim: ").strip().lower()
        if secim == "exit":
            return
        elif secim == "1":
            username = input("[?] Kullanıcı adı: ").strip()
            if not username:
                console.print("[red]Kullanıcı adı gerekli![/red]")
                time.sleep(1)
                continue
            
            found = sherlock_scan_gercek(username)
            console.clear()
            console.print(Panel(f"[bold cyan]🔍 {username} ARAMA SONUÇLARI[/bold cyan]", box=ROUNDED))
            if found:
                console.print("[bold green]✓ GERÇEK KAYITLI SİTELER:[/bold green]")
                for site, url in found:
                    console.print(f"  [cyan]•[/cyan] {site}: {url}")
            else:
                console.print("[red]✗ Hiçbir sitede kayıt bulunamadı[/red]")
            
            chrome_sonuc = chrome_ara(username)
            if chrome_sonuc:
                console.print("\n[bold yellow]🌐 CHROME ARAMA:[/bold yellow]")
                for url in chrome_sonuc:
                    console.print(f"  [cyan]•[/cyan] {url}")
            
            input("\n[dim]Devam için Enter'a bas...[/dim]")

# ========== KİMLİK MODU ==========
def kimlik_modu():
    while True:
        console.clear()
        console.print(Panel("[bold yellow]🪪 KİMLİK SORGULAMA[/bold yellow]", box=ROUNDED))
        console.print("[yellow]1[/yellow] - Ad-Soyad ile sorgula")
        console.print("[yellow]exit[/yellow] - Ana menüye dön")
        secim = input("\n[?] Seçim: ").strip().lower()
        if secim == "exit":
            return
        elif secim == "1":
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
            
            console.clear()
            if sonuc:
                console.print(Panel("[bold green]✅ KAYIT BULUNDU[/bold green]", box=ROUNDED))
                table = Table(style="cyan")
                table.add_column("Alan", style="yellow")
                table.add_column("Değer", style="white")
                for k, v in sonuc.items():
                    table.add_row(k, str(v))
                console.print(table)
            else:
                console.print("[red]❌ Veri bulunamadı![/red]")
            
            input("\n[dim]Devam için Enter'a bas...[/dim]")

# ========== ANA MENÜ ==========
def main():
    while True:
        console.clear()
        header = """
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║   ██████╗ ██████╗ ███████╗███████╗                       ║
║  ██╔════╝██╔═══██╗╚══███╔╝╚══███╔╝                      ║
║  ██║     ██║   ██║  ███╔╝   ███╔╝                       ║
║  ██║     ██║   ██║ ███╔╝   ███╔╝                        ║
║  ╚██████╗╚██████╔╝███████╗███████╗                      ║
║   ╚═════╝ ╚═════╝ ╚══════╝╚══════╝                      ║
║                                                           ║
║              CRSZ PANEL v9.0                              ║
║                                                           ║
║  [1] OSINT - Kullanıcı ara (Sherlock + Chrome)           ║
║  [2] Kimlik sorgula (Ad-Soyad + İl/İlçe)                 ║
║  [exit] Çıkış                                            ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
        """
        console.print(Align.center(header, style="bold red"))
        secim = input("\n[?] Seçim: ").strip().lower()
        
        if secim == "1":
            osint_modu()
        elif secim == "2":
            kimlik_modu()
        elif secim == "exit":
            console.print("[bold red]Paneli kapatılıyor...[/bold red]")
            sys.exit()
        else:
            console.print("[red]Geçersiz seçim![/red]")
            time.sleep(1)

if __name__ == "__main__":
    main()
