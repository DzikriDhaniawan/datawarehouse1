import os
import pdfplumber

# Menentukan direktori tempat file PDF berada
pdf_directory = r"C:/Users/Dzikri/Downloads"

# Mencari file PDF terbaru di direktori
pdf_files = [f for f in os.listdir(pdf_directory) if f.endswith('.pdf')]
latest_pdf_file = max([os.path.join(pdf_directory, f) for f in pdf_files], key=os.path.getmtime)

# Membaca data dari file PDF terbaru
with pdfplumber.open(latest_pdf_file) as pdf:
    # Menyimpan teks arus kas, laba rugi, dan neraca
    cash_flow_text = "Laporan laba rugi"
    income_statement_text = "Laporan arus kas"
    balance_sheet_text = "Laporan neraca"
    
    # Menentukan halaman yang ingin dibaca (misalnya halaman 1 hingga 10)
    for page_number in range(1, len(pdf.pages) + 1):  # Halaman 1 hingga terakhir
        page = pdf.pages[page_number - 1]  # Halaman dimulai dari 0
        text = page.extract_text()
        
        if text:
            # Mencari bagian arus kas, laba rugi, dan neraca
            if "ARUS KAS" in text.lower():
                cash_flow_text += text + "\n"
            if "LAPORAN LABA RUGI" in text.lower():
                income_statement_text += text + "\n"
            if "LAPORAN POSISI KEUANGAN" in text.lower():
                balance_sheet_text += text + "\n"

    # Menyimpan hasil ke file teks
    with open('arus_kas.txt', 'w', encoding='utf-8') as cash_flow_file:
        cash_flow_file.write(cash_flow_text)
        
    with open('laba_rugi.txt', 'w', encoding='utf-8') as income_statement_file:
        income_statement_file.write(income_statement_text)
        
    with open('neraca.txt', 'w', encoding='utf-8') as balance_sheet_file:
        balance_sheet_file.write(balance_sheet_text)

print(f"Data arus kas, laba rugi, dan neraca dari PDF terbaru '{latest_pdf_file}' berhasil disimpan.")
