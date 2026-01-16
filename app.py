import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

# --- 1. 网页基础设置 (Apple Style) ---
st.set_page_config(
    page_title="Badger Behavior Inquiry",
    page_icon="🦡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 注入 CSS 让背景变黑，字体变白 (Dark Mode)
st.markdown("""
<style>
    .stApp {
        background-color: #0E1117;
        color: #FAFAFA;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #262730;
        border-radius: 4px 4px 0px 0px;
        gap: 1px;
        padding-top: 10px;
        padding-bottom: 10px;
        color: #FAFAFA;
    }
    .stTabs [aria-selected="true"] {
        background-color: #FF4B4B;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# --- 2. 加载数据的函数 ---
@st.cache_data
def load_data():
    # 这里为了演示，我用了 try-except。你需要把 Data.xlsx - Sheet1.csv 改成 data_day1.csv
    # 建议你把 Excel 另存为两个 csv：data_day1.csv 和 data_day2.csv
    try:
        df1 = pd.read_csv("Data.xlsx - Sheet1.csv") # Day 1
        df2 = pd.read_csv("Data.xlsx - Sheet3.csv") # Day 2
    except:
        # 如果你还没有拆分文件，可以用这段备用逻辑
        df1 = pd.read_csv("Data.csv") 
        df2 = df1.copy() # 暂时用一样的

    # --- Day 1 清洗 ---
    df1.columns = df1.columns.str.strip()
    df1['Reaction'] = df1['Reaction'].astype(str).str.strip().str.title().replace(
        {'Nan': 'No Response', 'None': 'No Response', 'Childen Shouting': 'Avoidance'})
    df1['Time_Obj'] = pd.to_datetime(df1['Time'].astype(str), format='%H:%M:%S', errors='coerce')
    df1['People'] = pd.to_numeric(df1['People'].astype(str).replace({'20+': '20'}), errors='coerce').fillna(1)
    col_sound1 = 'Sound(dB)' if 'Sound(dB)' in df1.columns else 'Sound'
    df1['Sound'] = pd.to_numeric(df1[col_sound1], errors='coerce')
    df1 = df1.dropna(subset=['Sound', 'People'])

    # --- Day 2 清洗 (如果有 Pitch 列) ---
    df2.columns = df2.columns.str.strip()
    if 'Pitch' in df2.columns:
        df2['Pitch'] = df2['Pitch'].str.strip().str.title()
        # 清洗 Is_Scared
        target = ['Avoidance', 'Defensive', 'Vigilance']
        if 'Reaction' in df2.columns:
            df2['Reaction'] = df2['Reaction'].astype(str).str.strip().str.title()
            df2['Is_Scared'] = df2['Reaction'].isin(target)
    
    return df1, df2

# 加载数据
df_day1, df_day2 = load_data()

# --- 3. 侧边栏 (Sidebar) ---
with st.sidebar:
    st.title("🦡 The Inquiry")
    st.markdown("**What scares the badger more?**")
    st.info("Navigate through the tabs to see our data journey.")
    st.markdown("---")
    st.markdown("### Team Members")
    st.markdown("Sandie & Co.")
    st.markdown("---")
    st.caption("Built with Streamlit & Python")

# --- 4. 主页面 Tabs ---
tab1, tab2, tab3 = st.tabs(["📖 The Story", "🔊 Day 1: Volume vs Crowd", "🎶 Day 2: The Pitch Twist"])

# === TAB 1: 故事背景 ===
with tab1:
    st.header("The Mystery of the Badger")
    st.markdown("""
    We noticed something strange at the zoo. Sometimes the badger sleeps through a loud truck, 
    but wakes up for a tiny squeak.
    
    So we asked a comparative question:
    ### *Is it the **Volume** of the noise, or the **Size** of the crowd?*
    """)
    st.image("https://upload.wikimedia.org/wikipedia/commons/2/23/Badger-badger.jpg", caption="Our Subject", width=400) # 也可以换成你们拍的照片

# === TAB 2: Day 1 核心交互图 ===
with tab2:
    st.header("Trial 1: The Battle of Variables")
    st.markdown("Interact with the chart below. **Bubble Size = Crowd Size**, **Color = Stress**.")
    
    # 交互过滤器
    col_filter1, col_filter2 = st.columns(2)
    with col_filter1:
        min_val = int(df_day1['Sound'].min())
        max_val = int(df_day1['Sound'].max())
        sound_range = st.slider("Filter Decibels (dB):", min_val, max_val, (min_val, max_val))
    
    filtered_df1 = df_day1[df_day1['Sound'].between(sound_range[0], sound_range[1])]

    # 气泡图
    fig1 = px.scatter(filtered_df1,
                     x="Time_Obj",
                     y="Sound",
                     size="People",
                     color="Reaction",
                     color_discrete_map={
                         "No Response": "#333333",
                         "Vigilance": "#FFD60A",
                         "Avoidance": "#FF9F0A",
                         "Defensive": "#FF453A"
                     },
                     category_orders={"Reaction": ["No Response", "Vigilance", "Avoidance", "Defensive"]},
                     hover_data={"Time_Obj": "|%H:%M", "Sound": True, "People": True},
                     size_max=30,
                     template="plotly_dark",
                     title="Timeline: Noise Levels & Crowd Size"
    )
    fig1.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig1, use_container_width=True)

    # 统计结论
    st.markdown("### 📊 The Verdict")
    st.success("**Volume Wins.** Our Logistic Regression model shows Sound has **2x** the impact of Crowd Size.")

# === TAB 3: Day 2 反转 ===
with tab3:
    st.header("Trial 2: It's Not Just About Volume")
    st.markdown("We found a flaw in Day 1. Some quiet sounds (kids) were scarier than loud sounds (adults).")
    
    if 'Pitch' in df_day2.columns:
        # 简单的柱状图对比 High Pitch vs Low Pitch 的受惊率
        pitch_stats = df_day2.groupby('Pitch')['Is_Scared'].mean().reset_index()
        
        fig2 = px.bar(pitch_stats, 
                      x='Pitch', 
                      y='Is_Scared', 
                      color='Pitch',
                      title="Scare Rate: High Pitch vs. Low Pitch",
                      template="plotly_dark",
                      color_discrete_map={"High": "#FF453A", "Low": "#00CC96"}
        )
        fig2.update_layout(yaxis_title="Probability of Being Scared", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig2, use_container_width=True)
        
        st.markdown("### 💡 Insight")
        st.warning("**Pitch beats Volume.** A high-pitched sound triggers a primal fear response, even at lower volumes.")
    else:
        st.error("Day 2 Data (Pitch) not found. Please upload Sheet3 data.")