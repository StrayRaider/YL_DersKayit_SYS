import os
import re
from PIL import Image
from pdf2image import convert_from_path
import cv2
import pytesseract

def runOcr(filePath):
    data = ocrRead(filePath)
    if data:
        sdata = getStudentData(data)
        print(sdata)
        return parseDataNew(data), sdata
    else:
        print("error at reading data")

def ocrRead(filePath = '/home/stray/EmreKayaTranskript.pdf'):
    doc = convert_from_path(filePath)
    path, fileName = os.path.split(filePath)
    fileBaseName, fileExtension = os.path.splitext(fileName)
    custom_config = r'--psm 6 --oem 3'
    #custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789 --dpi 300'
    #custom_config = r"--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789"

    allPages = """  """

    for page_number, page_data in enumerate(doc):
        #txt = pytesseract.image_to_string(Image.fromarray(page_data)).encode("utf-8")
        txt = pytesseract.image_to_string(page_data,lang="eng", config=custom_config).encode("utf-8")
        allPages = allPages+" "+str(txt)
        #print("Page # {} - {}".format(str(page_number),txt))
    #print(allPages)
    return allPages


def parseData(data):
    print("\n\n\n")
    for x in data.split(" "):
        if x != '':
            print(x)
            y = re.findall("[A-F]{2}", x)
            if y:
                print("here : ",y,"\n")
            z = re.findall("\b[0-9]{7} ", x)
            if z:
                print("digited : ",z,"\n")
                
def getStudentData(data):
    studentData = []
    for i in data.split("\\n"):
        if "Mezuniyet Ortalamasi : " in i:
            i = i.split(" ")
            for x in i:
                note = str(re.findall("\d+\.\d+",str(i))[0])
                if(note):
                    print("\n",note,"\n")
                    studentData.append(float(note))
                    break

        elif "Ad1" in i:
            name = i.split(":")[1]
            name = name.split(" ")[0]
            studentData.append(name)

        elif "Soyad1" in i:
            surname = i.split(": ")[1]
            surname = surname.split(" ")[0]
            studentData.append(surname)

        elif "Ogrenci No" in i:
            studentNo = i.split(": ")[1]
            studentNo = studentNo.split(" ")[0]
            studentData.append(studentNo)
        if len(studentData) == 4:
            break
    print(studentData)
    return studentData
    

def parseDataNew(data):
    lessonC = 0
    lessons = []
    lessonNos = re.findall("(?<!\d)[0-9]{7}(?!\d)",data)
    notes = ['AA','BA', 'BB','CB', 'CC', 'DC','DD','FD','FF','KK','G']
    for i in data.split("\\n"):
        lessonNos = re.findall("(?<!\d)[0-9]{7}(?!\d)",i)
        if lessonNos:
            lessonC += 1
            lessons.append(i)
            #print(i.split(" "))
    #print(lessonC)
    lessonList = []

    for lesson in lessons:
        print(lesson)

        #name
        z = lesson
        z = z.split(" ")
        name = str(z[1]) +" "+ str(z[2])
        print(name)
        #name

        lessonL = []
        lessonNo = re.findall("(?<!\d)[0-9]{7}(?!\d)",lesson)[0]
        lessonL.append(lessonNo)
        foundednotes = re.findall("(?<![\w(])[A-Z]{2}(?![\w)])",lesson)
        foundedg = re.findall("(?<![\w(])[G](?![\w)])",lesson)
        print("here", foundedg)
        for x in foundedg:
            foundednotes.append(foundedg[0])
        print("here", foundednotes)
        for i in foundednotes:
            if i in notes:
                lessonL.append(i)
        if len(lessonL) == 1:
            lessonL.append("--")
        lessonL.append(name)
        lessonList.append(lessonL)

    print(lessonList) 
    for i in lessonList:
        print(i)
        
    return lessonList
    """ 
    data = data.replace('\\n', ' ')
    #print(data)
    lessonNos = re.findall("(?<!\d)[0-9]{7}(?!\d)",data)
    print(lessonNos, len(lessonNos))
    lessonNotes = re.findall("(?<![\w(])[A-Z]{2}(?![\w)])",data)
    notes = ['AA','BA', 'BB','CB', 'CC', 'DC','DD','FD','FF','KK']
    noteNumbers = 0
    print(lessonNotes)
    for i in lessonNotes:
        if i in notes:
            noteNumbers += 1
            print(i)
    print(noteNumbers)

    for i in data.split("Yariyll"):
        for x in str(i).split("AKTS"):
            print(x)
   """



    """#data = "123 1234567 emre AA 1234567 asd AA"
    y = re.findall("[A-Z]{2}", data)
    data_2 = data
    foundednotes = []
    notes = ['AA','BA', 'BB','CB', 'CC', 'DC','DD','FF','KK']
    for i in y:
        if i in notes:
            #print("here : ",i,"\n")
            foundednotes.append(i)
            data_2 = data_2.replace(str(i),str(i)+'\n')
    print(foundednotes)
    digits = re.findall("^[0-9]{7} ", data)
    if digits:
        print("digited : ",digits,"\n")
        for i in digits:
            data_2 = data_2.replace(str(i),'\n'+str(i))
    print(data_2, "\n here : ")
    data_3 = data_2.split('\n')
    for i in data_3:
        if i != '':
            print(i)"""

    
                

#data = ocrRead()
data = """
  b'Firefox\n\nlof 5\n\nhttps://ogr.kocaeli.edu.tr/KOUBS/Ogrenci/AnaGiris.cfm ?CFID=27305...\n\nKOCAELI UNIVERSITESI\nBASARI DURUM BELGESI\n\nOgrenci No : 210201029 T.C. Kimlik No : 40294706844\nAd1 :EMRE Dogum Tarihi :25/11/2003\n\nSoyad1 : KAYA\n\nBelge Tarihi :19/10/2023\n\nEgitim Birimi : Mithendislik Fakiiltesi Kayit Tarihi 1 04/09/2021\nProgrami/ABD/ASD : Bilgisayar Miihendisligi Giris Tiirit : OSYS\n\nAkademik Derece Tiirii : Lisans\nMezuniyet Ortalamasi : 3.52\n\n1. Yariyll\n\n0201202 Programlama I\nBilgisayar\n0201287 Miihendisligine\nGirig\nBilgisayar\n\n0201288 Laboratuvari I\n\n9501005 Matematik I\n9501018 Lineer Cebir\n\n9501038 Fizik I\n\n9901012 Tiirk Dili I (UE)\n\n9903365 Ingilizce I (UE)\n\nAtatiirk Tlkeleri ve\n9905013 Inkilap Tarihi I\n(UE)\n\nDersin\n\nStatiisii\nZorunlu\nDers\n\nZorunlu\nDers\n\nZorunlu\nDers\nZorunlu\nDers\nZorunlu\nDers\nZorunlu\nDers\n\nZorunlu\nDers\n\nZorunlu\nDers\n\nZorunlu\nDers\n\nSimify/Donemi : 3. Simf / 5 D\xc3\xa9nem\nGenel Not Ortalamas : 3.52\nBasarilan AKTS : 124\n\nOgretim\nDili\n\nBasar1\nNotu\n\nBasar\n\nAKTS Durumu\n\nKatsay1 Aciklama\n\nTirkce 3 CB 2.5 Bagarih\nTirkge 2 AA 4 Basarili\n\nTirkce 3 AA 4 Bagarih\nTirkce 6 BA 3.5 Bagarih\nTirkce 3 BB 3 Bagarih\n\nTirkce 5 BB 3 Bagarih\n\nOrgiin Dersin\nUzaktan Egitim\nDersi ile\nEslestirilmesi\n\nTirkce 2 BA 3.5 Bagarih\n\nOrgiin Dersin\nUzaktan Egitim\nDersi ile\nEslestirilmesi\n\nTirk\xc2\xa2e 4 AA 4 Basarili\n\nOrgiin Dersin\nUzaktan Egitim\nDersi ile\nEslestirilmesi\n\nTirkge 2 CB 2.5 Basarili\n\nUmuttepe Yerleskesi 41001 - Izmit/Kocaeli\nTel: +90 (262) 303 12 01 - 02 Fax: +90 (262) 303 12 03\nhttp://www .kocaeli.edu.tr E-Posta: ogrenci@kocaeli.edu.tr\n\n10/19/23, 15:14\n'b'Firefox https://ogr.kocaeli.edu.tr/KOUBS/Ogrenci/AnaGiris.cfm ?CFID=27305...\n\nKOCAELI UNIVERSITESI\nBASARI DURUM BELGESI\n\nOgrenci No : 210201029 T.C. Kimlik No : 40294706844\nAd1 :EMRE Dogum Tarihi : 25/11/2003\nSoyad1 : KAYA Belge Tarihi :19/10/2023\n\nDersin  Ogretim Basari Basar\n2. Yariyll Statiisii Dili AKTS Notu Katsay1 Durumu Aciklama\n0201204 Programlama II ZD(:;:nlu Tiirkge 3 AA 4 Basarili\nElektrik Devre 7z I\n0201295 Temelleri ve oruniu Tirkce 5 AA 4 Basarili\nDers\nUygulamalar:\n0201373 Bilgisayar Zorunlu Tirkce 3 BB 3 Basarih\n~ 7 Laboratuvari IT Ders N\n9501006 Matematik II ZD(:;:nlu Tirkce 6 BA 35 Basarih\n9501037 Fizik 11 ZD\xe2\x80\x98:::\xe2\x80\x9cIU Tirke 5  BA 3.5  Basanh\nZorunlu Orgiin Dersin\n9901013 Tiirk Dili IT (UE) Ders Tirkce 2 BA 35 Basarih  Uzaktan Egitim Dersi\n) ile Eslestirilmesi\n] Zorunlu Orgiin Dersin\n9903367 Ingilizce II (UE) Ders Tirkce 4 BA 35 Basarih  Uzaktan Egitim Dersi\n) ile Eslestirilmesi\nAtatiirk ilkeleri ve Zorunlu Orgiin Dersin\n9905014 Inkilap Tarihi IT Tirkce 2 BB 3 Basarih  Uzaktan Egitim Dersi\nDers . . .\n(UE) ile Eslestirilmesi\n9912002 Kariyer Planlama ZD(:;:nlu Tirkce 0 G 0 Basarih\n\nDersin  Ogretim Basar1 Basar\n3. Yariyll Statiisii Dili AKTS Notu Katsay1 Durumu Aciklama\n0105230 Kesikli Matematik %\xe2\x80\x98;\xe2\x80\x98:\xe2\x80\x9c1\xe2\x80\x9c Tirkee 4 BA 35  Basarih\nVeri Yapilart ve Zorunlu .\n0201206 Algoritmalart Ders Tiirkce 4 AA 4 Basarili\n\nUmuttepe Yerleskesi 41001 - Izmit/Kocaeli\nTel: +90 (262) 303 12 01 - 02 Fax: +90 (262) 303 12 03\nhttp://www .kocaeli.edu.tr E-Posta: ogrenci@kocaeli.edu.tr\n\n20f 5 10/19/23, 15:14\n'b'Firefox\n\n30f 5\n\nKOCAELI UNIVERSITESI\nBASARI DURUM BELGESI\n\nOgrenci No : 210201029 T.C. Kimlik No : 40294706844\n\nAd1 :EMRE Dogum Tarihi : 25/11/2003\nSoyad1 : KAYA Belge Tarihi :19/10/2023\nProgramlama Zorunlu .\n0201207 Laboratuvar - I Ders Tiirkge AA\n0201269 Mantiksal Tasarim ve  Zorunlu Tiirkge AA\nUygulamalar: Ders\n. Zorunlu .\n0201386 Staj I Ders Tiirkce G\nDiferansiyel Zorunlu .\n9501017 Denklemler Ders Tiirkce CcC\n9502028 Nesneye Yonelik Zorunlu Tiirkge AA\nProgramlama Ders\nDersin  Ogretim\n4. Yariyll Statiisii Dili AKTS\n0201208 Bi!gisayqr Organizasyonu ve Zorunlu Tirkee 4 AA\nMimarisi Ders\n0201210 Veritaban1 Yonetimi %(;I;:nlu Tirkce 3 BA\n0201211 Sistem Programlama %(;I;:nlu Tirkce 3 AA\n0201422 Programlama Laboratuvari \xe2\x80\x94 Zorunlu Tirkee 3 BA\nI Ders\n0201423 Progmlma Dilleri Zorunlu Tirkee 3 BA\nPrensipleri Ders\nOlasilik ve Raslant1 Zorunlu .\n9502026 Degiskenleri Ders Tirkce 5 AA\n9502029 Elektronik ve Uygulamalar1 %::nlu Tirkce 5 BB\nUni\\iersite Secmeli I\nDOGAL YAPI TASI Zorunlu Tirk\xc2\xa2e 4 AA\n(0215203 ISLETMECILIGI VE Ders (Tiirkge) (4)\n\nEKONOMISI)\n\nUmuttepe Yerleskesi 41001 - Izmit/Kocaeli\n\nTel: +90 (262) 303 12 01 - 02 Fax: +90 (262) 303 12 03\n\nhttp://www .kocaeli.edu.tr E-Posta: ogrenci@kocaeli.edu.tr\n\nBasan\nNotu\n\nBasarili\nBasarili\nBasarili\nBasarili\nBasarili\n4 Bagsarili\n35 Basarili\n4 Bagsarili\n35 Basarili\n35 Basarili\n4 Bagsarili\n3 Basarili\n4 Bagsarili\n\nhttps://ogr.kocaeli.edu.tr/KOUBS/Ogrenci/AnaGiris.cfm ?CFID=27305...\n\nAciklama\n\nUSD\n\n10/19/23, 15:14\n'b'Firefox https://ogr.kocaeli.edu.tr/KOUBS/Ogrenci/AnaGiris.cfm ?CFID=27305...\n\nKOCAELI UNIVERSITESI\nBASARI DURUM BELGESI\n\nOgrenci No : 210201029 T.C. Kimlik No : 40294706844\nAd1 :EMRE Dogum Tarihi : 25/11/2003\nSoyad1 : KAYA Belge Tarihi :19/10/2023\n\n5. Yariyl S\xe2\x80\x98:;:fl\xe2\x80\x98s\':l Ogl\xe2\x80\x98;fltiim AKTS B;Ei\xe2\x80\x98: Katsay1 D]?f:;:u Agiklama\n0201212 Igletim Sistemleri 20" Turkge 4 KK 0 Akt Donern\ns o 1 e Twe s KK 0 QNETen\n0201425 Isaret ve Sistemler %(:r*snlu Tirkge 3 KK 0 - 21(1;1;? SZ:H\n0201426 Staj 11 Zownlt - fydge 4 KK 0 - A Do\nooy Y e 3 kk 0 AR\n9502014 Sayisal Yontemler %(:r*snlu Tiirkce 3 KK 0 - 21(1;1;? SZ:H\n0201405 Ei_llg; t(():xgi.\';:%nligi ve ]S)t;gr?f li Tirkce 4 BA 35 Basarili\n\ngniversite Secmeli Zorunlu  Tiirkge 4 KK 0 . Aktif D\xc3\xa9nem\n(0805297 Film Kiiltiirii) Ders (Turkge) (4) Alman Ders\n\n6. Yariyil Dersin Statiisii Ogretim Dili AKTS Basar1 Notu Katsay1 Bagar1 Durumu Aciklama\n\nDersin  Ogretim Basar Basar\n7. Yariyll Statiisii Dili AKTS Notu Katsay1 Durumu Aciklama\nDogal Dil Isleme ve . e T\n0201378 Metin Madenciligine 0\xe2\x84\xa2 Tirkee 5 KK 0 Aktif D\xc3\xa9nem\nGiris Ders IIT Alinan Ders\n\n8. Yariyil Dersin Statiisii Ogretim Dili AKTS Basar1 Notu Katsay1 Bagar1 Durumu Aciklama\n\nAKTS Toplam Bilgileri Not Araliklart\n\nUmuttepe Yerleskesi 41001 - Izmit/Kocaeli\nTel: +90 (262) 303 12 01 - 02 Fax: +90 (262) 303 12 03\nhttp://www .kocaeli.edu.tr E-Posta: ogrenci@kocaeli.edu.tr\n\n4 of 5 10/19/23, 15:14\n'b"Firefox\n\n50f 5\n\nhttps://ogr.kocaeli.edu.tr/KOUBS/Ogrenci/AnaGiris.cfm ?CFID=27305...\n\nKOCAELI UNIVERSITESI\nBASARI DURUM BELGESI\n\nOgrenci No : 210201029 T.C. Kimlik No : 40294706844\nAd1 :EMRE Dogum Tarihi : 25/11/2003\nSoyad1 : KAYA Belge Tarihi :19/10/2023\n\nZorunlu Secmeli Ders Universite\n\nDers Se\xc2\xa2meli Ders\nSe\xc2\xa2meli 4 Puanlar Notlar <28 Agiklamalar\nDers I Sayilar\nSe\xc2\xa2meli 0 90-100 AA 4 Basarili\nOgrencinin Bagardig1 Ders II 80-89 BA 3.5 Bagarilt\n116 . 4\nAKTS Toplami Secmeli 0 75719 BB 3 Basarili\nDers II{ 70-74 CB 2.5 Bagarili\nSe\xc2\xa2meli 0 60-69 CC 2 Basarili\nDers IV\n50-59 DC 1.5 Kosullu\nSe\xc2\xa2meli 4 40-49 DD 1 Basarisiz\nDers I 30-39 FD 0.5 Basarisiz\nSecmeli\nAlmast Gereken AKTS Ders 11 4 0-29 FF 0 Bagarisiz\nToplami (2021/2022 Ders 180 S i 12 S 0 Siiren\nListesi ecmeli\nistesi) Ders 1T 20 Cz'ah\xc2\xa7ma\xe2\x80\x98\n. N 0 Girmedi\nSecmeli\nDesv 20 K 0 Kalir\nBagarih olunan uzaktan 6gretim derslerinin toplam AKTS G 0 Ge(%er\ndegieri = 16 E- 0 Bksik\nD 0 Devamsiz\n\nBoliimiin 2021/2022 Ders Listesine kayith 6grencilerin mezuniyet\nkontrollerinde ders listelerinde yer alan secimlik dersler icin\ngrup bazh kontrol yapilmaktadir.\n\n* Bu ogrenci disiplin cezasi almamigtir.\n\nUmuttepe Yerleskesi 41001 - Izmit/Kocaeli\nTel: +90 (262) 303 12 01 - 02 Fax: +90 (262) 303 12 03\nhttp://www .kocaeli.edu.tr E-Posta: ogrenci@kocaeli.edu.tr\n\n10/19/23, 15:14\n"

"""
#data = ocrRead()
#getStudentData(data)
#parseDataNew(data)
