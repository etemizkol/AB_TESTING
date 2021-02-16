import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
pd.set_option('display.max_columns', 20)

pd.set_option('expand_frame_repr', False) # KOLONLARIN / İLE AŞAĞI İNMESİNİ ENGELLER HEPSİ TEK SIRADA OLUR
pd.set_option('display.float_format', lambda x: '%.5f' % x)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


# Güven aralığı üzerine bir örnek çalışma
import statsmodels.stats.api as sms

df = sns.load_dataset("tips")
df.describe().T

# Total Bill: Hesap
# Tip : Bahşiş
sms.DescrStatsW(df["total_bill"]).tconfint_mean()
# Sonuç: (18.66333170435847, 20.908553541543164)
# Yorum: Restrorana gelecek 100 gruptan 95'i 18,66-20,90 arasında hesap bırakacak

sms.DescrStatsW(df["tip"]).tconfint_mean()
# Sonuç (2.8237993062818205, 3.172758070767359)
# Yorum Restorana geleek müşterileri grupları %95 güven aralığında 2,82-3,17 arası bahşiş bırakacaklar

# Bu işlemi yapmadan AYKIRI DEĞERLER TÖRPÜLENEBİLİR
# NaN DEĞERLER UÇURULMALIDIR.

# Başka bir örnek
df = sns.load_dataset("titanic")
df.describe().T

sms.DescrStatsW(df["age"].dropna()).tconfint_mean()
# Önemli not: Bütün verisetine dropna denirse
# o değişkene ait varolan değerlerde uçabileceğinden
# sace güven aralığı hesaplanacak kolona dropna demek gerekir
# Yorum: Titanikteki yolcuların yaşı %95 güven aralığında 28-30 arasındadır


# # AB Testing (Bağımsız İki Örneklem T Testi)
# İki grup ortalaması arasında karşılaştırma yapılmak istenildiğinde kullanılır.

df = sns.load_dataset("tips")
df.groupby("smoker").agg({"total_bill":"mean"})
# Sigara içernler ve içmeyenler arasında hesap konusunda istatistiksel olarak anlamlı bir fark var mı?

# Matematiksel olarak fark var
# Şans eseri olup olmadığını görmek için istatistiksel olarak bakacağız

# ------------------------------------------------------------------------------------------
# Proje Başladı

# nihai başarı ölçütü Purchase sayısı
control_group = pd.read_excel("\ab_testing_data.xlsx",sheet_name="Control Group")
control_group.head()
col_list = ["Impression","Click","Purchase","Earning"]
control_group = control_group[col_list]
control_group.head()
test_group = pd.read_excel("\ab_testing_data.xlsx",sheet_name="Test Group")
test_group = test_group[col_list]
test_group.head()
control_group.describe().T
test_group.describe().T
control_pur =control_group["Purchase"]
test_pur = test_group["Purchase"]
# normallik testi
#--------------------------------------------------------------------------------------
# 1. hipotez :
# average bidding grubunun dağılımı ile normal dağılım arasında istatistiki bir fark yoktur.
# average bidding grubunun dağılımı ile normal dağılım arasında istatistiki bir vardır.
# p<0.05 ise H0 RED

from scipy.stats import shapiro
test_istatistigi, pvalue = shapiro(test_pur)
print('Test İstatistiği = %.4f, p-değeri = %.4f' % (test_istatistigi, pvalue))

# p = 0.15
# 0.15 < 0.05 ifadesi sağlanmadığı için H0 RED EDİLEMEZ.
# Sonuç olarak Average bidding grubu dağılımı ile normal dağılım arasında istatistiki anlamlı bir fark yoktur.


# 2. hipotez :
# Control bidding grubunun dağılımı ile normal dağılım arasında istatistiki bir fark yoktur.
# Control bidding grubunun dağılımı ile normal dağılım arasında istatistiki bir vardır.
# p<0.05 ise H0 RED
# p>0.05 ise H0 REDDEDİLEMEZ

from scipy.stats import shapiro
test_istatistigi, pvalue = shapiro(control_pur)
print('Test İstatistiği = %.4f, p-değeri = %.4f' % (test_istatistigi, pvalue))

# p = 0.58
# 0.58 < 0.05 ifadesi sağlanmadığı için H0 RED EDİLEMEZ.
# Sonuç olarak Control bidding grubu dağılımı ile normal dağılım arasında istatistiki anlamlı bir fark yoktur.

# İki örneklemimiz de normallik varsayımı kabulunü geçtiği için Bağımsız iki örneklem T testi uygulanacaktır.
#--------------------------------------------------------------------------------------------------------------

# Varyans homojenliği testi
# hipotez:
# H0: Varyanslar homojendir
# H1: Varyanslar homojen değildir.
# levene testi kullanılacaktır.
from scipy import stats

stats.levene(test_pur,control_pur)

# P value = pvalue=0.108
# 0.108 < 0.05 ifadesi sağlanmadığı için H0 RED EDİLEMEZ.
# Sonuç olarak iki grubun varyansları homojendir.

# İki örneklemimiz de normallik varsayımı ve Varyans homojenliği testini geçtiği için Bağımsız iki örneklem T testi uygulanacaktır.

print(control_pur.mean())
print(test_pur.mean())
# Average bidding purchase ortalaması : 582.10
# Maximum bidding purchase ortalaması : 550.89
# Matematiksel olarak Average bidding daha yüksek satınalma ortalamsı sunuyor.
# Haydi bu soruyu birde istatistiksel olarak inceleyelim.

# Hipotez:
# H0: Maximum bidding ve Average Bidding ortalamarı arasında istatistiki olarak farklılık yoktur.
# H1: Maximum bidding ve Average Bidding ortalamarı arasında istatistiki olarak farklılık vardır.

# Bağımsız iki örneklem t testi:
test_istatistigi, pvalue = stats.ttest_ind(control_pur,test_pur,equal_var=True) # Varyans homojenliği sağlandığı için true
print("P Value değeri:",pvalue)
# P<0.05 İSE H0 RED
# P = 0.34
# H0 Reddedilemez
# Yani Maximum bidding ve Average Bidding ortalamarı arasında istatistiki olarak farklılık yoktur.

import statsmodels.stats.api as sms
sms.DescrStatsW(test_pur).tconfint_mean()
sms.DescrStatsW(control_pur).tconfint_mean()
