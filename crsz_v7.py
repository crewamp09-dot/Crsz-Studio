#!/usr/bin/env python3
# CRSZ HACK PANEL v7.0 - KOMUTLU GEÇİŞ SİSTEMİ

import os, sys, json, time, re
import requests
from datetime import datetime
from colorama import init
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.align import Align
from rich.progress import Progress, SpinnerColumn, TextColumn
import instaloader
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import whois

init(autoreset=True)
console = Console()
ua = UserAgent()

# ========== KİMLİK VERİTABANI (demo) ==========
VERI_TABANI = [
    {
        "ad": "Ahmet", "soyad": "Yılmaz", "il": "İstanbul", "ilce": "Kadıköy",
        "tc": "12345678901", "telefon": "05551234567", "adres": "Kadıköy, İstanbul",
        "dogum_yili": "1985", "anne_kizlik": "Demir", "baba_ad": "Mehmet"
    },
    {
        "ad": "Mehmet", "soyad": "Demir", "il": "Ankara", "ilce": "Çankaya",
        "tc": "10987654321", "telefon": "05321234567", "adres": "Çankaya, Ankara",
        "dogum_yili": "1990", "anne_kizlik": "Yıldız", "baba_ad": "Ali"
    },
    {
        "ad": "Ayşe", "soyad": "Kaya", "il": "İzmir", "ilce": "Bornova",
        "tc": "11223344556", "telefon": "05431234567", "adres": "Bornova, İzmir",
        "dogum_yili": "1995", "anne_kizlik": "Çelik", "baba_ad": "Hasan"
    }
]

# ========== SHERLOCK SİTELERİ (kısaltılmış) ==========
SITES = {
    "github": "https://github.com/{}",
    "twitter": "https://twitter.com/{}",
    "reddit": "https://www.reddit.com/user/{}",
    "youtube": "https://www.youtube.com/@{}",
    "instagram": "https://www.instagram.com/{}",
    "tiktok": "https://www.tiktok.com/@{}",
    "facebook": "https://www.facebook.com/{}",
    "pinterest": "https://www.pinterest.com/{}",
    "tumblr": "https://{}.tumblr.com",
    "spotify": "https://open.spotify.com/user/{}",
    "twitch": "https://www.twitch.tv/{}",
    "steam": "https://steamcommunity.com/id/{}",
    "patreon": "https://www.patreon.com/{}",
    "medium": "https://medium.com/@{}",
    "devianart": "https://www.deviantart.com/{}"
}

# ========== ANA MENÜ ==========
def display_main_header():
    console.clear()
    header = """
    ╔══════════════════════════════════════════════════════════════╗
    ║   ██████╗ ██████╗ ███████╗███████╗                          ║
    ║  ██╔════╝██╔═══██╗╚══███╔╝╚══███╔╝                         ║
    ║  ██║     ██║   ██║  ███╔╝   ███╔╝                          ║
    ║  ██║     ██║   ██║ ███╔╝   ███╔╝                           ║
    ║  ╚██████╗╚██████╔╝███████╗███████╗                         ║
    ║   ╚═════╝ ╚═════╝ ╚══════╝╚══════╝                         ║
    ║              CRSZ PANEL v7.0 - KOMUTLU                      ║
    ║                                                             ║
    ║  [bold yellow]KOMUTLAR:[/bold yellow]                                        ║
    ║  [cyan]osint[/cyan]   - 100+ platformda kullanıcı adı taraması              ║
    ║  [cyan]kimlik[/cyan]  - Ad-soyad + il/ilçe ile kimlik sorgulama             ║
    ║  [cyan]exit[/cyan]    - Paneli kapat                                      ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    console.print(Align.center(header, style="bold red"))

# ========== OSINT MODÜLÜ (V5) ==========
def get_tiktok(username):
    try:
        url = f"https://www.tiktok.com/@{username}"
        resp = requests.get(url, headers={"User-Agent": ua.random}, timeout=15)
        if resp.status_code != 200: return None
        soup = BeautifulSoup(resp.text, 'html.parser')
        script = soup.find("script", id="__NEXT_DATA__")
        if not script: return None
        data = json.loads(script.string)
        user = data.get("props", {}).get("pageProps", {}).get("userInfo", {})
        if not user: return None
        return {
            "username": username,
            "full_name": user.get("user", {}).get("uniqueId", ""),
            "bio": user.get("user", {}).get("bioDescription", "")[:100],
            "follower_count": user.get("stats", {}).get("followerCount", 0),
            "following_count": user.get("stats", {}).get("followingCount", 0),
            "verified": user.get("user", {}).get("verified", False)
        }
    except: return None

def get_instagram(username):
    try:
        loader = instaloader.Instaloader(quiet=True, user_agent=ua.random)
        profile = instaloader.Profile.from_username(loader.context, username)
        return {
            "username": username,
            "full_name": profile.full_name,
            "bio": profile.biography[:100],
            "follower_count": profile.followers,
            "following_count": profile.followees,
            "post_count": profile.mediacount,
            "verified": profile.is_verified
        }
    except: return None

def sherlock_scan(username):
    found = []
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True) as progress:
        task = progress.add_task("[cyan]Taranıyor...", total=len(SITES))
        for site, url_template in SITES.items():
            url = url_template.format(username)
            try:
                r = requests.get(url, headers={"User-Agent": ua.random}, timeout=5)
                if r.status_code == 200:
                    found.append((site, url))
            except: pass
            progress.advance(task)
    return found

def osint_modu():
    console.clear()
    console.print("[bold cyan]=== OSINT MODU ===[/bold cyan]")
    username = input("[?] Kullanıcı adı: ").strip()
    if not username:
        console.print("[red]Kullanıcı adı gerekli![/red]")
        return
    
    console.print("[cyan]🔍 Sherlock taraması...[/cyan]")
    found = sherlock_scan(username)
    if found:
        console.print("[bold green]✓ Bulunan platformlar:[/bold green]")
        for site, url in found[:15]:
            console.print(f"  [cyan]• {site}:[/cyan] {url}")
    
    console.print("[cyan]🐧 TikTok taranıyor...[/cyan]")
    tk = get_tiktok(username)
    if tk:
        console.print("[bold magenta]📱 TIKTOK:[/bold magenta]")
        console.print(f"  Kullanıcı: @{tk['username']}")
        console.print(f"  Takipçi: {tk['follower_count']}")
        console.print(f"  Bio: {tk['bio']}")
    
    console.print("[cyan]📸 Instagram taranıyor...[/cyan]")
    ig = get_instagram(username)
    if ig:
        console.print("[bold green]📷 INSTAGRAM:[/bold green]")
        console.print(f"  Kullanıcı: @{ig['username']}")
        console.print(f"  Takipçi: {ig['follower_count']}")
        console.print(f"  Bio: {ig['bio']}")
    
    input("\n[bold yellow]Devam etmek için Enter'a bas...[/bold yellow]")

# ========== KİMLİK MODÜLÜ (V6) ==========
def kimlik_ara(ad, soyad, il, ilce):
    sonuclar = []
    for kisi in VERI_TABANI:
        if (kisi["ad"].lower() == ad.lower() and 
            kisi["soyad"].lower() == soyad.lower() and
            kisi["il"].lower() == il.lower() and
            kisi["ilce"].lower() == ilce.lower()):
            sonuclar.append(kisi)
    return sonuclar

def kimlik_modu():
    console.clear()
    console.print("[bold yellow]=== KİMLİK SORGULAMA MODU ===[/bold yellow]")
    ad = input("[?] Ad: ").strip()
    soyad = input("[?] Soyad: ").strip()
    il = input("[?] İl: ").strip()
    ilce = input("[?] İlçe: ").strip()
    
    sonuclar = kimlik_ara(ad, soyad, il, ilce)
    if sonuclar:
        console.print("[bold green]✅ KAYIT BULUNDU:[/bold green]")
        for kisi in sonuclar:
            table = Table(title=f"{kisi['ad']} {kisi['soyad']}", style="cyan")
            table.add_column("Alan", style="yellow")
            table.add_column("Değer", style="white")
            table.add_row("TC", kisi["tc"])
            table.add_row("Telefon", kisi["telefon"])
            table.add_row("Adres", kisi["adres"])
            table.add_row("Doğum", kisi["dogum_yili"])
            console.print(table)
    else:
        console.print("[red]❌ Veri bulunamadı![/red]")
    
    input("\n[bold yellow]Devam etmek için Enter'a bas...[/bold yellow]")

# ========== ANA ==========
def main():
    while True:
        display_main_header()
        komut = input("\n[?] Komut girin (osint/kimlik/exit): ").strip().lower()
        if komut == "osint":
            osint_modu()
        elif komut == "kimlik":
            kimlik_modu()
        elif komut == "exit":
            console.print("[bold red]Paneli kapatılıyor...[/bold red]")
            sys.exit()
        else:
            console.print("[red]Geçersiz komut! osint, kimlik veya exit yazın.[/red]")
            time.sleep(1)

if __name__ == "__main__":
    main()
