import os
import random
from google import genai

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

topics = [
    "জীবনের বাস্তব কোনো ছোট অভিজ্ঞতা বা প্রতিদিনের কোনো উপলব্ধি (Storytelling)",
    "বাংলাদেশের বর্তমান সময়ের সাধারণ মানুষের জীবনযাত্রা বা চলমান কোনো বিষয় নিয়ে ব্যক্তিগত ও যৌক্তিক বিশ্লেষণ",
    "ডিজিটাল কাজ, ওয়েবসাইট বা কন্টেন্ট ক্রিয়েশন করতে গিয়ে শেখা দারুণ কোনো বাস্তব অভিজ্ঞতা বা টিপস",
    "ফ্রেন্ডলিস্টের মানুষদের কাছে কোনো বিষয়ে পরামর্শ চাওয়া বা সহজ কোনো প্রশ্ন করা যাতে সবাই কমেন্ট করতে আগ্রহ পায়",
    "মাত্র ২-৩ লাইনের খুব গভীর এবং ভাবনা জাগানিয়া একটি ছোট স্ট্যাটাস"
]

selected_topic = random.choice(topics)

prompt = f"""
তুমি একজন সচেতন, বাস্তববাদী মানুষের ব্যক্তিগত ফেইসবুক প্রোফাইলের জন্য একটি স্ট্যাটাস লিখবে। 
আজকের বিষয়: {selected_topic}

লেখার নিয়মাবলী:
১. লেখাটি একদম স্বাভাবিক মানুষের মতো হতে হবে। কোনো কর্পোরেট ভাব, কৃত্রিমতা বা রোবটিক ভাষা থাকা যাবে না। মনে হতে হবে একজন মানুষ তার বন্ধুদের সাথে নিজের মনের কথা শেয়ার করছে।
২. লেখার ভেতরে কোনোভাবেই লম্বা ড্যাশ বা এম-ড্যাশ ব্যবহার করা যাবে না।
৩. "এটা কি শুধুই..., নাকি...?" এই ধরণের গতানুগতিক বাক্য একদমই ব্যবহার করা যাবে না।
৪. ফেইসবুক অ্যালগরিদম যেসব সংবেদনশীল বা নেতিবাচক শব্দ পছন্দ করে না (যেমন: মৃ/ত্যু, হ/ত্যা, দু/র্নীতি, রা/জনীতি, আ/ন্দোলন, বা/তিল, ব/ন্ধ ইত্যাদি), সেগুলোর মাঝে অবশ্যই স্ল্যাশ (/) ব্যবহার করবে।
৫. কোনো হ্যাশট্যাগ (#) ব্যবহার করবে না এবং লেখার শুরুতে বা শেষে কোনো অতিরিক্ত কথা লিখবে না। শুধু মূল স্ট্যাটাসটুকু লিখবে।
"""

# যে মডেলগুলো একে একে চেক করবে
models_to_try = [
    "gemini-3-flash-preview",
    "gemini-3.0-flash",
    "gemini-2.5-flash",
    "gemini-2.0-flash",
    "gemini-flash-latest"
]

post_text = None

for model_name in models_to_try:
    try:
        print(f"Trying model: {model_name}")
        response = client.models.generate_content(
            model=model_name,
            contents=prompt,
        )
        post_text = response.text.strip()
        print(f"Success with {model_name}!")
        break
    except Exception as e:
        print(f"Model {model_name} failed: {e}")

# ওপরের তালিকায় না পেলে অ্যাকাউন্টের চালু থাকা যেকোনো flash মডেল নিজে খুঁজে নেবে
if not post_text:
    for m in client.models.list():
        if "flash" in m.name.lower() and "tts" not in m.name.lower() and "image" not in m.name.lower():
            try:
                print(f"Auto-detected model: {m.name}")
                response = client.models.generate_content(
                    model=m.name,
                    contents=prompt,
                )
                post_text = response.text.strip()
                print(f"Success with {m.name}!")
                break
            except Exception as e:
                continue

if not post_text:
    raise Exception("Could not generate post. Please check your GEMINI_API_KEY.")

with open("latest_post.txt", "w", encoding="utf-8") as f:
    f.write(post_text)

print("Post saved to latest_post.txt successfully!")
