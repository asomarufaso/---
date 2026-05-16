import streamlit as st
import pandas as pd
import io

# পেজ কনফিগারেশন
st.set_page_config(page_title="ডাইনামিক ভাড়া রসিদ জেনারেটর", page_icon="🏡", layout="centered")

st.title("🏡 ডাইনামিক ভাড়া রসিদ জেনারেটর")
st.write("আপনার এক্সেল (.xlsx) ফাইলটি আপলোড করে স্ট্যাটাসসহ রসিদ জেনারেট করুন।")

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

# এক্সেল ফাইল আপলোডার
uploaded_file = st.file_uploader("📁 আপনার এক্সেল ফাইলটি আপলোড করুন", type=["xlsx"])

if uploaded_file is not None:
    try:
        df = pd.read_excel(uploaded_file)
        st.success(f"✅ মোট {len(df)} টি বিল ও রসিদ প্রসেস করার জন্য প্রস্তুত!")
        
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
                prev_due = float(row['Due'])      
                prev_adv = float(row['Advance'])  
                
                # Paid কলাম চেক করা
                paid_amount = float(row['Paid']) if 'Paid' in df.columns else 0.0

                # ক্যালকুলেশন ও রাউন্ডিং
                mas_bangla = months_map.get(month, month.capitalize())
                elec_raw = unit * rate
                elec_final = custom_round(elec_raw)
                
                # মোট বিল হিসাব
                total_bill = custom_round((rent + elec_raw + water + clean + prev_due) - prev_adv)
                
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

                # রসিদ ফরম্যাট
                msg = f"""╔══🏡✨ ভাড়ার রসিদ ✨🏡══╗
📍 ফ্ল্যাট নং: {to_bangla_formatted(flat).upper()}
📅 মাস: {mas_bangla} ২০২৬
╠══════════════════════╣
🏠 মোট ভাড়া            : {to_bangla_formatted(total_bill)}৳
💵 পরিশোধ করেছেন      : {to_bangla_formatted(paid_amount)}৳
📌 বকেয়া               : {due_display}
💰 অগ্রিম               : {adv_display}
╠══════════════════════╣
{status_msg}
🌿 আল্লাহ আপনার রিজিকে বরকত দান করুন।
╚════ 💁‍♂️ মারুফ ════╝"""
                
                # স্ক্রিনে রসিদ দেখানো
                st.code(msg, language=None)
                
    except Exception as e:
        st.error(f"❌ এরর: {e}। অনুগ্রহ করে নিশ্চিত করুন আপনার এক্সেল ফাইলের কলামগুলোর নাম ঠিক আছে কিনা।")
