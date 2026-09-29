#!/usr/bin/env python3
# CRSZ HACK PANEL v3.0

import os, sys, json, time, re
import requests
from datetime import datetime
from colorama import init, Fore, Back, Style
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.align import Align
import instaloader
from fake_useragent import UserAgent
from bs4 import BeautifulSoup

init(autoreset=True)
console = Console()
ua = UserAgent()

CONFIG = {"timeout": 30, "output_dir": "crsz_results"}
if not os.path.exists(CONFIG["output_dir"]):
    os.makedirs(CONFIG["output_dir"])

def log(msg, level="INFO"):
    ts = datetime.now().strftime("%H:%M:%S")
    if level=="INFO": console.print(f"[{ts}] [cyan]INFO[/cyan] {msg}")
    elif level=="ERROR": console.print(f"[{ts}] [red]ERROR[/red] {msg}")
    elif level=="SUCCESS": console.print(f"[{ts}] [green]SUCCESS[/green] {msg}")

def save_results(data, filename):
    path = os.path.join(CONFIG["output_dir"], filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    log(f"Kaydedildi: {path}", "SUCCESS")

def display_big_header():
    console.clear()
    header = """
    ╔═══════════════════════════════════════════════════╗
    ║   ██████╗ ██████╗ ███████╗███████╗              ║
    ║  ██╔════╝██╔═══██╗╚══███╔╝╚══███╔╝             ║
    ║  ██║     ██║   ██║  ███╔╝   ███╔╝              ║
    ║  ██║     ██║   ██║ ███╔╝   ███╔╝               ║
    ║  ╚██████╗╚██████╔╝███████╗███████╗             ║
    ║   ╚═════╝ ╚═════╝ ╚══════╝╚══════╝             ║
    ║          CRSZ HACK PANEL v3.0                    ║
    ║       TikTok + Instagram OSINT                   ║
    ╚═══════════════════════════════════════════════════╝
    """
    console.print(Align.center(header, style="bold red"))

class TikTokOSINT:
    def __init__(self, username):
        self.username = username
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": ua.random})
        self.base_url = "https://www.tiktok.com/@"

    def get_user_info(self):
        try:
            url = f"{self.base_url}{self.username}"
            resp = self.session.get(url, timeout=30)
            if resp.status_code != 200:
                return None
            soup = BeautifulSoup(resp.text, 'html.parser')
            data_script = soup.find("script", id="__NEXT_DATA__")
            if not data_script:
                return None
            json_data = json.loads(data_script.string)
            user_data = None
            for key in json_data.get("props", {}).get("pageProps", {}).keys():
                if "userInfo" in key:
                    user_data = json_data["props"]["pageProps"][key]
                    break
            if not user_data:
                return None
            info = {
                "username": self.username,
                "full_name": user_data.get("userInfo", {}).get("user", {}).get("uniqueId", ""),
                "nickname": user_data.get("userInfo", {}).get("user", {}).get("nickname", ""),
                "bio": user_data.get("userInfo", {}).get("user", {}).get("bioDescription", ""),
                "follower_count": user_data.get("userInfo", {}).get("stats", {}).get("followerCount", 0),
                "following_count": user_data.get("userInfo", {}).get("stats", {}).get("followingCount", 0),
                "verified": user_data.get("userInfo", {}).get("user", {}).get("verified", False)
            }
            return info
        except:
            return None

class InstagramOSINT:
    def __init__(self, username):
        self.username = username
        self.loader = instaloader.Instaloader(quiet=True, user_agent=ua.random)
        self.profile = None

    def get_user_info(self):
        try:
            self.profile = instaloader.Profile.from_username(self.loader.context, self.username)
            info = {
                "username": self.username,
                "full_name": self.profile.full_name,
                "bio": self.profile.biography[:150],
                "follower_count": self.profile.followers,
                "following_count": self.profile.followees,
                "post_count": self.profile.mediacount,
                "verified": self.profile.is_verified,
                "private": self.profile.is_private
            }
            return info
        except:
            return None

def main():
    display_big_header()
    tk = input("[?] TikTok kullanıcı adı: ").strip()
    ig = input("[?] Instagram kullanıcı adı: ").strip()
    
    tk_info = None
    ig_info = None
    
    if tk:
        tik = TikTokOSINT(tk)
        tk_info = tik.get_user_info()
        if tk_info:
            console.print(f"[green]✓ TikTok: @{tk_info['username']} bulundu[/green]")
        else:
            console.print(f"[red]✗ TikTok: @{tk} bulunamadı[/red]")
    
    if ig:
        ins = InstagramOSINT(ig)
        ig_info = ins.get_user_info()
        if ig_info:
            console.print(f"[green]✓ Instagram: @{ig_info['username']} bulundu[/green]")
        else:
            console.print(f"[red]✗ Instagram: @{ig} bulunamadı[/red]")
    
    if tk_info or ig_info:
        combined = {"timestamp": datetime.now().isoformat(), "tiktok": tk_info, "instagram": ig_info}
        fname = f"crsz_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        save_results(combined, fname)
        console.print("[bold green]✓ Tarama tamamlandı![/bold green]")
    else:
        console.print("[bold red]✗ Hiçbir veri alınamadı[/bold red]")

if __name__ == "__main__":
    main()
