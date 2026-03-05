import secrets
import string

def generate_secure_api_key(length: int = 32) -> str:
    """
    Генерирует криптографически безопасный API-ключ.
    Использует URL-safe алфавит (буквы, цифры, - и _).
    """
    # token_urlsafe генерирует строку, которую удобно передавать в заголовках HTTP
    return secrets.token_urlsafe(length)

if __name__ == "__main__":
    new_key = generate_secure_api_key()
    
    print("\n" + "="*50)
    print("ГЕНЕРАТОР БЕЗОПАСНЫХ КЛЮЧЕЙ ДЛЯ MES-GATEWAY")
    print("="*50)
    print(f"Ваш новый API-ключ:\n\n{new_key}\n")
    print("="*50)
    print("ЧТО С НИМ ДЕЛАТЬ:")
    print("1. Скопируйте этот ключ.")
    print("2. Откройте файл .env в корне проекта.")
    print(f"3. Замените значение API_KEY_SECRET={new_key}")
    print("4. Перезапустите сервер.")
    print("="*50 + "\n")