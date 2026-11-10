// Scroll para o topo
function waitForElement(selector, callback) {
    const interval = setInterval(() => {
        const element = document.querySelector(selector);
        if (element) {
            clearInterval(interval);
            callback(element);
        }
    }, 100);
}

waitForElement("#scroll_top", function (scrollBtn) {
    scrollBtn.addEventListener("click", function () {
        window.scrollTo({ top: 0, behavior: "smooth" });
    });
});

const sectionIds = [
    "player-profile",
    "attribute-summary",
    "comparison",
    "heatmap",
    "passing",
    "shooting",
    "dribbling",
    "team-passing"
];

const waitForSections = setInterval(() => {
    const allExist = sectionIds.every(id => document.getElementById(id));
    if (allExist) {
        clearInterval(waitForSections);

        const navLinks = document.querySelectorAll(".nav-link");
        navLinks.forEach(link => {
            link.addEventListener("click", function (e) {
                e.preventDefault();
                const targetId = this.getAttribute("href").substring(1);
                const target = document.getElementById(targetId);
                if (target) {
                    target.scrollIntoView({ behavior: "smooth" });
                }
            });
        });
    }
}, 100);

// Ativar destaque dinâmico com scroll (scroll spy)
window.addEventListener("scroll", () => {
    let currentSection = "";

    sectionIds.forEach(id => {
        const section = document.getElementById(id);
        if (section) {
            const sectionTop = section.getBoundingClientRect().top;
            if (sectionTop <= 150) {
                currentSection = id;
            }
        }
    });

    const navLinks = document.querySelectorAll(".nav-link");
    navLinks.forEach(link => {
        const linkId = link.getAttribute("href").substring(1);
        if (linkId === currentSection) {
            link.classList.add("active");
        } else {
            link.classList.remove("active");
        }
    });
});
