import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- 1. 页面配置 (Apple Dark Mode 风格) ---
st.set_page_config(
    page_title="Badger Behavior Inquiry",
    page_icon="🦡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 注入 CSS 让界面更丝滑、字体更好看
st.markdown("""
<style>
    .stApp { background-color: #000000; color: #FFFFFF; }
    h1, h2, h3 { font-family: 'Helvetica Neue', sans-serif; font-weight: 700; }
    .stMetric { background-color: #1c1c1e; padding: 15px; border-radius: 12px; border: 1px solid #333; }
    /* 调整 Tab 样式 */
    .stTabs [data-baseweb="tab-list"] { gap: 20px; }
    .stTabs [data-baseweb="tab"] { height: 50px; white-space: pre-wrap; background-color: #1c1c1e; border-radius: 10px; color: #fff; }
    .stTabs [aria-selected="true"] { background-color: #0A84FF; color: white; }
</style>
""", unsafe_allow_html=True)

# --- 2. 数据加载函数 (读取你的真实数据) ---
@st.cache_data
def load_data():
    df = None
    # 自动尝试读取 Excel 或 CSV
    try:
        df = pd.read_excel("Data.xlsx") # 优先读 Excel
    except:
        try:
            df = pd.read_csv("Data.csv") # 备选读 CSV
        except:
            pass
            
    if df is not None:
        # 简单清洗数据，防止报错
        # 假设列名大概是 Time, Sound, People, Reaction, Pitch
        # 这里做一些标准化处理
        df.columns = df.columns.str.strip() # 去除空格
        return df
    else:
        return None

df = load_data()

# --- 3. 侧边栏导航 (基于 Outline) ---
with st.sidebar:
    st.title("🦡 Navigation")
    # 对应 Outline 的各个 Part
    section = st.radio("Go to Section:", [
        "Part 1: The Intro", 
        "Part 2: The Hypothesis", 
        "Part 3: Data Story (Day 1)", 
        "Part 4: The Twist (Pitch)", 
        "Part 5: Behavioral Radar",
        "Part 6: Conclusion"
    ])

# ==========================================
# PART 1: INTRODUCTION [Outline Part 1 & 2]
# ==========================================
if section == "Part 1: The Intro":
    st.title("The Invisible Stress: Decoding the Badger's World")
    st.caption("An Interactive Inquiry into Animal Welfare & Visitor Experience")
    
    # [Outline Source 6] Video placeholder
    st.video("https://www.youtube.com/watch?v=A35X-pX6N4M") # 这里可以换成你拍的獾的视频链接
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 🕵️‍♀️ The Why")
        st.write("""
        **Subject:** American Badger (Taxidea taxus)
        **Observation:** We noticed he sleeps through loud trucks but wakes up for whispers.
        **Goal:** To understand how *Sound* vs. *Crowd Size* affects his stress levels.
        """) # [Outline Source 3]
    with col2:
        st.markdown("### 🛠️ The Setup")
        st.write("""
        * **Tools:** Decibel Meter, Python Script, Ethogram.
        * **Method:** 2-Day Observation at The Living Desert Zoo.
        """) # [Outline Source 13]

    st.info("👇 Please utilize the sidebar to navigate through our findings.")

# ==========================================
# PART 2: THE HYPOTHESIS [Outline Part 3]
# ==========================================
elif section == "Part 2: The Hypothesis":
    st.title("The Hypothesis")
    st.markdown("Before analyzing the data, we asked two questions:")
    
    col1, col2 = st.columns(2)
    with col1:
        # [Outline Source 9]
        st.metric(label="Hypothesis A", value="Volume (dB)", delta="Is louder scarier?")
        st.write("We expected high decibels to trigger immediate stress.")
    
    with col2:
        # [Outline Source 10]
        st.metric(label="Hypothesis B", value="Crowd Size", delta="Are more people scarier?")
        st.write("We expected larger groups to cause more anxiety.")

# ==========================================
# PART 3: DATA STORY (DAY 1) [Outline Part 5]
# ==========================================
elif section == "Part 3: Data Story (Day 1)":
    st.title("Day 1: The Volume Trap")
    st.markdown("We visualized the relationship between **Sound**, **Crowd**, and **Reaction**.")
    
    if df is not None:
        # 交互式滑块 [Outline Source 16]
        min_sound = int(df['Sound'].min()) if 'Sound' in df.columns else 40
        max_sound = int(df['Sound'].max()) if 'Sound' in df.columns else 90
        
        sound_filter = st.slider("Filter by Sound Level (dB):", min_sound, max_sound, (min_sound, max_sound))
        
        # 筛选数据
        filtered_df = df
        if 'Sound' in df.columns:
            filtered_df = df[(df['Sound'] >= sound_filter[0]) & (df['Sound'] <= sound_filter[1])]

        # 气泡图：展示 "The Nuance" [Outline Source 16]
        if 'Time' in df.columns and 'Sound' in df.columns:
            fig = px.scatter(filtered_df, 
                             x="Time", 
                             y="Sound", 
                             size="People" if "People" in filtered_df.columns else None,
                             color="Reaction" if "Reaction" in filtered_df.columns else None,
                             title="Interactive Timeline: Sound vs. Reaction",
                             template="plotly_dark",
                             color_discrete_map={
                                 "No Response": "#333333", 
                                 "Vigilance": "#FFD60A", 
                                 "Defensive": "#FF453A"
                             },
                             hover_data=df.columns)
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("""
            **Observation:** * Large bubbles (Crowds) didn't always mean red dots (Stress).
            * Some red dots appeared at low volume. **Why?** -> Go to Part 4.
            """)
    else:
        st.error("⚠️ Data file not found. Please verify 'Data.xlsx' is in your GitHub repo.")

# ==========================================
# PART 4: THE TWIST (PITCH) [Outline Part 6]
# ==========================================
elif section == "Part 4: The Twist (Pitch)":
    st.title("The Twist: Pitch Matters")
    st.markdown("### It's not just *how loud*, but *how high*.") # [Outline Source 19]
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.warning("🚛 Low Pitch (Trucks/Men)")
        st.markdown("**85 dB (Loud)** -> `Reaction: None`")
        st.caption("Evolutionary: Low frequency often means harmless thunder or wind.")
        
    with col2:
        st.error("👶 High Pitch (Kids/Screech)")
        st.markdown("**55 dB (Quiet)** -> `Reaction: ALERT!`")
        st.caption("Evolutionary: High frequency mimics predators or distress calls.")
    
    # [Outline Source 21] Recovery Lag
    st.markdown("---")
    st.subheader("⏳ The 'Recovery Lag' Phenomenon")
    st.info("Once stressed by a high-pitched sound, the badger remained in 'High Alert' even after the sound stopped.")
    
    # 模拟 Hysteresis 曲线 (示意图)
    x_data = list(range(10))
    y_stress = [1, 1, 8, 8, 7, 6, 5, 4, 2, 1] # 受到刺激后缓慢下降
    fig_lag = px.line(x=x_data, y=y_stress, title="Stress Recovery Hysteresis", labels={'x':'Time (min)', 'y':'Stress Level'})
    fig_lag.update_traces(line_color='#FF453A')
    st.plotly_chart(fig_lag, use_container_width=True)

# ==========================================
# PART 5: BEHAVIORAL RADAR [Outline Part 8 & Radar System]
# ==========================================
elif section == "Part 5: Behavioral Radar":
    st.title("The Badger's 'Radar' System")
    st.markdown("Through observation, we mapped the badger's sensory hierarchy.")
    
    # 使用 Tab 来做你的 Radar System 归纳 [Outline Source 33]
    tab1, tab2, tab3 = st.tabs(["👁️ Vision (Motion)", "🐾 Vibration (Seismic)", "🐕 Digging (Language)"])
    
    with tab1:
        st.header("Motion-Based Vision")
        # [Outline Source 36-38]
        st.write("Badgers are myopic (nearsighted). They rely heavily on **detecting motion**.")
        st.image("https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjEx.../giphy.gif", caption="Visualizing Motion Tracking (Placeholder)") 
        st.warning("Insight: If you stand perfectly still, you are invisible.")

    with tab2:
        st.header("Seismographic Paws")
        # [Outline Source 39-40]
        st.write("They are sensitive to **ground vibrations**.")
        st.progress(90, text="Sensitivity to Heavy Footsteps")
        st.caption("Heavy footsteps alert them before sound does.")

    with tab3:
        st.header("Digging as Language")
        # [Outline Source 50-52]
        c1, c2 = st.columns(2)
        with c1:
            st.success("Slow, Rhythmic Digging")
            st.markdown("= **Nesting (Comfort)**")
        with c2:
            st.error("Frantic, Erratic Digging")
            st.markdown("= **Displacement (Stress)**")

# ==========================================
# PART 6: CONCLUSION [Outline Part 9]
# ==========================================
elif section == "Part 6: Conclusion":
    st.title("Conclusion & Solutions")
    st.balloons() # 撒花动画，庆祝项目完成
    
    st.markdown("### 📋 Actionable Plan for the Zoo") # [Outline Source 31]
    
    st.checkbox("🚫 **Quiet Zones:** Signs reminding visitors to lower pitch, not just volume.")
    st.checkbox("🚧 **Visual Barriers:** Reduce motion triggers near the glass.")
    st.checkbox("🌿 **Scattered Feeding:** Continue purely for enrichment.")
    
    st.markdown("---")
    st.markdown("### Thank You!")
    st.caption("Project by Sandie | Winter Internship 2026")
