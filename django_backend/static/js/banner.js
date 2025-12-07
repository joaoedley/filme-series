(function () {
    const root = document.getElementById("banner");
    if (!root) return;
  
    const slides = Array.from(root.querySelectorAll(".slide"));
    const dots = Array.from(root.querySelectorAll(".dot"));
    const prevBtn = root.querySelector(".prev");
    const nextBtn = root.querySelector(".next");
  
    let idx = slides.findIndex(s => s.classList.contains("active"));
    if (idx < 0) idx = 0;
  
    function show(i) {
      slides.forEach((s, k) => s.classList.toggle("active", k === i));
      dots.forEach((d, k) => d.classList.toggle("active", k === i));
      idx = i;
    }
  
    function next() {
      show((idx + 1) % slides.length);
    }
    function prev() {
      show((idx - 1 + slides.length) % slides.length);
    }
  
    let timer = setInterval(next, 3000);
    function restart() {
      clearInterval(timer);
      timer = setInterval(next, 3000);
    }
  
    nextBtn && nextBtn.addEventListener("click", () => { next(); restart(); });
    prevBtn && prevBtn.addEventListener("click", () => { prev(); restart(); });
    dots.forEach((d, i) => d.addEventListener("click", () => { show(i); restart(); }));
  
    // Pausar ao passar o mouse (desktop)
    root.addEventListener("mouseenter", () => clearInterval(timer));
    root.addEventListener("mouseleave", () => restart());
  })();