import re

def process_text(text):

    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b'

    found_emails = re.findall(email_pattern, text)
    hidden_text = re.sub(email_pattern, '{adres email ukryty}', text)
    emails_list = ';'.join(found_emails)
    return hidden_text, emails_list

with open('sampleText.txt', 'r', encoding='utf-8') as f:
    text = f.read()


hidden_text, emails_list = process_text(text)
print("\nZnalezione adresy email:")
print(emails_list)