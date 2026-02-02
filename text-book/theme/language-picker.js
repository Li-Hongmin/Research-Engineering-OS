// Language picker for mdBook multilingual setup
// Dropdown menu to switch between /zh/ and /en/ versions
(function() {
    const defined_languages = [
        ["zh", "中文"],
        ["en", "English"],
        ["ja", "日本語"],
    ];

    function getCurrentLanguage() {
        const path = window.location.pathname;
        const match = path.match(/\/(zh|en|ja)(\/|$)/);
        return match ? match[1] : "zh";
    }

    function getBasePath() {
        const path = window.location.pathname;
        const match = path.match(/^(.*?)\/(zh|en|ja)(\/|$)/);
        return match ? match[1] : "";
    }

    function getPagePath() {
        const path = window.location.pathname;
        const match = path.match(/\/(zh|en|ja)(\/.*)?$/);
        return match && match[2] ? match[2] : "/";
    }

    function buildLanguageUrl(targetLang) {
        const basePath = getBasePath();
        const pagePath = getPagePath();
        return `${basePath}/${targetLang}${pagePath}`;
    }

    function createLanguagePicker() {
        const currentLang = getCurrentLanguage();
        const currentName = defined_languages.find(l => l[0] === currentLang)?.[1] || "中文";

        const picker = document.createElement("div");
        picker.className = "language-picker";
        picker.innerHTML = `
            <button class="language-toggle" aria-label="切换语言 / Switch language" aria-expanded="false">
                <span class="language-icon">🌐</span>
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
                font-size: 0.9rem;
                font-weight: 500;
                transition: all 0.2s ease;
                box-shadow: 0 2px 4px rgba(74, 144, 217, 0.3);
            }
            .language-toggle:hover {
                background: linear-gradient(135deg, #357abd 0%, #2868a9 100%);
                box-shadow: 0 4px 8px rgba(74, 144, 217, 0.4);
            }
            .language-icon {
                font-size: 1.1rem;
            }
            .language-arrow {
                font-size: 0.6rem;
                transition: transform 0.2s ease;
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
                border-radius: 6px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.15);
                min-width: 120px;
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
                padding: 0.6rem 1rem;
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

        const toggle = picker.querySelector(".language-toggle");
        const list = picker.querySelector(".language-list");

        toggle.addEventListener("click", (e) => {
            e.stopPropagation();
            const isOpen = list.classList.toggle("show");
            picker.classList.toggle("open", isOpen);
            toggle.setAttribute("aria-expanded", isOpen);
        });

        document.addEventListener("click", () => {
            list.classList.remove("show");
            picker.classList.remove("open");
            toggle.setAttribute("aria-expanded", "false");
        });

        document.addEventListener("keydown", (e) => {
            if (e.key === "Escape") {
                list.classList.remove("show");
                picker.classList.remove("open");
                toggle.setAttribute("aria-expanded", "false");
            }
        });

        return picker;
    }

    function insertLanguagePicker() {
        const rightButtons = document.querySelector(".right-buttons");
        if (rightButtons) {
            const picker = createLanguagePicker();
            rightButtons.insertBefore(picker, rightButtons.firstChild);
        }
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", insertLanguagePicker);
    } else {
        insertLanguagePicker();
    }
})();
