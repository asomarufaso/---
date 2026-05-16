import streamlit as st
import pandas as pd
import io

# পেজ সেটআপ
st.set_page_config(page_title="ডাইনামিক ভাড়া রসিদ জেনারেটর", page_icon="🏠", layout="centered")

st.title("🏠 ডাইনামিক ভাড়া রসিদ জেনারেটর")
st.write("আপনার এক্সেল (.xlsx) ফাইলটি আপলোড করে এক ক্লিকে সব রসিদ তৈরি করুন।")

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

def custom_round(num):
    return int(num) + 1 if num - int(num) >= 0.5 else int(num)

months_map = {
    "january": "জানুয়ারি", "february": "ফেব্রুয়ারি", "march": "মার্চ", 
    "april": "এপ্রিল", "may": "মে", "june": "জুন", 
    "july": "জুলাই", "august": "আগস্ট", "september": "সেপ্টেম্বর", 
    "october": "অক্টোবর", "november": "নভেম্বর", "december": "ডিসেম্বর"
}

# ফাইল আপলোডার উইজেট
uploaded_file = st.file_uploader("📁 আপনার এক্সেল ফাইলটি এখানে ড্রপ করুন বা ব্রাউজ করুন", type=["xlsx"])

if uploaded_file is not None:
    try:
        df = pd.read_excel(uploaded_file)
        st.success(f"✅ সফলভাবে {len(df)} টি ফ্ল্যাটের ডাটা লোড হয়েছে!")
        
        # জেনারেট বাটন
        if st.button("সব রসিদ একসাথে জেনারেট করুন ✨"):
            st.write("### 📋 জেনারেট হওয়া রসিদসমূহ:")
            
            for index, row in df.iterrows():
                flat = str(row['Flat'])
                month = str(row['Month']).strip().lower()
                rent = float(row['Rent'])
                unit = float(row['Unit']) 
                rate = float(row['Rate'])
                water = float(row['Water'])
                clean = float(row['Cleaning'])
                due = float(row['Due'])
                adv = float(row['Advance'])

                # ক্যালকুলেশন ও রাউন্ডিং
                mas_bangla = months_map.get(month, month.capitalize())
                elec_raw = unit * rate
                elec_final = custom_round(elec_raw)
                total_final = custom_round((rent + elec_raw + water + clean + due) - adv)
                
                # বিল ফরম্যাট ডিজাইন
                msg = f"""🌟✨ ━━《 🏠 বাড়ি ভাড়ার বিবরণ 🏠 》━━ ✨🌟
🏡 ফ্ল্যাট: {to_bangla_formatted(flat).upper()}

📅 মাস: {mas_bangla} ২০২৬
📋 বিস্তারিত হিসাব:
━━━━━━━━━━━━━━━━━━━
🏠 বাড়ি ভাড়া: {to_bangla_formatted(rent)}৳
⚡ বৈদ্যুতিক বিল: {to_bangla_formatted(unit, is_unit=True)}×{to_bangla_formatted(rate)} = {to_bangla_formatted(elec_final)}৳
🚿 পানির বিল: {to_bangla_formatted(water)}৳
🧹🗑 ক্লিনিং ও আবর্জনা বিল: {to_bangla_formatted(clean)}৳
📌 বকেয়া: {to_bangla_formatted(due)}৳
💰 অগ্রিম: {to_bangla_formatted(adv)}৳
━━━━━━━━━━━━━━━━━━━
💵 মোট পরিশোধযোগ্য: ({to_bangla_formatted(rent)}+{to_bangla_formatted(elec_final)}+{to_bangla_formatted(water)}+{to_bangla_formatted(clean)}+{to_bangla_formatted(due)}-{to_bangla_formatted(adv)})
🎯 সর্বমোট: {to_bangla_formatted(total_final)}✅

📌 👉 নির্ধারিত সময়ে বিলটি পরিশোধ করবেন

🌟 শুভেচ্ছান্তে,
💁‍♂️ মারুফ
-------------------------------------------"""
                
                # ওয়েব স্ক্রিনে কোড আকারে দেখানো যাতে সহজে কপি করা যায়
                st.code(msg, language=None)
                
    except Exception as e:
        st.error(f"ফাইল প্রসেস করতে সমস্যা হয়েছে। নিশ্চিত করুন যে কলামের নামগুলো ঠিক আছে। এরর: {e}")
