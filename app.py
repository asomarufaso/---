import streamlit as st

# পেজ কনফিগারেশন
st.set_page_config(page_title="ভাড়া রসিদ জেনারেটর", page_icon="🏡", layout="centered")

st.title("🏡 ভাড়ার রসিদ জেনারেটর (ম্যানুয়াল এন্ট্রি)")
st.write("নিচের তথ্যগুলো পূরণ করে তাৎক্ষণিকভাবে রসিদ তৈরি করুন।")

# সংখ্যা রূপান্তর ও কমা ফরম্যাট ফাংশন
def to_bangla_formatted(num, is_unit=False):
    if isinstance(num, (int, float)):
        if is_unit:
            formatted_num = "{:,g}".format(num) 
        else:
            formatted_num = "{:,}".format(int(num))
    else:
        formatted_num = str(num).lower()

    eng_to_bng = {'0':'০', '1':'১', '2':'২', '3':'৩', '4':'৪', '5':'৫', '6':'৬', '7':'৭', '8':'৮', '9':'৯', ',':',', '.':'.'}
    eng_to_bng_char = {'a':'এ', 'b':'বি', 'c':'সি', 'd':'ডি', 'e':'ই', 'f':'এফ'}
    
    return "".join(eng_to_bng.get(char, eng_to_bng_char.get(char, char)) for char in formatted_num)

months_map = {
    "January": "জানুয়ারি", "February": "ফেব্রুয়ারি", "March": "মার্চ", 
    "April": "এপ্রিল", "May": "মে", "June": "জুন", 
    "July": "জুলাই", "August": "আগস্ট", "September": "সেপ্টেম্বর", 
    "October": "অক্টোবর", "November": "নভেম্বর", "December": "ডিসেম্বর"
}

# ইনপুট ফর্ম ডিজাইন
col1, col2 = st.columns(2)

with col1:
    flat_no_raw = st.text_input("📍 ফ্ল্যাট নং (যেমন: 1A বা 2B)", "1A")
    month_input = st.selectbox("📅 মাস নির্বাচন করুন", list(months_map.keys()))
    year_raw = st.text_input("📆 বছর", "2026")

with col2:
    total_bill_raw = st.number_input("🏠 মোট ভাড়া (Total Amount)", min_value=0, value=7115, step=1)
    paid_amount_raw = st.number_input("💵 পরিশোধ করেছেন (Paid Amount)", min_value=0, value=7000, step=1)
    name = st.text_input("💁‍♂️ শুভেচ্ছান্তে (আপনার নাম)", "মারুফ")

st.write("---")

# জেনারেট বাটন
if st.button("রসিদ তৈরি করুন ✨", type="primary"):
    # কনভার্সন
    flat_no_bn = to_bangla_formatted(flat_no_raw).upper()
    year_bn = to_bangla_formatted(year_raw)
    month_bn = months_map[month_input]
    
    total_bill = int(total_bill_raw)
    paid_amount = int(paid_amount_raw)
    
    # ডাইনামিক স্ট্যাটাস ও মেসেজ নির্ধারণ
    current_due = 0
    current_adv = 0
    status_msg = ""
    due_display = "০৳"
    adv_display = "০৳"
    
    if paid_amount < total_bill:
        current_due = total_bill - paid_amount
        status_msg = "✅ আপনার আংশিক ভাড়া গ্রহণ করা হয়েছে।\n🙏 অনুগ্রহ করে দ্রুত বকেয়াটুকু পরিশোধের চেষ্টা করবেন।"
        due_display = f"{to_bangla_formatted(current_due)}৳ ⚠️"
    elif paid_amount > total_bill:
        current_adv = paid_amount - total_bill
        status_msg = "🌸 ধন্যবাদ! আপনার অতিরিক্ত জমা টাকা পরবর্তী\nমাসের ভাড়ার সাথে সমন্বয় করা হবে।"
        adv_display = f"{to_bangla_formatted(current_adv)}৳ ⭐"
    else:
        status_msg = "✨ আলহামদুলিল্লাহ, আপনার এই মাসের ভাড়া\nসম্পূর্ণ পরিশোধ হয়েছে। ধন্যবাদ। 🤝"
        due_display = "০৳ (পরিশোধিত)"

    # ফাইনাল রসিদ টেক্সট
    receipt = f"""╔══🏡✨ ভাড়ার রসিদ ✨🏡══╗
📍 ফ্ল্যাট নং: {flat_no_bn}
📅 মাস: {month_bn} {year_bn}
╠══════════════════════╣
🏠 মোট ভাড়া            : {to_bangla_formatted(total_bill)}৳
💵 পরিশোধ করেছেন      : {to_bangla_formatted(paid_amount)}৳
📌 বকেয়া               : {due_display}
💰 অগ্রিম               : {adv_display}
╠══════════════════════╣
{status_msg}
🌿 আল্লাহ আপনার রিজিকে বরকত দান করুন।
╚════ 💁‍♂️ {name} ════╝"""

    # স্ক্রিনে সুন্দর করে আউটপুট দেখানো
    st.write("### 📋 আপনার রসিদ রেডি:")
    st.code(receipt, language=None)
    st.success("💡 ওপরের রসিদটির ডানদিকের 'Copy' বাটনে ক্লিক করে সহজেই কপি করে হোয়াটসঅ্যাপ বা মেসেঞ্জারে পাঠিয়ে দিন।")
