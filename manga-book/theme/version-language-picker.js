// Version + Language Picker for mdBook multilingual setup
// Provides dual-axis switching between versions (Text/Manga) and languages (zh/en/ja)
(function() {
    const versions = [
        ["text", "📖 Text"],
        ["manga", "🎨 Manga"],
    ];

    const languages = [
        ["zh", "中文"],
        ["en", "English"],
        ["ja", "日本語"],
    ];

    // ============================================
    // Context Detection Functions
    // ============================================

    function getBookContext() {
        const pathname = window.location.pathname;

        // Detect if we're in manga or text version
        const isManga = /\/manga(\/|$)/.test(pathname);

        // Detect current language
        const langMatch = pathname.match(/\/(zh|en|ja)(\/|$)/);
        const currentLang = langMatch ? langMatch[1] : "en";

        // Extract page path (everything after /manga/lang/ or /lang/)
        let pagePath = "/";
        if (isManga) {
            // For manga: /manga/zh/00-preface/03.html → /00-preface/03.html
            const match = pathname.match(/\/manga\/(zh|en|ja)(\/.*)?$/);
            pagePath = match && match[2] ? match[2] : "/";
        } else {
            // For text: /en/00-preface.html → /00-preface.html
            const match = pathname.match(/\/(zh|en|ja)(\/.*)?$/);
            pagePath = match && match[2] ? match[2] : "/";
        }

        // Calculate base path (everything before manga/ or lang/)
        let basePath = "";
        if (isManga) {
            const baseMatch = pathname.match(/^(.*?)\/manga\//);
            basePath = baseMatch ? baseMatch[1] : "";
        } else {
            const baseMatch = pathname.match(/^(.*?)\/(zh|en|ja)\//);
            basePath = baseMatch ? baseMatch[1] : "";
        }

        return {
            version: isManga ? "manga" : "text",
            language: currentLang,
            pagePath: pagePath,
            basePath: basePath,
            isManga: isManga
        };
    }

    // ============================================
    // URL Construction Functions
    // ============================================

    function buildVersionUrl(targetVersion, context) {
        const basePath = context.basePath;
        let pagePath = context.pagePath;

        if (targetVersion === "manga") {
            // Fix path mapping: text has single-page structure (e.g., /00-preface.html)
            // while manga has multi-page structure (e.g., /00-preface/01.html)
            if (!context.isManga) {
                // Extract chapter name from text path: /00-preface.html → /00-preface/01.html
                const chapterMatch = pagePath.match(/\/([\w-]+)\.html$/);
                if (chapterMatch) {
                    pagePath = `/${chapterMatch[1]}/01.html`;
                }
            }
            return `${basePath}/manga/${context.language}${pagePath}`;
        } else {
            // When switching from manga to text, preserve the same language
            const lang = context.language;
            
            // Fix path mapping: manga has multi-page structure (e.g., /00-preface/01.html)
            // while text has single-page structure (e.g., /00-preface.html)
            if (context.isManga) {
                // Extract chapter name from manga path: /00-preface/01.html → /00-preface.html
                const chapterMatch = pagePath.match(/\/([\w-]+)\//);
                if (chapterMatch) {
                    pagePath = `/${chapterMatch[1]}.html`;
                } else if (pagePath === "/" || pagePath === "") {
                    pagePath = "/";
                }
            }
            
            return `${basePath}/${lang}${pagePath}`;
        }
    }

    function buildLanguageUrl(targetLang, context) {
        const basePath = context.basePath;
        const pagePath = context.pagePath;
        return `${basePath}/${targetLang}${pagePath}`;
    }

    // ============================================
    // UI Creation Functions
    // ============================================

    function createVersionPicker(context) {
        const currentVersion = context.version;
        const currentVersionName = versions.find(v => v[0] === currentVersion)?.[1] || "📖 Text";

        const picker = document.createElement("div");
        picker.className = "version-picker picker-dropdown";
        picker.setAttribute("role", "navigation");
        picker.setAttribute("aria-label", "Version selector");

        picker.innerHTML = `
            <button class="version-toggle picker-toggle" aria-label="Switch between Text and Manga versions" aria-expanded="false" aria-haspopup="true">
                <span class="picker-icon">${currentVersionName}</span>
                <span class="picker-arrow">▼</span>
            </button>
            <ul class="version-list picker-menu" role="menu">
                ${versions.map(([code, name]) => `
                    <li role="none">
                        <a href="${buildVersionUrl(code, context)}"
                           role="menuitem"
                           class="picker-item ${code === currentVersion ? 'active' : ''}"
                           ${code === currentVersion ? 'aria-current="page"' : ''}>
                            ${name}
                        </a>
                    </li>
                `).join('')}
            </ul>
        `;

        return picker;
    }

    function createLanguagePicker(context) {
        // Hide language picker if we're in manga mode
        if (context.isManga) {
            return null;
        }

        const currentLang = context.language;
        const currentLangName = languages.find(l => l[0] === currentLang)?.[1] || "English";

        const picker = document.createElement("div");
        picker.className = "language-picker picker-dropdown";
        picker.setAttribute("role", "navigation");
        picker.setAttribute("aria-label", "Language selector");

        picker.innerHTML = `
            <button class="language-toggle picker-toggle" aria-label="Switch between languages (中文 / English / 日本語)" aria-expanded="false" aria-haspopup="true">
                <span class="picker-icon">🌐 ${currentLangName}</span>
                <span class="picker-arrow">▼</span>
            </button>
            <ul class="language-list picker-menu" role="menu">
                ${languages.map(([code, name]) => `
                    <li role="none">
                        <a href="${buildLanguageUrl(code, context)}"
                           role="menuitem"
                           class="picker-item ${code === currentLang ? 'active' : ''}"
                           ${code === currentLang ? 'aria-current="page"' : ''}>
                            ${name}
                        </a>
                    </li>
                `).join('')}
            </ul>
        `;

        return picker;
    }

    function attachPickerEventHandlers(picker) {
        const toggle = picker.querySelector(".picker-toggle");
        const menu = picker.querySelector(".picker-menu");

        if (!toggle || !menu) return;

        // Toggle menu on button click
        toggle.addEventListener("click", (e) => {
            e.stopPropagation();
            const isOpen = menu.classList.toggle("show");
            picker.classList.toggle("open", isOpen);
            toggle.setAttribute("aria-expanded", isOpen);
        });

        // Close menu when clicking outside
        document.addEventListener("click", () => {
            menu.classList.remove("show");
            picker.classList.remove("open");
            toggle.setAttribute("aria-expanded", "false");
        });

        // Close menu on Escape key
        document.addEventListener("keydown", (e) => {
            if (e.key === "Escape") {
                menu.classList.remove("show");
                picker.classList.remove("open");
                toggle.setAttribute("aria-expanded", "false");
            }
        });

        // Keyboard navigation within menu
        const items = menu.querySelectorAll("a");
        items.forEach((item, index) => {
            item.addEventListener("keydown", (e) => {
                if (e.key === "ArrowDown") {
                    e.preventDefault();
                    items[(index + 1) % items.length].focus();
                } else if (e.key === "ArrowUp") {
                    e.preventDefault();
                    items[(index - 1 + items.length) % items.length].focus();
                } else if (e.key === "Enter") {
                    item.click();
                }
            });
        });
    }

    // ============================================
    // Styles Injection
    // ============================================

    function injectStyles() {
        const style = document.createElement("style");
        style.textContent = `
            /* Picker Group Container - Inline with other buttons */
            .picker-group {
                display: inline-flex;
                gap: 0.5rem;
                align-items: center;
                margin-right: 0.8rem;
                vertical-align: middle;
            }

            /* Shared Picker Dropdown Styles */
            .picker-dropdown {
                position: relative;
                display: inline-block;
                vertical-align: middle;
            }

            /* Shared Toggle Button Styles */
            .picker-toggle {
                display: inline-flex;
                align-items: center;
                gap: 0.4rem;
                padding: 0.5rem 0.8rem;
                border: none;
                border-radius: 6px;
                color: #fff;
                cursor: pointer;
                font-size: 1rem;
                font-weight: 500;
                transition: all 0.2s ease;
                white-space: nowrap;
                vertical-align: middle;
            }

            /* Version Picker (Teal) */
            .version-toggle {
                background: linear-gradient(135deg, #0d9488 0%, #0f766e 100%);
                box-shadow: 0 2px 4px rgba(13, 148, 136, 0.3);
            }

            .version-toggle:hover {
                background: linear-gradient(135deg, #0f766e 0%, #115e59 100%);
                box-shadow: 0 4px 8px rgba(13, 148, 136, 0.4);
            }

            /* Language Picker (Blue) */
            .language-toggle {
                background: linear-gradient(135deg, #4a90d9 0%, #357abd 100%);
                box-shadow: 0 2px 4px rgba(74, 144, 217, 0.3);
            }

            .language-toggle:hover {
                background: linear-gradient(135deg, #357abd 0%, #2868a9 100%);
                box-shadow: 0 4px 8px rgba(74, 144, 217, 0.4);
            }

            /* Arrow Animation */
            .picker-arrow {
                font-size: 0.6rem;
                transition: transform 0.2s ease;
            }

            .picker-dropdown.open .picker-arrow {
                transform: rotate(180deg);
            }

            /* Menu Styles */
            .picker-menu {
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
                min-width: 140px;
                z-index: 1000;
            }

            .picker-menu.show {
                display: block;
            }

            .picker-menu li {
                margin: 0;
                padding: 0;
            }

            .picker-item {
                display: block;
                padding: 0.6rem 1rem;
                color: var(--fg);
                text-decoration: none;
                white-space: nowrap;
                transition: background 0.15s ease;
            }

            .picker-item:hover {
                background: var(--quote-bg);
            }

            .picker-item.active {
                font-weight: bold;
                color: var(--links);
            }

            .picker-item.active::before {
                content: "✓ ";
            }

            /* Mobile Responsive */
            @media (max-width: 768px) {
                .picker-group {
                    gap: 0.3rem;
                    margin-right: 0.5rem;
                }

                .picker-toggle {
                    padding: 0.4rem 0.6rem;
                    font-size: 0.85rem;
                }

                .picker-menu {
                    min-width: 120px;
                }
            }
        `;
        document.head.appendChild(style);
    }

    // ============================================
    // Main Insertion Function
    // ============================================

    function insertPickers() {
        const rightButtons = document.querySelector(".right-buttons");
        if (!rightButtons) return;

        const context = getBookContext();

        // Create picker group container
        const pickerGroup = document.createElement("div");
        pickerGroup.className = "picker-group";

        // Version picker (always visible)
        const versionPicker = createVersionPicker(context);
        if (versionPicker) {
            pickerGroup.appendChild(versionPicker);
            attachPickerEventHandlers(versionPicker);
        }

        // Language picker (only visible in text mode)
        const languagePicker = createLanguagePicker(context);
        if (languagePicker) {
            pickerGroup.appendChild(languagePicker);
            attachPickerEventHandlers(languagePicker);
        }

        // Insert picker group at the beginning of right-buttons
        rightButtons.insertBefore(pickerGroup, rightButtons.firstChild);
    }

    // ============================================
    // Initialization
    // ============================================

    function init() {
        injectStyles();
        insertPickers();
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", init);
    } else {
        init();
    }
})();
