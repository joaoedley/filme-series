// Basic player helpers for Bunny videos
// - Switch <video> src when clicking episode items
// - Auto play on source change

(function(){
    const video = document.querySelector(".player video");
    if (!video) return;
  
    // Switch source when clicking items with [data-video-src]
    document.addEventListener("click", (e) => {
      const el = e.target.closest("[data-video-src]");
      if (!el) return;
      const src = el.getAttribute("data-video-src");
      if (!src) return;
      changeSource(src);
    });
  
    function changeSource(src){
      // If using HLS .m3u8, native Safari supports it. For other browsers,
      // consider hls.js. For now, rely on MP4/WebM or native HLS.
      video.pause();
      video.src = src;
      video.load();
      video.play().catch(()=>{});
    }
  
    // Optional: autoplay first episode if marked
    const first = document.querySelector("[data-video-src].autoplay");
    if (first) {
      const src = first.getAttribute("data-video-src");
      if (src) changeSource(src);
    }
  })();