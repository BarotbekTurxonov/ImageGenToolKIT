import requests
import sqlite3
import time
from datetime import datetime

class ProxyManager:
    def __init__(self, db_name="proxies.db"):
        self.db_name = db_name
        self.proxy_sources = [
            "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=1000&country=all&ssl=all&anonymity=all",
            "https://www.proxy-list.download/api/v1/get?type=http",
            "https://www.proxyscan.io/api/proxy?limit=100&type=http",
            "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
            "https://openproxy.space/list/http"
        ]
        self.setup_database()

    def setup_database(self):
        """Create SQLite database and proxies table if not exists."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS proxies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ip TEXT UNIQUE,
                port TEXT,
                protocol TEXT DEFAULT 'http',
                limit_count INTEGER DEFAULT 15,
                last_validated TEXT
            )
        """)
        conn.commit()
        conn.close()

    def fetch_proxies(self):
        """Fetch proxies from various sources."""
        proxies = set()
        for url in self.proxy_sources:
            try:
                print(f"Fetching proxies from: {url}")
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    proxies.update(response.text.splitlines())
            except Exception as e:
                print(f"Failed to fetch from {url}: {e}")
        print(f"Total proxies fetched: {len(proxies)}")
        return proxies

    def validate_proxy(self, proxy):
        """Validate a single proxy by making a request."""
        try:
            test_url = "https://magichour.ai"
            proxies = {"http": proxy, "https": proxy}
            response = requests.get(test_url, proxies=proxies, timeout=5)
            if response.status_code == 200:
                print(f"Proxy validated: {proxy}")
                return True
        except requests.exceptions.ProxyError as e:
            if "Tunnel connection failed" in str(e):
                print(f"Proxy failed: {proxy} - Bad Request")
        except Exception as e:
            print(f"Proxy failed: {proxy} - {e}")
        return False

    def save_proxy(self, proxy):
        """Save a validated proxy to the database."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        ip, port = proxy.split(":")
        try:
            cursor.execute("""
                INSERT OR IGNORE INTO proxies (ip, port, last_validated) 
                VALUES (?, ?, ?)
            """, (ip, port, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            conn.commit()
            print(f"Proxy saved: {proxy}")
        except Exception as e:
            print(f"Failed to save proxy {proxy}: {e}")
        finally:
            conn.close()

    def validate_and_store_proxies(self, proxies):
        """Validate proxies and store valid ones in the database."""
        for proxy in proxies:
            if self.validate_proxy(proxy):
                self.save_proxy(proxy)

    def get_proxies_from_db(self, limit=10):
        """Retrieve valid proxies from the database."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT ip, port FROM proxies WHERE limit_count > 0 LIMIT ?
        """, (limit,))
        results = cursor.fetchall()
        conn.close()
        return [f"{ip}:{port}" for ip, port in results]

    def reduce_limit(self, proxy):
        """Reduce usage limit for a proxy."""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        ip, port = proxy.split(":")
        cursor.execute("""
            UPDATE proxies SET limit_count = limit_count - 1 WHERE ip = ? AND port = ?
        """, (ip, port))
        conn.commit()
        conn.close()



if __name__ == "__main__":
    manager = ProxyManager()

    fetched_proxies = manager.fetch_proxies()
    manager.validate_and_store_proxies(fetched_proxies)

    valid_proxies = manager.get_proxies_from_db(limit=5)
    print("Valid proxies:", valid_proxies)

    if valid_proxies:
        manager.reduce_limit(valid_proxies[0])
        print(f"Reduced limit for proxy: {valid_proxies[0]}")
