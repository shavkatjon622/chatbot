from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import re

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Savol-javoblar bazasi
qa_pairs = {
    "salom": "Salom! Qanday yordam bera olishim mumkin?",
    "yaxshi": "Yaxshi, rahmat! Sizni qanday yordam bera olishim mumkin?",
    "qalesiz": "Yaxshi, rahmat! Sizni qanday yordam bera olishim mumkin?",
    "yordam ber": "Albatta! Sizga qanday yordam kerak?",
    "hozirgi vaqt": f"Hozirgi vaqt: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
    "bugungi vaqt": f"Bugungi vaqt: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
    "bugun havo qanday": "Bugungi havo sharoiti uchun iltimos, mahalliy ob-havo manbaiga qarang.",
    "ob havo qanday": "Bugungi havo sharoiti uchun iltimos, mahalliy ob-havo manbaiga qarang.",
    "havo qanday": "Bugungi havo sharoiti uchun iltimos, mahalliy ob-havo manbaiga qarang.",
    "o'zbekiston poytaxti nima": "O'zbekiston poytaxti Toshkent shahri.",
    "dunyoning eng baland tog'i qaysi": "Dunyoning eng baland tog'i Everest tog'idir, u Nepalda joylashgan.",
    "yaponiyadagi mashhur shaharlar": "Yaponiya poytaxti Tokio, shuningdek, Osaka, Kyoto, va Hokkaido mashhur shaharlardir.",
    "google nima qiladi": "Google internet qidiruv tizimi va turli xil onlayn xizmatlar, masalan, Gmail, Google Maps va YouTube xizmatlarini taqdim etadi.",
    "python dasturlash tili nima": "Python - bu yuqori darajadagi dasturlash tili bo'lib, u o'qish osonligi va qulayligi bilan mashhur.",
    "dunyoning eng katta okeani qaysi": "Tinch okeani dunyoning eng katta okeanidir.",
    "marsda hayot bormi": "Hozircha Marsda hayotning mavjudligi aniqlanmagan.",
    "kimyo nima": "Kimyo - bu moddalar va ularning xossalari, tarkibi va o'zgarishlari bilan shug'ullanadigan fan.",
    "matematika nima": "Matematika sonlar, shakllar, va ularning o'zaro munosabatlarini o'rganadigan ilmiy soha.",
    "uzbekistonda nechta viloyat bor": "O'zbekistonda 12 viloyat va 1 respublika – Toshkent shahri mavjud.",
    "eng katta daryo qaysi": "Dunyoning eng uzun daryosi Nil daryosidir.",
    "toshkent qaysi davlatda joylashgan": "Toshkent O'zbekiston poytaxti bo'lib, O'zbekistonda joylashgan.",
    "eng ko'p gapiriladigan tillar qaysilar": "Dunyoning eng ko'p gapiriladigan tillari: Xitoy tili, ingliz tili, hindi tili va ispan tili.",
    "yilni qanday hisoblash mumkin": "Yil 365 kun, lekin kabisat yillarida 366 kunga ega bo'ladi.",
    "yuqori texnologiya nima": "Yuqori texnologiya - bu ilm-fan va texnologiyaning eng zamonaviy va ilg'or sohalarini anglatadi.",
    "sun'iy intellekt nima": "Sun'iy intellekt kompyuterlar va mashinalarga inson aqlini taqlid qilish imkoniyatini beruvchi texnologiya.",
    "vulkan nima": "Vulkan yer po'stlog'ida gazlar va magma chiqib keladigan tabiiy shakl.",
    "bitcoin nima": "Bitcoin - bu raqamli valyuta bo'lib, u markazlashtirilmagan tizim asosida ishlaydi.",
    "yangi yil bayrami qachon": "Yangi yil bayrami har yili 1-yanvarda nishonlanadi.",
    "eng katta mamlakat qaysi": "Dunyoning eng katta mamlakati Rossiya.",
    "internet nima": "Internet - bu dunyo bo'ylab kompyuterlar va tarmoqlarni bog'laydigan global tizim.",
    "koronavirus nima": "Koronavirus - bu o'pkada yallig'lanish keltirib chiqaradigan virus turidir.",
    "android nima": "Android - bu mobil telefonlar va planshetlar uchun mo'ljallangan operatsion tizim.",
    "iPhone nima": "iPhone - Apple kompaniyasining mobil telefon brendi.",
    "usmoniylar imperiyasi qachon tushdi": "Usmoniylar imperiyasi 1922 yilda tushdi, u turli millatlarni o'z ichiga olgan katta imperiya edi.",
    "dunyo aholi soni qancha": "Dunyo bo'yicha aholi soni 8 milliarddan oshgan.",
    "toshkentda qaysi universitetlar mavjud": "Toshkentda O'zbekiston Milliy Universiteti, Toshkent Davlat Yuridik Universiteti va boshqa ko'plab universitetlar mavjud.",
    "aylana yuzasining maydoni qanday hisoblanadi": "Aylana yuzasining maydoni Pi * r^2 formulasi bilan hisoblanadi, bunda r - aylananing radiusi.",
    "yulduz nima": "Yulduz - bu yengil va issiq gazdan tashkil topgan, katta massa va kuchli nur sochadigan osmonda joylashgan jism.",
    "atom nima": "Atom - bu moddalar kimyoviy xossalarini saqlovchi eng kichik zarrachadir.",
    "dengiz suvining tuzligi qancha": "Dengiz suvining tuzligi o'rtacha 3.5% ni tashkil qiladi.",
    "uchish nima": "Uchish - bu havoda turli ob'ektlarning yuqoriga ko'tarilishi yoki parvoz qilishi.",
    "qaysi film oscarni yutdi": 'Oscar mukofoti eng yaxshi film uchun har yili beriladi, so\'nggi yillarda "Parasite" va "Everything Everywhere All at Once" yutgan.',
    "piramida nima": "Piramida - bu to'g'ri burchakli bazaga ega, uchta yoki ko'proq tomonga qarab balandlashadigan shakldir.",
    "robot nima": "Robot - bu dasturlash va mexanik qurilmalar yordamida ishlaydigan avtomatik qurilma.",
    "ko'chada nima bor": "Ko'cha - bu yo'llar, piyodalar uchun yo'laklar, avtomobillar uchun yo'llar va boshqa infratuzilma elementlarini o'z ichiga olgan hudud.",
    "ovozli yordamchi nima": "Ovozli yordamchi - bu kompyuter yoki mobil qurilmalarda ovozli buyruqlarga javob beradigan sun'iy intellekt tizimi.",
    "boshqa sayyoralar haqida nimani bilamiz": "Hozirgi kunda boshqa sayyoralar haqida ko'plab ma'lumotlar mavjud, ammo hayot izlari hali topilmagan.",
    "hayvonlar qanday ovoz chiqaradi": "Hayvonlar turli xil ovozlar chiqaradi, masalan, itlar havlaydi, mushuklar miyovlaydi.",
    "dengiz nima": "Dengiz - bu okean bilan bog'langan, qirg'oqlar bilan o'ralgan katta suv havzasi.",
    "avtomobillar nima": "Avtomobillar - bu motorli transport vositalari bo'lib, ular yo'lda harakat qilish uchun mo'ljallangan.",
    "adabiyot nima": "Adabiyot - bu yozma va og'zaki ifoda orqali inson tafakkurini, his-tuyg'ularini ifodalovchi san'at turi.",
    "rus tilida qanday so'zlar mavjud": "Rus tilida ko'plab so'zlar mavjud, ularning ba'zilari juda mashhur va har kuni ishlatiladi.",
    "bugungi yil qaysi yil": f"Bugungi yil: {datetime.now().year}",
    "tezlik nima": "Tezlik - bu ob'ektning harakatining vaqtga nisbatan o'zgarishi.",
    "qanday sportlarni yaxshi ko'rasiz": "Mening sportlarim haqida ma'lumotim yo'q, lekin sizning sevimli sportingiz qanday?",
    "insho yozish qanday bo'ladi": "Insho yozishda birinchi navbatda mavzu tanlanadi, so'ngra argumentlar keltiriladi va xulosa chiqariladi.",
    "olimpiya o'yinlari qachon o'tadi": "Olimpiya o'yinlari har to'rt yilda o'tkaziladi.",
    "musiqa nima": "Musiqa - bu tovushlar orqali ifodalangan san'at turi.",
    "kitob nima": "Kitob - bu matnli axborotlarni saqlovchi va o'qish uchun mo'ljallangan nashr.",
    "film nima": "Film - bu tasvirlar va ovozlar yordamida yaratilgan san'at asari."
}

# Foydalanuvchidan kelgan matnni normalize qilish
def normalize_input(user_input):
    # Kichik harflarga o'tkazish va maxsus belgilarni olib tashlash
    user_input = user_input.lower()
    user_input = re.sub(r"[^a-zA-Z0-9\s]", "", user_input)  # Maxsus belgilarni olib tashlash
    user_input = re.sub(r"\s+", " ", user_input)  # Ko'p bo'shliqlarni bitta bo'shliq bilan almashtirish
    # Ba'zi sinonimlar va turli shakllarni birlashtirish
    user_input = user_input.replace("ob havo", "bugun havo qanday").replace("hozirgi vaqt", "bugungi vaqt")
    return user_input

# Savolga javob olish funksiyasi
def get_answer(question):
    normalized_input = normalize_input(question)
    
    # Agar savol bazada bo'lsa, javobni qaytarish
    if normalized_input in qa_pairs:
        return qa_pairs[normalized_input]
    else:
        return "Kechirasiz, bu savolga javobim yo'q."

@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    question = data.get('question', '')
    answer = get_answer(question)
    return jsonify({'answer': answer})

if __name__ == '__main__':
    app.run(debug=True)