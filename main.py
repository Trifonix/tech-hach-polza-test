"""
Проверка MX-записей доменов email-адресов.
"""

import re
import sys
from dns import resolver, exception

def extract_domain(email):
    match = re.search(r'@([^.]+(\.[^.]+)*)', email.strip())
    return match.group(1) if match else None

def check_domain_mx_records(domain):
    try:
        resolver.resolve(domain, 'A')
    except (resolver.NXDOMAIN, resolver.NoAnswer):
        return "домен отсутствует"
    
    try:
        resolver.resolve(domain, 'MX')
        return "домен валиден"
    except (resolver.NXDOMAIN, resolver.NoAnswer, resolver.Timeout, exception.DNSException):
        return "MX-записи отсутствуют или некорректны"

def main():
    try:
        with open('emails.txt', 'r', encoding='utf-8') as f:
            emails = f.readlines()
    except FileNotFoundError:
        print("Создайте файл emails.txt с email-адресами (по одному на строку).")
        sys.exit(1)
    
    print("#" * 40)
    print("Записываем результаты в файл ./result.txt")

    with open('result.txt', 'a', encoding='utf-8') as f:
        f.write(f"{"-" * 40}\n")
    
    for email in emails:
        domain = extract_domain(email)
        if not domain:
            status = "неверный формат email"
        else:
            status = check_domain_mx_records(domain)
        
        # print(f"k{email.strip():20}\t{status}")

        with open('result.txt', 'a', encoding='utf-8') as f:
            f.write(f"k{email.strip():20}\t\t\t\t{status}\n")
    
    with open('result.txt', 'a', encoding='utf-8') as f:
        f.write(f"{"-" * 40}\n")

    print("Закрываем ./result.txt")
    print("#" * 40)

if __name__ == "__main__":
    main()
