 // --- GERENCIAMENTO DO TEMA ---
        const themeToggle = document.getElementById('themeToggle');
        const themeIcon = document.getElementById('themeIcon');

        const savedTheme = localStorage.getItem('theme') || (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
        document.documentElement.setAttribute('data-theme', savedTheme);
        updateThemeIcon(savedTheme);

        themeToggle.addEventListener('click', () => {
            const currentTheme = document.documentElement.getAttribute('data-theme');
            const newTheme = currentTheme === 'light' ? 'dark' : 'light';
            document.documentElement.setAttribute('data-theme', newTheme);
            localStorage.setItem('theme', newTheme);
            updateThemeIcon(newTheme);
        });

        function updateThemeIcon(theme) {
            themeIcon.textContent = theme === 'light' ? '🌙' : '☀️';
        }

        // --- SALVAR PREFERÊNCIAS E COPIAR RESULTADO ---
        const form = document.getElementById('converter-form');
        const tipoConversaoSelect = document.getElementById('tipo_conversao');
        const chaveCesarInput = document.getElementById('chave_cesar');
        const copyButton = document.getElementById('copy-button');

        function carregarPreferencias() {
            const savedOption = localStorage.getItem('lastConversion');
            const savedKey = localStorage.getItem('lastKey');
            if (savedOption) tipoConversaoSelect.value = savedOption;
            if (savedKey) chaveCesarInput.value = savedKey;
        }

        function salvarPreferencias() {
            localStorage.setItem('lastConversion', tipoConversaoSelect.value);
            localStorage.setItem('lastKey', chaveCesarInput.value);
        }

        function copiarResultado() {
            const resultadoTexto = document.getElementById('resultado').innerText;
            if (resultadoTexto) {
                navigator.clipboard.writeText(resultadoTexto)
                    .then(() => alert('Texto copiado para a área de transferência!'))
                    .catch(() => alert('Falha ao copiar o texto.'));
            } else {
                alert('Nada para copiar!');
            }
        }

        document.addEventListener('DOMContentLoaded', carregarPreferencias);
        form.addEventListener('submit', salvarPreferencias);
        copyButton.addEventListener('click', copiarResultado);