// Language switcher for mdBook multilingual setup
// Two toggle buttons to switch between /zh/ and /en/ versions
(function() {
    const defined_languages = [
        ["zh", "中文"],
        ["en", "English"],
    ];

    function getCurrentLanguage() {
        const path = window.location.pathname;
        const match = path.match(/\/(zh|en)(\/|$)/);
        return match ? match[1] : "zh";
    }

    function getBasePath() {
        const path = window.location.pathname;
        const match = path.match(/^(.*?)\/(zh|en)(\/|$)/);
        return match ? match[1] : "";
    }

    function getPagePath() {
        const path = window.location.pathname;
        const match = path.match(/\/(zh|en)(\/.*)?$/);
        return match && match[2] ? match[2] : "/";
    }

    function buildLanguageUrl(targetLang) {
        const basePath = getBasePath();
        const pagePath = getPagePath();
        return `${basePath}/${targetLang}${pagePath}`;
    }

    function createLanguageSwitcher() {
        const currentLang = getCurrentLanguage();

        const switcher = document.createElement("div");
        switcher.className = "language-switcher";
        switcher.innerHTML = defined_languages.map(([code, name]) => `
            <a href="${buildLanguageUrl(code)}"
               class="lang-btn ${code === currentLang ? 'active' : ''}"
               ${code === currentLang ? 'aria-current="true"' : ''}>
                ${name}
            </a>
        `).join('');

        const style = document.createElement("style");
        style.textContent = `
            .language-switcher {
                display: flex;
                gap: 0;
                margin-right: 0.5rem;
                border-radius: 6px;
                overflow: hidden;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            .lang-btn {
                padding: 0.5rem 1rem;
                text-decoration: none;
                font-size: 0.9rem;
                font-weight: 500;
                transition: all 0.2s ease;
                border: none;
                background: #e8e8e8;
                color: #666;
            }
            .lang-btn:first-child {
                border-radius: 6px 0 0 6px;
            }
            .lang-btn:last-child {
                border-radius: 0 6px 6px 0;
            }
            .lang-btn:hover {
                background: #d0d0d0;
                color: #333;
            }
            .lang-btn.active {
                background: linear-gradient(135deg, #4a90d9 0%, #357abd 100%);
                color: #fff;
                cursor: default;
                box-shadow: inset 0 1px 3px rgba(0,0,0,0.2);
            }
            .lang-btn.active:hover {
                background: linear-gradient(135deg, #4a90d9 0%, #357abd 100%);
                color: #fff;
            }
            /* Dark theme support */
            .navy .lang-btn,
            .coal .lang-btn,
            .ayu .lang-btn {
                background: #3a3a3a;
                color: #aaa;
            }
            .navy .lang-btn:hover,
            .coal .lang-btn:hover,
            .ayu .lang-btn:hover {
                background: #4a4a4a;
                color: #fff;
            }
            .navy .lang-btn.active,
            .coal .lang-btn.active,
            .ayu .lang-btn.active {
                background: linear-gradient(135deg, #4a90d9 0%, #357abd 100%);
                color: #fff;
            }
        `;
        document.head.appendChild(style);

        return switcher;
    }

    function insertLanguageSwitcher() {
        const rightButtons = document.querySelector(".right-buttons");
        if (rightButtons) {
            const switcher = createLanguageSwitcher();
            rightButtons.insertBefore(switcher, rightButtons.firstChild);
        }
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", insertLanguageSwitcher);
    } else {
        insertLanguageSwitcher();
    }
})();
