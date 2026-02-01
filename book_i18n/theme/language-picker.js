// Language picker for mdBook multilingual setup
// Adds a dropdown to switch between /zh/ and /en/ versions
(function() {
    // Available languages with display names
    const defined_languages = [
        ["zh", "中文"],
        ["en", "English"],
    ];

    // Get current language from URL path
    function getCurrentLanguage() {
        const path = window.location.pathname;
        // Match /zh/ or /en/ in the path
        const match = path.match(/\/(zh|en)(\/|$)/);
        return match ? match[1] : "zh";
    }

    // Get the base path (everything before /zh/ or /en/)
    function getBasePath() {
        const path = window.location.pathname;
        const match = path.match(/^(.*?)\/(zh|en)(\/|$)/);
        return match ? match[1] : "";
    }

    // Get the page path (everything after /zh/ or /en/)
    function getPagePath() {
        const path = window.location.pathname;
        const match = path.match(/\/(zh|en)(\/.*)?$/);
        if (match && match[2]) {
            return match[2];
        }
        return "/";
    }

    // Build URL for target language
    function buildLanguageUrl(targetLang) {
        const basePath = getBasePath();
        const pagePath = getPagePath();
        return `${basePath}/${targetLang}${pagePath}`;
    }

    // Create language picker HTML
    function createLanguagePicker() {
        const currentLang = getCurrentLanguage();
        const currentName = defined_languages.find(l => l[0] === currentLang)?.[1] || "中文";

        const picker = document.createElement("div");
        picker.className = "language-picker";
        picker.innerHTML = `
            <button class="language-toggle" aria-label="Select language" aria-expanded="false">
                <span class="language-icon">🌐</span>
                <span class="language-label">Language:</span>
                <span class="language-name">${currentName}</span>
                <span class="language-arrow">▼</span>
            </button>
            <ul class="language-list" role="menu">
                ${defined_languages.map(([code, name]) => `
                    <li role="menuitem">
                        <a href="${buildLanguageUrl(code)}"
                           class="${code === currentLang ? 'active' : ''}"
                           ${code === currentLang ? 'aria-current="true"' : ''}>
                            ${name}
                        </a>
                    </li>
                `).join('')}
            </ul>
        `;

        // Style the picker
        const style = document.createElement("style");
        style.textContent = `
            .language-picker {
                position: relative;
                display: inline-block;
                margin-right: 0.5rem;
            }
            .language-toggle {
                display: flex;
                align-items: center;
                gap: 0.4rem;
                padding: 0.5rem 0.8rem;
                background: linear-gradient(135deg, #4a90d9 0%, #357abd 100%);
                border: none;
                border-radius: 6px;
                color: #fff;
                cursor: pointer;
                font-size: 0.95rem;
                font-weight: 500;
                transition: all 0.2s ease;
                box-shadow: 0 2px 4px rgba(74, 144, 217, 0.3);
            }
            .language-toggle:hover {
                background: linear-gradient(135deg, #357abd 0%, #2868a9 100%);
                box-shadow: 0 4px 8px rgba(74, 144, 217, 0.4);
                transform: translateY(-1px);
            }
            .language-icon {
                font-size: 1.1rem;
            }
            .language-arrow {
                font-size: 0.65rem;
                transition: transform 0.2s ease;
                opacity: 0.9;
            }
            .language-label {
                font-size: 0.75rem;
                opacity: 0.85;
                margin-right: 0.2rem;
            }
            .language-picker.open .language-arrow {
                transform: rotate(180deg);
            }
            .language-list {
                display: none;
                position: absolute;
                top: 100%;
                right: 0;
                margin: 0.3rem 0 0 0;
                padding: 0.3rem 0;
                list-style: none;
                background: var(--bg);
                border: 1px solid var(--icons);
                border-radius: 4px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.15);
                min-width: 100px;
                z-index: 1000;
            }
            .language-list.show {
                display: block;
            }
            .language-list li {
                margin: 0;
                padding: 0;
            }
            .language-list a {
                display: block;
                padding: 0.5rem 1rem;
                color: var(--fg);
                text-decoration: none;
                white-space: nowrap;
                transition: background 0.15s ease;
            }
            .language-list a:hover {
                background: var(--quote-bg);
            }
            .language-list a.active {
                font-weight: bold;
                color: var(--links);
            }
            .language-list a.active::before {
                content: "✓ ";
            }
        `;
        document.head.appendChild(style);

        // Toggle dropdown
        const toggle = picker.querySelector(".language-toggle");
        const list = picker.querySelector(".language-list");

        toggle.addEventListener("click", (e) => {
            e.stopPropagation();
            const isOpen = list.classList.toggle("show");
            picker.classList.toggle("open", isOpen);
            toggle.setAttribute("aria-expanded", isOpen);
        });

        // Close on outside click
        document.addEventListener("click", () => {
            list.classList.remove("show");
            picker.classList.remove("open");
            toggle.setAttribute("aria-expanded", "false");
        });

        // Close on escape key
        document.addEventListener("keydown", (e) => {
            if (e.key === "Escape") {
                list.classList.remove("show");
                picker.classList.remove("open");
                toggle.setAttribute("aria-expanded", "false");
            }
        });

        return picker;
    }

    // Insert language picker into the page
    function insertLanguagePicker() {
        const rightButtons = document.querySelector(".right-buttons");
        if (rightButtons) {
            const picker = createLanguagePicker();
            rightButtons.insertBefore(picker, rightButtons.firstChild);
        }
    }

    // Run when DOM is ready
    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", insertLanguagePicker);
    } else {
        insertLanguagePicker();
    }
})();
