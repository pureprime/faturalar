from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas

# T1 ve T2+T3 kullanım ücretleri
T1_RATE = 2.790395
T2_T3_RATE = 3.706589

def calculate_bill(previous_data, current_data):
    # Net kullanımların hesaplanması
    net_total_usage = current_data['total_usage'] - previous_data['total_usage']
    net_t1_usage = current_data['t1_usage'] - previous_data['t1_usage']
    net_t2_t3_usage = (current_data['t2_usage'] + current_data['t3_usage']) - (previous_data['t2_usage'] + previous_data['t3_usage'])

    # Fatura tutarlarının hesaplanması
    t1_cost = net_t1_usage * T1_RATE
    t2_t3_cost = net_t2_t3_usage * T2_T3_RATE
    total_cost = t1_cost + t2_t3_cost

    # Ortak alan payının hesaplanması
    common_area_share = net_total_usage * 0.1125
    final_cost = total_cost + common_area_share

    return {
        'net_total_usage': net_total_usage,
        'net_t1_usage': net_t1_usage,
        'net_t2_t3_usage': net_t2_t3_usage,
        't1_cost': t1_cost,
        't2_t3_cost': t2_t3_cost,
        'total_cost': total_cost,
        'common_area_share': common_area_share,
        'final_cost': final_cost
    }

def generate_pdf(data, apartment_no):
    filename = f"daire_{apartment_no}_elektrik_faturasi.pdf"
    c = canvas.Canvas(filename, pagesize=A4)
    c.translate(20 * mm, 280 * mm)
    
    # Başlık
    c.drawString(0, 0, f"Daire No: {apartment_no} Elektrik Faturası")
    
    # Kullanımlar ve maliyetler
    c.drawString(0, -20, f"Net Toplam Kullanım: {data['net_total_usage']} kWh")
    c.drawString(0, -40, f"Gündüz Endeksi (T1 Kullanımı): {data['net_t1_usage']} kWh")
    c.drawString(0, -60, f"Gece Endeksi (T2 + T3 Kullanımı): {data['net_t2_t3_usage']} kWh")
    c.drawString(0, -80, f"Gündüz Maliyeti: {data['t1_cost']:.2f} TL")
    c.drawString(0, -100, f"Gece Maliyeti: {data['t2_t3_cost']:.2f} TL")
    c.drawString(0, -120, f"Toplam Maliyet: {data['total_cost']:.2f} TL")
    c.drawString(0, -140, f"Ortak Alan Payı: {data['common_area_share']:.2f} TL")
    c.drawString(0, -160, f"Ödenecek Toplam Tutar: {data['final_cost']:.2f} TL")
    
    # PDF'i kapatma
    c.showPage()
    c.save()

def get_usage_data_for_month(month):
    usage_data = []
    for i in range(1, 21):  # 20 daire için döngü
        print(f"\n{i}. Daire için {month} Ayı Verilerini Girin:")
        apartment_no = input("Daire No: ")
        total_usage = float(input(f"Toplam Kullanım (kWh): "))
        t1_usage = float(input(f"T1 Kullanımı (Gündüz, kWh): "))
        t2_usage = float(input(f"T2 Kullanımı (Gece, kWh): "))
        t3_usage = float(input(f"T3 Kullanımı (Gece, kWh): "))

        usage_data.append({
            'apartment_no': apartment_no,
            'total_usage': total_usage,
            't1_usage': t1_usage,
            't2_usage': t2_usage,
            't3_usage': t3_usage
        })

    return usage_data

def sum_usages(usage_data):
    total_usage = sum(d['total_usage'] for d in usage_data)
    t1_usage = sum(d['t1_usage'] for d in usage_data)
    t2_usage = sum(d['t2_usage'] for d in usage_data)
    t3_usage = sum(d['t3_usage'] for d in usage_data)

    return {
        'total_usage': total_usage,
        't1_usage': t1_usage,
        't2_usage': t2_usage,
        't3_usage': t3_usage
    }

# Önceki ve mevcut aylar için veri alımı
previous_month_data = get_usage_data_for_month("Mayıs")
current_month_data = get_usage_data_for_month("Haziran")

# Her daire için fatura hesaplama ve PDF oluşturma
for i in range(20):
    previous_data = previous_month_data[i]
    current_data = current_month_data[i]
    
    # Fatura hesaplama
    bill_data = calculate_bill(previous_data, current_data)
    
    # PDF oluşturma (daire no'ya göre)
    generate_pdf(bill_data, current_data['apartment_no'])

