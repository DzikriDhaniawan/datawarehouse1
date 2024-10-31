import pandas as pd
from pyspark.sql import SparkSession
import os
import pdfplumber

print(os.getcwd())
os.chdir('C:/Users/Dzikri/Documents/SEMESTER 2')

# Path JDBC driver
jdbc_driver_path = r"C:\pangkalandata\drivers\mysql-connector-java-8.0.30.jar"

# Path file Excel
file_path = r"C:\pangkalandata\FinancialStatement-2023-Tahunan-AALI.xlsx"
# Path file PDF
pdf_file_path = r'C:\pangkalandata\laporan.pdf'

# Membuat SparkSession dan menambahkan konfigurasi untuk MySQL JDBC driver
spark = SparkSession.builder \
    .appName("Import Data to MySQL") \
    .config("spark.jars", jdbc_driver_path) \
    .getOrCreate()

# Membaca data dari Excel menggunakan pandas
laba_rugi_df = pd.read_excel(file_path, sheet_name="1321000", header=29)
arus_kas_df = pd.read_excel(file_path, sheet_name="1510000", header=179)
laporan_neraca_df = pd.read_excel(file_path, sheet_name="SheetName")  # Ganti dengan nama sheet yang benar

# Konversi DataFrame pandas ke DataFrame PySpark
laba_rugi_spark = spark.createDataFrame(laba_rugi_df)
arus_kas_spark = spark.createDataFrame(arus_kas_df)
laporan_neraca_spark = spark.createDataFrame(laporan_neraca_df)

# Mengatur koneksi JDBC ke MySQL
jdbc_url = "jdbc:mysql://localhost:3306/financial_data"
connection_properties = {
    "user": "root",
    "password": "",  # Ganti dengan password MySQL Anda
    "driver": "com.mysql.cj.jdbc.Driver"
}

# Menyimpan DataFrame PySpark ke tabel MySQL
laba_rugi_spark.write.jdbc(url=jdbc_url, table="laba_rugi", mode="overwrite", properties=connection_properties)
arus_kas_spark.write.jdbc(url=jdbc_url, table="arus_kas", mode="overwrite", properties=connection_properties)
laporan_neraca_spark.write.jdbc(url=jdbc_url, table="laporan_neraca", mode="overwrite", properties=connection_properties)

df_check = spark.read.jdbc(url=jdbc_url, table="laba_rugi", properties=connection_properties)
df_check.show(10)

# Misalkan df_spark adalah DataFrame PySpark Anda
laba_rugi_spark.write.text("output.txt")

# Membaca data dari file PDF dan menyimpannya ke file teks
with pdfplumber.open(pdf_file_path) as pdf, open('output_pdf.txt', 'w', encoding='utf-8') as output_file:
    for page in pdf.pages:
        text = page.extract_text()
        output_file.write(text)
        output_file.write('\n')

print("Data berhasil diimpor ke MySQL dan teks dari PDF berhasil disimpan ke output_pdf.txt.")

# Tutup SparkSession
spark.stop()
