import streamlit as st
import streamlit.components.v1 as components

# 1. 페이지 기본 설정
st.set_page_config(page_title="Edge-AI 차단 시스템 시연", layout="wide")

st.markdown("""
    <style>
    .main-title { font-size: 28px; font-weight: bold; color: #1E3A8A; }
    .sub-title { font-size: 14px; color: #4B5563; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<p class="main-title">⚡ Edge-AI 기반 아크 플래시 사전 차단 시스템 (60 FPS 초고속 데모)</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">본 화면은 발표 시연용 초고속 브라우저 렌더링 엔진(HTML5 Canvas)으로 구동됩니다.</p>', unsafe_allow_html=True)
st.markdown("---")

# 2. 사이드바 제어판 (발표 시나리오 세팅)
st.sidebar.header("🕹️ 데모 시나리오 설정")
system_mode = st.sidebar.selectbox(
    "운영 모드 선택",
    ["정식 가동 (실시간 초고속 회로 차단)", "운영 초기 (스마트워치 알람 경고)"]
)

st.sidebar.markdown("---")
st.sidebar.subheader("💡 발표 시연 가이드")
st.sidebar.info(
    "오른쪽 화면의 **[▶️ 실시간 계통 감시 시작]** 버튼을 누르면 부드러운 스캔이 시작됩니다.\n\n"
    "**1초~3초 사이에 랜덤하게** 아크 전조가 발생하며, "
    "사고 발생 순간 **AI 엔진의 정밀 차단 소요 시간**이 화면에 실시간 표시됩니다."
)

# 3. 메인 화면 레이아웃 및 가동 버튼
run_btn = st.button("🚀 실시간 계통 감시 및 AI 추론 시작 (Live Demonstration)", type="primary")

# 4. 랜덤 타이밍 및 차단 시간 측정 로직이 주입된 자바스크립트 엔진
if run_btn:
    mode_flag = "breaker" if system_mode == "정식 가동 (실시간 초고속 회로 차단)" else "watch"

    # VS Code에서 초록색/회색 문자열 박스로 보여도 정상 작동하는 구역입니다!
    html_code = f"""
    <div id="simulation-panel" style="background-color: #111827; padding: 20px; border-radius: 12px; font-family: sans-serif; color: white;">
        
        <div id="status-banner" style="background-color: #065F46; padding: 15px; border-radius: 8px; margin-bottom: 20px; font-weight: bold; font-size: 16px; border-left: 5px solid #10B981; transition: all 0.3s;">
            🟢 [LIVE] 초고속 샘플링 가동 중... AI가 용접기/인버터 정상 노이즈 필터링 완료 (안정 상태)
        </div>

        <div style="display: flex; gap: 20px;">
            <div style="flex: 1; background: #1F2937; padding: 10px; border-radius: 8px;">
                <div style="font-size: 14px; font-weight: bold; margin-bottom: 5px; color: #9CA3AF;">📈 실시간 전류 스코프 (Time Domain)</div>
                <canvas id="timeCanvas" width="500" height="300" style="width:100%; background:#05070A; border-radius:4px;"></canvas>
            </div>
            <div style="flex: 1; background: #1F2937; padding: 10px; border-radius: 8px;">
                <div style="font-size: 14px; font-weight: bold; margin-bottom: 5px; color: #9CA3AF;">📊 Edge단 초고속 주파수 분석 (FFT)</div>
                <canvas id="freqCanvas" width="500" height="300" style="width:100%; background:#05070A; border-radius:4px;"></canvas>
            </div>
        </div>
    </div>

    <script>
        const mode = "{mode_flag}";
        const tCanvas = document.getElementById('timeCanvas');
        const fCanvas = document.getElementById('freqCanvas');
        const tCtx = tCanvas.getContext('2d');
        const fCtx = fCanvas.getContext('2d');
        const banner = document.getElementById('status-banner');

        // [핵심 업데이트] 시간 측정 변수 세팅
        const startTime = Date.now();
        // 1000ms(1초)에서 3000ms(3초) 사이의 랜덤한 폭발 시간 설정
        const triggerTime = 1000 + Math.random() * 2000; 
        // Edge AI 및 논리회로 연산 + 차단기 개방까지 걸린 가상 정밀 시간 (1.15ms ~ 2.65ms 사이 랜덤 산출)
        const processingTime = (1.15 + Math.random() * 1.50).toFixed(2);

        let frame = 0;
        let animationId;

        // 계측기 눈금 선(그리드) 그리기
        function drawGrid(ctx, w, h) {{
            ctx.strokeStyle = '#1E293B';
            ctx.lineWidth = 1;
            for(let y = 30; y < h; y += 30) {{
                ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(w, y); ctx.stroke();
            }}
            for(let x = 50; x < w; x += 50) {{
                ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, h); ctx.stroke();
            }}
        }}

        // 60 FPS 브라우저 애니메이션 루프
        function animate() {{
            frame++;
            
            tCtx.clearRect(0, 0, tCanvas.width, tCanvas.height);
            fCtx.clearRect(0, 0, fCanvas.width, fCanvas.height);
            
            drawGrid(tCtx, tCanvas.width, tCanvas.height);
            drawGrid(fCtx, fCanvas.width, fCanvas.height);

            // 현재 흘러간 실제 시간 계산
            const elapsed = Date.now() - startTime;
            // 지정된 랜덤 타이밍이 지나면 아크 발생
            const isArc = elapsed >= triggerTime;

            // 1. 전류 스코프 파형 연산 및 시각화
            tCtx.lineWidth = 2;
            tCtx.strokeStyle = isArc ? '#EF4444' : '#3B82F6';
            tCtx.shadowBlur = isArc ? 10 : 4;
            tCtx.shadowColor = tCtx.strokeStyle;
            tCtx.beginPath();

            for(let x = 0; x < tCanvas.width; x++) {{
                let t = x * 0.05;
                let phase = frame * 0.15;
                
                let y = 150 + 60 * Math.sin(t * 0.3 - phase) + (Math.random() - 0.5) * 6;
                y += 8 * Math.sin(t * 1.5 - phase); 

                if (isArc) {{
                    y += 35 * Math.sin(t * 4.5) * Math.exp(- (x%100) * 0.02);
                }}

                if(x === 0) tCtx.moveTo(x, y);
                else tCtx.lineTo(x, y);
            }}
            tCtx.stroke();
            tCtx.shadowBlur = 0;

            // 2. 주파수 스펙트럼(FFT) 그래프 연산 및 시각화
            fCtx.fillStyle = isArc ? '#EF4444' : '#10B981';
            fCtx.fillRect(60, tCanvas.height - 200, 15, 200); 
            fCtx.fillRect(180, tCanvas.height - 40, 12, 40);
            
            for(let i = 20; i < fCanvas.width; i += 15) {{
                if(i !== 60 && i !== 180 && i !== 380) {{
                    let h = 5 + Math.random() * 15;
                    fCtx.fillRect(i, fCanvas.height - h, 8, h);
                }}
            }}

            // 아크 발생 시 프리즈 및 결과 화면 출력
            if (isArc) {{
                let arcH = 180 + Math.random() * 20;
                fCtx.fillStyle = '#EF4444';
                fCtx.shadowBlur = 10;
                fCtx.shadowColor = '#EF4444';
                fCtx.fillRect(380, fCanvas.height - arcH, 15, arcH);
                fCtx.shadowBlur = 0;

                // 측정된 실제 랜덤 트리거 도달 시간초 계산 (소수점 둘째자리까지)
                const exactTriggerSec = (triggerTime / 1000).toFixed(2);

                if (mode === "breaker") {{
                    banner.style.backgroundColor = "#991B1B";
                    banner.style.borderLeftColor = "#EF4444";
                    banner.innerHTML = `💥 [CRITICAL] 가동 후 ${{exactTriggerSec}}초 시점, 아크 플래시 폭발 위험 전조 감지!<br>
                    <span style="font-size:13px; font-weight:normal; color:#FCA5A5;">
                    • AI 분석 엔진 판정: 4.8kHz 영역 비정상 고주파 이상 패턴 매칭 완료<br>
                    • 시스템 제어 명령: [물리 차단기 격리 트리거 즉시 개방]<br>
                    • <b>폭발 전조 감지 후 차단 완료까지 걸린 시간: <span style="color:#FFF; font-weight:bold; font-size:14px;">${{processingTime}} ms</span> (골든타임 이내 원천 차단 성공)</b>
                    </span>`;
                    document.getElementById('simulation-panel').style.border = "3px solid #EF4444";
                }} else {{
                    banner.style.backgroundColor = "#92400E";
                    banner.style.borderLeftColor = "#F59E0B";
                    banner.innerHTML = `🚨 [WARNING] 가동 후 ${{exactTriggerSec}}초 시점, 배전반 내 미세 아크 불꽃 패턴 발생<br>
                    <span style="font-size:13px; font-weight:normal; color:#FDE68A;">
                    • 현재 모드: 안전 검증 및 데이터 최적화를 위한 '초기 모니터링 모드'<br>
                    • 시스템 제어 명령: 무작위 라인 스톱 방지를 위해 차단 유보<br>
                    • <b>이상 신호 포착 및 스마트워치 원격 알람 발송 완료 소요 시간: <span style="color:#FFF; font-weight:bold; font-size:14px;">${{processingTime}} ms</span></b>
                    </span>`;
                    document.getElementById('simulation-panel').style.border = "3px solid #F59E0B";
                }}
                
                cancelAnimationFrame(animationId);
                return;
            }}

            animationId = requestAnimationFrame(animate);
        }}

        animate();
    </script>
    """
    components.html(html_code, height=450)
else:
    st.info("⚡ 시스템 가동 준비 완료. 위의 가동 버튼을 누르면 끊김 없는 실시간 시뮬레이션 데모가 시작됩니다.")