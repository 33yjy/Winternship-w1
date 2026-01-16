import streamlit as st
import time

# --- 1. 页面基础设置 (伪装成苹果风) ---
st.set_page_config(
    page_title="Badger: The Invisible Stress",
    page_icon="🦡",
    layout="wide",
    initial_sidebar_state="collapsed" # 默认收起侧边栏，更像网页
)

# 注入 CSS (这是让它变“高级”的关键，去掉了Streamlit原本的丑边框)
st.markdown("""
<style>
    /* 全局黑底白字 */
    .stApp {
        background-color: #000000;
        color: #FFFFFF;
    }
    /* 标题样式 */
    h1 {
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: 700;
        font-size: 3.5rem !important;
        background: -webkit-linear-gradient(#eee, #333);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    /* 卡片样式 */
    .stMetric {
        background-color: #1c1c1e;
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #333;
    }
    /* 按钮样式 */
    .stButton>button {
        border-radius: 20px;
        background-color: #0A84FF; 
        color: white;
        border: none;
        padding: 10px 24px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# --- 2. 侧边栏导航 (模拟你的Outline结构) ---
with st.sidebar:
    st.title("Navigation")
    section = st.radio("Go to:", 
        ["Intro: The Invisible Stress", 
         "Hypothesis: Sound vs Crowd", 
         "Data: The Discovery", 
         "Insights: Radar System", 
         "Conclusion: Action Plan"])

# --- 3. 页面内容 (Scrollytelling 滚动叙事) ---

# === SECTION 1: INTRO ===
if section == "Intro: The Invisible Stress":
    # 模拟全屏大标题
    st.container()
    st.markdown("# The Invisible Stress")
    st.markdown("### Decoding the Badger's World: An Interactive Inquiry")
    st.markdown("---")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("""
        **Subject:** The Badger (Taxidea taxus)  
        **Location:** The Living Desert Zoo  
        **Problem:** Why does he wake up for a whisper but sleep through a truck?
        """)
        st.info("👇 Scroll down to explore our investigation.")
    with col2:
        # 这里用了一个占位图，以后可以换成你的Badger视频
        st.image("https://upload.wikimedia.org/wikipedia/commons/2/23/Badger-badger.jpg", caption="Our Subject in 'Torpor' mode")

# === SECTION 2: HYPOTHESIS ===
elif section == "Hypothesis: Sound vs Crowd":
    st.markdown("# The Hypothesis")
    st.write("We started with two simple questions. Click to explore.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🔊 Is it Volume?")
        st.write("Does loud noise (dB) directly correlate to stress?")
        if st.button("Test Volume Hypothesis"):
            with st.status("Analyzing Decibel Data..."):
                time.sleep(1) # 假装在计算
                st.write("Loading CSV...")
                time.sleep(0.5)
                st.write("Running Regression...")
            st.error("Result: Only PARTIALLY true.")
            
    with col2:
        st.markdown("### 👥 Is it the Crowd?")
        st.write("Do more people mean more fear?")
        if st.button("Test Crowd Hypothesis"):
            with st.status("Counting People..."):
                time.sleep(1)
            st.warning("Result: Weak Correlation found.")

# === SECTION 3: DATA STORY (The Twist) ===
elif section == "Data: The Discovery":
    st.markdown("# The Data Twist: It's Pitch, Not Volume")
    
    # 模拟你Outline里的 Part 5 & 6
    st.markdown("We found an **'Outlier'**. Look at this comparison:")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 🚚 Scenario A: The Truck")
        st.metric(label="Volume", value="85 dB", delta="High Volume")
        st.metric(label="Pitch", value="Low Frequency", delta_color="off")
        st.success("Badger Reaction: 😴 Sleeping (No Stress)")
        
    with col2:
        st.markdown("### 🧒 Scenario B: The Child")
        st.metric(label="Volume", value="55 dB", delta="-30 dB (Quieter)", delta_color="inverse")
        st.metric(label="Pitch", value="High Frequency (Screech)", delta="Danger!")
        st.error("Badger Reaction: 👁️ ALERT (High Stress)")
    
    st.markdown("---")
    st.markdown("> **Findings:** The badger's hearing is evolutionarily tuned to *high-frequency threats* (predators), not just loudness.")

# === SECTION 4: INSIGHTS (Interactive Radar) ===
elif section == "Insights: Radar System":
    st.markdown("# The 'Radar' System")
    st.write("Interact with the sensors to see how the badger perceives the world.")
    
    # 用 tab 模拟你的雷达交互
    tab1, tab2, tab3 = st.tabs(["👁️ Vision", "🐾 Vibration", "👂 Hearing"])
    
    with tab1:
        st.markdown("### Motion-Based Vision")
        st.warning("Fun Fact: Badgers are myopic (nearsighted).")
        st.write("They rely on **MOTION**. If you stand still, you are invisible.")
        
    with tab2:
        st.markdown("### Seismographic Paws")
        st.write("They feel footsteps before they hear them.")
        st.progress(90, text="Vibration Sensitivity Level")
        
    with tab3:
        st.markdown("### Frequency Tuned Hearing")
        st.line_chart([10, 20, 80, 40, 90, 20], height=200) # 假数据图表
        st.caption("Spikes indicate reaction to High Pitch sounds")

# === SECTION 5: CONCLUSION ===
elif section == "Conclusion: Action Plan":
    st.markdown("# Solutions for the Zoo")
    
    col1, col2 = st.columns(2)
    with col1:
        st.success("✅ Proposal 1: Quiet Zones")
        st.write("Signs reminding visitors to lower pitch, not just volume.")
    with col2:
        st.success("✅ Proposal 2: Visual Barriers")
        st.write("Reducing 'Motion' triggers near the glass.")

    st.markdown("---")
    st.markdown("### Thank you")