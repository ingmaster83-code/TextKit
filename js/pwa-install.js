// PWA 설치 유도 스크립트 — 텍스트킷
(function() {
  let deferredPrompt = null;

  window.addEventListener('beforeinstallprompt', e => {
    e.preventDefault();
    deferredPrompt = e;
    const heroBtn = document.getElementById('heroInstallBtn');
    if (heroBtn) heroBtn.style.display = 'inline-flex';
  });

  window.addEventListener('appinstalled', () => {
    deferredPrompt = null;
    closePWABanner();
    const heroBtn = document.getElementById('heroInstallBtn');
    if (heroBtn) heroBtn.style.display = 'none';
  });

  document.addEventListener('DOMContentLoaded', () => {
    if (window.matchMedia('(display-mode: standalone)').matches) {
      const heroBtn = document.getElementById('heroInstallBtn');
      if (heroBtn) heroBtn.style.display = 'none';
      return;
    }
    const heroBtn = document.getElementById('heroInstallBtn');
    if (heroBtn) {
      heroBtn.addEventListener('click', () => {
        if (deferredPrompt) {
          deferredPrompt.prompt();
          deferredPrompt.userChoice.then(() => {
            deferredPrompt = null;
            heroBtn.style.display = 'none';
          });
        } else {
          alert('주소창 오른쪽의 설치 아이콘(⊕)을 클릭해 홈 화면에 추가하세요.');
        }
      });
    }
  });

  if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/sw.js').catch(() => {});
  }

  // 페이지 사용 후 배너 표시
  let bannerShown = false;
  document.addEventListener('DOMContentLoaded', () => {
    setTimeout(() => {
      if (!bannerShown) showPWABanner();
    }, 30000);
  });

  window.showPWABanner = function() {
    if (bannerShown) return;
    if (sessionStorage.getItem('pwa_shown')) return;
    if (window.matchMedia('(display-mode: standalone)').matches) return;

    const isIOS = /iPad|iPhone|iPod/.test(navigator.userAgent) && !window.MSStream;
    if (!isIOS && !deferredPrompt) return;

    bannerShown = true;
    sessionStorage.setItem('pwa_shown', '1');

    const btnHtml = (!isIOS && deferredPrompt)
      ? `<button class="pwa-btn-install" onclick="window.triggerPWAInstall()">설치하기</button>`
      : (isIOS ? `<span class="pwa-ios-hint">Safari 메뉴 → 홈 화면에 추가</span>` : '');

    const style = document.createElement('style');
    style.textContent = `
      #pwa-install-banner {
        position: fixed; bottom: 0; left: 0; right: 0; z-index: 9999;
        background: #1A1A2E; border-top: 3px solid #F59E0B;
        padding: 14px 16px; display: flex; align-items: center; gap: 12px;
        box-shadow: 0 -4px 20px rgba(0,0,0,0.3);
        animation: slideUp 0.3s ease;
        font-family: 'Noto Sans KR', -apple-system, sans-serif;
      }
      @keyframes slideUp { from { transform: translateY(100%); } to { transform: translateY(0); } }
      .pwa-banner-icon { font-size: 2rem; flex-shrink: 0; }
      .pwa-banner-text { flex: 1; }
      .pwa-banner-text strong { display: block; color: #fff; font-size: 0.95rem; }
      .pwa-banner-text span { color: rgba(255,255,255,0.7); font-size: 0.82rem; }
      .pwa-ios-hint { color: rgba(255,255,255,0.7); font-size: 0.82rem; }
      .pwa-btn-install {
        background: #F59E0B; color: #1A1A2E; border: none; border-radius: 8px;
        padding: 8px 18px; font-size: 0.88rem; font-weight: 700; cursor: pointer;
        white-space: nowrap; flex-shrink: 0; font-family: inherit;
      }
      .pwa-btn-install:hover { background: #D97706; }
      .pwa-btn-close {
        background: none; border: none; color: rgba(255,255,255,0.5);
        font-size: 1.2rem; cursor: pointer; padding: 4px; flex-shrink: 0;
      }
      .pwa-btn-close:hover { color: #fff; }
    `;
    document.head.appendChild(style);

    const banner = document.createElement('div');
    banner.id = 'pwa-install-banner';
    banner.innerHTML = `
      <div class="pwa-banner-icon">✏️</div>
      <div class="pwa-banner-text">
        <strong> 바로가기 추가</strong>
        <span>${isIOS ? 'Safari 메뉴 → 홈 화면에 추가' : '앱처럼 설치해서 빠르게 접근하세요!'}</span>
      </div>
      ${btnHtml}
      <button class="pwa-btn-close" onclick="window.closePWABanner()">✕</button>
    `;
    document.body.appendChild(banner);

    setTimeout(closePWABanner, 20000);
  };

  window.triggerPWAInstall = function() {
    if (!deferredPrompt) return;
    deferredPrompt.prompt();
    deferredPrompt.userChoice.then(() => {
      deferredPrompt = null;
      closePWABanner();
    });
  };

  window.closePWABanner = function() {
    const el = document.getElementById('pwa-install-banner');
    if (el) el.remove();
  };

  // 변환 버튼 클릭 시 광고 인터스티셜 (document 레벨 캡처)
  (function() {
    const CONVERT_IDS = ['convertBtn','compressBtn','mergeBtn','splitBtn','deleteBtn',
      'applyBtn','rotateBtn','unlockBtn','processBtn','cropBtn',
      'generateBtn','resizeBtn','startBtn','generateAllBtn','printBtn'];
    let adDone = false;

    document.addEventListener('click', function(e) {
      const id = e.target && e.target.id;
      if (!CONVERT_IDS.includes(id)) return;
      if (adDone) return;
      e.stopImmediatePropagation();
      e.preventDefault();
      const btn = e.target;
      showConvertAd(function() {
        adDone = true;
        btn.click();
      });
    }, true); // capture phase — 도구 자체 리스너보다 먼저 실행

    // 다운로드 버튼은 PWA 배너만
    document.addEventListener('DOMContentLoaded', function() {
      const downloadBtn = document.getElementById('downloadBtn');
      if (downloadBtn) {
        downloadBtn.addEventListener('click', function() {
          setTimeout(showPWABanner, 1500);
        });
      }
    });
  })();

  window.showConvertAd = function(callback) {
    if (window.matchMedia('(display-mode: standalone)').matches) { callback(); return; }

    const style = document.createElement('style');
    style.textContent = [
      '#dl-ad-overlay{position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(0,0,0,0.85);z-index:10000;display:flex;align-items:center;justify-content:center;animation:dlFadeIn .2s ease}',
      '@keyframes dlFadeIn{from{opacity:0}to{opacity:1}}',
      '#dl-ad-box{background:#fff;border-radius:16px;padding:20px 20px 16px;max-width:360px;width:92%;text-align:center;box-shadow:0 8px 40px rgba(0,0,0,0.4)}',
      '#dl-ad-converting{font-size:1rem;font-weight:700;color:#333;margin-bottom:4px;display:flex;align-items:center;justify-content:center;gap:8px}',
      '#dl-ad-converting::before{content:"";display:inline-block;width:16px;height:16px;border:2px solid #ddd;border-top-color:#333;border-radius:50%;animation:dlSpin .8s linear infinite}',
      '@keyframes dlSpin{to{transform:rotate(360deg)}}',
      '#dl-ad-sublabel{font-size:.72rem;color:#aaa;margin-bottom:12px}',
      '#dl-ad-footer{margin-top:12px;font-size:.83rem;color:#777}',
      '#dl-ad-close{margin-top:8px;padding:7px 22px;background:#222;color:#fff;border:none;border-radius:8px;cursor:pointer;font-size:.83rem;display:none}',
      '#dl-ad-close:hover{background:#444}'
    ].join('');
    document.head.appendChild(style);

    const overlay = document.createElement('div');
    overlay.id = 'dl-ad-overlay';
    overlay.innerHTML = '<div id="dl-ad-box">' +
      '<div id="dl-ad-converting">변환 중입니다...</div>' +
      '<div id="dl-ad-sublabel">잠시 광고를 시청해 주세요</div>' +
      '<ins class="adsbygoogle" style="display:block;min-height:100px"' +
        ' data-ad-client="ca-pub-6464921081676309"' +
        ' data-ad-slot="9432796175"' +
        ' data-ad-format="auto"' +
        ' data-full-width-responsive="true"></ins>' +
      '<div id="dl-ad-footer">' +
        '<span id="dl-ad-count">5</span>초 후 변환이 시작됩니다' +
        '<br><button id="dl-ad-close">건너뛰기</button>' +
      '</div>' +
    '</div>';
    document.body.appendChild(overlay);

    try { (window.adsbygoogle = window.adsbygoogle || []).push({}); } catch(e) {}

    var count = 5;
    var finish = function() {
      clearInterval(timer);
      var ov = document.getElementById('dl-ad-overlay');
      if (ov) ov.remove();
      callback();
    };

    document.getElementById('dl-ad-close').addEventListener('click', finish);

    var timer = setInterval(function() {
      count--;
      var el = document.getElementById('dl-ad-count');
      if (el) el.textContent = count;
      if (count <= 3) {
        var btn = document.getElementById('dl-ad-close');
        if (btn) btn.style.display = 'inline-block';
      }
      if (count <= 0) finish();
    }, 1000);
  };
    window._dlAdSkip = finish;

    const timer = setInterval(() => {
      count--;
      const el = document.getElementById('dl-ad-count');
      if (el) el.textContent = count;
      if (count <= 3) {
        const btn = document.getElementById('dl-ad-close');
        if (btn) btn.style.display = 'inline-block';
      }
      if (count <= 0) finish();
    }, 1000);
  };

$1
