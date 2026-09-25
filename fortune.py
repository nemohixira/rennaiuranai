import streamlit as st
import base64

# ページの設定
st.set_page_config(page_title="🔮 恋愛占い　逆ピラミット型", page_icon="🔮", layout="centered")

# --- 🔮 占いロジック ---
def char_to_number(char):
    vowels = {
        'あ': 1, 'い': 2, 'う': 3, 'え': 4, 'お': 5, 'か': 1, 'き': 2, 'く': 3, 'け': 4, 'こ': 5,
        'さ': 1, 'し': 2, 'す': 3, 'せ': 4, 'そ': 5, 'た': 1, 'ち': 2, 'つ': 3, 'て': 4, 'と': 5,
        'な': 1, 'に': 2, 'ぬ': 3, 'ね': 4, 'の': 5, 'は': 1, 'ひ': 2, 'ふ': 3, 'へ': 4, 'ほ': 5,
        'ま': 1, 'み': 2, 'む': 3, 'め': 4, 'も': 5, 'や': 1,         'ゆ': 3,        'よ': 5,
        'ら': 1, 'り': 2, 'る': 3, 'れ': 4, 'ろ': 5, 'わ': 1, 'ゐ': 2,         'ゑ': 4, 'を': 5,
        'ん': 1, 'が': 1, 'ぎ': 2, 'ぐ': 3, 'げ': 4, 'ご': 5, 'ざ': 1, 'じ': 2, 'ず': 3, 'ぜ': 4, 
        'ぞ': 5, 'だ': 1, 'ぢ': 2, 'づ': 3, 'で': 4, 'ど': 5, 'ば': 1, 'び': 2, 'ぶ': 3, 'べ': 4, 
        'ぼ': 5, 'ぱ': 1, 'ぴ': 2, 'ぷ': 3, 'ぺ': 4, 'ぽ': 5
    }
    return vowels.get(char, 0)

def name_to_number_list(name):
    return [char_to_number(c) for c in name if char_to_number(c) != 0]

def interleave_lists(list1, list2):
    result = []
    for a, b in zip(list1, list2):
        result.extend([a, b])
    result.extend(list1[len(list2):])
    result.extend(list2[len(list1):])
    return result

def reduce_to_final_two(nums):
    steps = [nums[:]]
    while len(nums) > 2:
        nums = [(nums[i] + nums[i+1]) % 10 for i in range(len(nums)-1)]
        steps.append(nums[:])
    return nums, steps

# --- 🚀 URL共有用の暗号化ロジック ---
def encode_result(name1, name2, score):
    raw_text = f"{name1},{name2},{score}"
    encoded_bytes = base64.urlsafe_b64encode(raw_text.encode('utf-8'))
    return encoded_bytes.decode('utf-8').replace("=", "")

def decode_result(code):
    try:
        rem = len(code) % 4
        if rem > 0:
            code += "=" * (4 - rem)
        decoded_bytes = base64.urlsafe_b64decode(code.encode('utf-8'))
        raw_text = decoded_bytes.decode('utf-8')
        name1, name2, score = raw_text.split(',')
        return name1, name2, int(score)
    except:
        return None

# --- 🖥️ 画面表示の制御 ---
st.title("🔮 恋愛占い　逆ピラミット型")
st.caption("名前を数字に変えて、2人の相性をピラミッドで占います。")

# URLパラメータの読み込み
share_code = st.query_params.get("share", None)

# ─── 💌 モード1: 共有された結果を表示する画面 ───
if share_code:
    decoded = decode_result(share_code)
    if decoded:
        name1, name2, score = decoded
        st.success("💌 共有された占い結果が届いています！")
        
        # 綺麗に中央寄せするスタイル
        st.markdown(f"""
            <div style="text-align: center; margin: 20px 0;">
                <h2 style="color: #FF4B4B;">💖 {name1} × {name2}</h2>
                <h3 style="font-size: 28px;">ふたりの相性は... 🎉 <span style="font-size: 40px; font-weight: bold; color: #FF4B4B;">{score}%</span> 🎉</h3>
            </div>
        """, unsafe_allow_html=True)
        
        # 再度占うボタン
        if st.button("自分も新しく占う 🎯", use_container_width=True):
            st.query_params.clear()
            st.rerun()
    else:
        st.error("共有コードが正しくありません。")

# ─── 🎯 モード2: 通常の入力画面 ───
else:
    name1 = st.text_input("🧑‍💼 あなたの名前（ひらがな）", placeholder="例：たろう")
    name2 = st.text_input("💖 相手の名前（ひらがな）", placeholder="例：はなこ")

    if st.button("相性を占う！ ✨", type="primary", use_container_width=True):
        if name1 and name2:
            n1 = name_to_number_list(name1)
            n2 = name_to_number_list(name2)
            combined = interleave_lists(n1, n2)
            
            if len(combined) < 2:
                st.error("ひらがなで正しく名前を入力してください。")
            else:
                final_two, steps = reduce_to_final_two(combined)
                score = int(f"{final_two[0]}{final_two[1]}")
                st.balloons()
                
                # 結果表示（中央寄せ）
                st.markdown(f"""
                    <div style="text-align: center; margin: 20px 0;">
                        <h2 style="font-size: 32px; color: #FF4B4B;">🎉 相性結果: {score}% 🎉</h2>
                    </div>
                """, unsafe_allow_html=True)
                
                st.write("### 📐 相性ピラミッド")
                
                pyramid_html = '<div style="text-align: center; font-family: monospace; line-height: 1.5; letter-spacing: 6px; font-size: 22px; background-color: #1e1e1e; padding: 25px; border-radius: 10px; color: #fff; box-shadow: inset 0 0 10px rgba(0,0,0,0.5);">'
                for row in steps:
                    line = ' '.join(str(n) for n in row)
                    pyramid_html += f'<div style="margin: 4px 0;">{line}</div>'
                pyramid_html += '</div>'
                
                st.markdown(pyramid_html, unsafe_allow_html=True)
                st.write("") 
                    
                # 🚀 共有リンク機能を完璧に修正
                code = encode_result(name1, name2, score)
                # あなたの公開URLとコードを完全にドッキングさせた本物のURLを作成
                full_share_url = f"https://streamlit.app{code}"
                
                st.warning("🔗 この結果を友達にシェアしよう！")
                st.write("下の入力欄の文字をぜんぶコピーして友達に送ってね：")
                # コピーしやすいようにテキスト入力欄に本物のURLを丸ごと表示
                st.text_input("コピー用URL", value=full_share_url, label_visibility="collapsed")
        else:
            st.error("両方の名前を入力してください。")
