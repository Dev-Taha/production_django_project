document.addEventListener("DOMContentLoaded", () => {
    const cards = document.querySelectorAll(".template-card");
    if(cards.length === 0) return; // Only execute on the templates dashboard

    const browserBody = document.querySelector(".browser-body");
    const previewTitle = document.getElementById("preview-title");
    const browserTitle = document.querySelector(".browser-url-bar span");

    const themes = [
        {
            name: "Classic Scholar &mdash; Version 2.4.1",
            url: "preview.smartapp.io/scholar-template",
            html: `
            <div class="bg-white h-100 p-4 p-md-5" style="font-family: 'Georgia', serif;">
                <div class="d-flex justify-content-between align-items-center mb-5 border-bottom pb-4">
                    <h4 class="fw-bold mb-0 text-dark">Dr. Sarah Jenkins</h4>
                    <nav class="d-none d-md-flex gap-4 fw-bold small text-uppercase" style="letter-spacing: 0.05em;">
                        <span class="text-primary border-bottom border-primary pb-1">Overview</span>
                        <span class="text-secondary">Research</span>
                        <span class="text-secondary">Publications</span>
                    </nav>
                </div>
                <div class="row align-items-center mt-2">
                    <div class="col-7">
                        <span class="text-primary fw-bold mb-3 d-inline-block small text-uppercase" style="letter-spacing: 0.1em;">Bio-Engineering</span>
                        <h1 class="display-4 text-dark mb-4" style="font-weight: 800; line-height: 1.1;">Deciphering the Neural Code.</h1>
                        <p class="text-secondary mb-4 lh-lg" style="font-size: 0.9rem;">Exploring the intersection of artificial intelligence and biological neural networks.</p>
                        <button class="btn btn-dark rounded-pill px-4 py-2 small fw-bold">View Publications</button>
                    </div>
                    <div class="col-5 text-end">
                        <div class="rounded-circle overflow-hidden d-inline-block border border-4 border-white shadow-sm" style="width: 140px; height: 140px;">
                            <img src="https://i.pravatar.cc/150?img=5" alt="Sarah" class="w-100 h-100 object-fit-cover">
                        </div>
                    </div>
                </div>
            </div>`
        },
        {
            name: "Modern Dark &mdash; Version 1.2.0",
            url: "preview.smartapp.io/modern-dark-02",
            html: `
            <div class="bg-dark text-white h-100 p-4 p-md-5" style="font-family: 'Inter', sans-serif;">
                <div class="d-flex justify-content-between align-items-center mb-5">
                    <h4 class="fw-bold mb-0 text-white">S. JENKINS</h4>
                    <nav class="d-none d-md-flex gap-4 fw-semibold small">
                        <span class="text-info">/overview</span>
                        <span class="text-secondary">/research</span>
                        <span class="text-secondary">/publications</span>
                    </nav>
                </div>
                <div class="row mt-4">
                    <div class="col-8">
                        <div class="badge bg-info text-dark mb-3 px-3 py-2 rounded-0 fw-bold">SYS_RESEARCHER_01</div>
                        <h1 class="display-5 text-white mb-4 fw-black text-uppercase" style="letter-spacing: -0.02em;">Advanced<br>Neural<br>Computation</h1>
                        <div class="bg-secondary bg-opacity-25 p-3 border-start border-info border-4">
                            <p class="text-light mb-0 small font-monospace">>> Executing biological mapping protocols...</p>
                        </div>
                    </div>
                    <div class="col-4 d-flex align-items-end justify-content-end">
                         <div class="bg-info" style="width: 60px; height: 60px;"></div>
                    </div>
                </div>
            </div>`
        },
        {
            name: "Minimalist Lab &mdash; Version 3.1.2",
            url: "preview.smartapp.io/min-lab",
            html: `
            <div class="bg-white h-100 p-4 p-md-5" style="font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;">
                <div class="d-flex justify-content-between align-items-start mb-5">
                    <h5 class="fw-normal mb-0 text-dark">Sarah<br>Jenkins.</h5>
                    <nav class="d-none d-md-flex flex-column gap-2 text-end small">
                        <span class="text-dark fw-bold">Overview</span>
                        <span class="text-secondary">Research</span>
                        <span class="text-secondary">Contact</span>
                    </nav>
                </div>
                <div class="mt-5 pt-4">
                    <h1 class="text-dark fw-light mb-4" style="font-size: 3rem; letter-spacing: -0.03em;">Simplicity in complex systems.</h1>
                    <p class="text-secondary w-75 lh-lg">Focusing entirely on the data. Minimalist Lab provides a distraction-free environment for pure academic research.</p>
                </div>
            </div>`
        },
        {
            name: "Executive Academic &mdash; Version 1.0.5",
            url: "preview.smartapp.io/exec-academic",
            html: `
            <div class="h-100 p-4 p-md-5 text-white position-relative" style="background-color: #0f172a; font-family: 'Playfair Display', serif;">
                <div class="position-absolute top-0 start-0 w-100 h-100" style="background: radial-gradient(circle at top right, rgba(217, 160, 84, 0.15), transparent 50%); pointer-events: none;"></div>
                <div class="d-flex justify-content-between align-items-center mb-5 position-relative z-1">
                    <h4 class="mb-0 text-white" style="color: #d9a054 !important;">Dr. Sarah Jenkins</h4>
                    <nav class="d-none d-md-flex gap-4 small" style="letter-spacing: 0.1em;">
                        <span class="text-white border-bottom pb-1" style="border-color: #d9a054 !important;">OVERVIEW</span>
                        <span class="text-secondary">RESEARCH</span>
                    </nav>
                </div>
                <div class="row align-items-center mt-4 position-relative z-1">
                    <div class="col-8">
                        <p class="mb-3 small text-uppercase" style="color: #d9a054; letter-spacing: 0.2em;">Director of Research</p>
                        <h1 class="display-5 text-white mb-4 lh-sm">Leading the future of <br><span style="font-style: italic; color: #d9a054;">bio-engineering.</span></h1>
                        <button class="btn rounded-0 px-4 py-2 small text-dark fw-bold mt-2" style="background-color: #d9a054;">Discover</button>
                    </div>
                </div>
            </div>`
        }
    ];

    cards.forEach((card, index) => {
        card.addEventListener("click", () => {
            // Update active state
            cards.forEach(c => {
                c.classList.remove("active");
                const badge = c.querySelector(".template-badge-primary");
                if(badge) badge.remove();
            });
            card.classList.add("active");
            
            // Add ACTIVE badge
            const titleDiv = card.querySelector(".d-flex.align-items-center");
            if(!titleDiv.querySelector(".template-badge-primary")) {
                const badge = document.createElement("span");
                badge.className = "template-badge-primary ms-2";
                badge.textContent = "ACTIVE";
                titleDiv.appendChild(badge);
            }

            // Update Preview Area
            previewTitle.innerHTML = themes[index].name;
            browserTitle.textContent = themes[index].url;
            
            // Add fade animation
            browserBody.style.opacity = '0';
            setTimeout(() => {
                browserBody.innerHTML = themes[index].html;
                browserBody.style.opacity = '1';
            }, 150);
        });
    });
    
    // Initialize first theme with transition properties
    browserBody.style.transition = 'opacity 0.15s ease-in-out';
    browserBody.innerHTML = themes[0].html;
});
