const form = document.getElementById('username-form');
const usernameInput = document.getElementById('username-input');
const resultContainer = document.getElementById('result-container');
const markdownOutput = document.getElementById('markdown-output');
const previewOutput = document.getElementById('preview-output');
const copyButton = document.getElementById('copy-button');
const themeToggle = document.getElementById('checkbox');
const body = document.body;

function applyTheme(theme) {
    if (theme === 'dark') {
        body.setAttribute('data-theme', 'dark');
        themeToggle.checked = true;
    } else {
        body.removeAttribute('data-theme');
        themeToggle.checked = false;
    }
}

const savedTheme = localStorage.getItem('theme');

const prefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;

if (savedTheme) {
    applyTheme(savedTheme);
} else if (prefersDark) {
    applyTheme('dark');
} else {
    applyTheme('light');
}


themeToggle.addEventListener('change', () => {
    if (themeToggle.checked) {
        body.setAttribute('data-theme', 'dark');
        localStorage.setItem('theme', 'dark'); // Save the choice
    } else {
        body.removeAttribute('data-theme');
        localStorage.setItem('theme', 'light'); // Save the choice
    }
});
form.addEventListener('submit', (event) => {
    event.preventDefault(); 

    const username = usernameInput.value.trim();
    if (!username) {
        return; 
    }


    const baseUrl = window.location.origin;

    const badgeUrl = `${baseUrl}/api/badge?username=${username}`;
    const profileUrl = `https://robocontest.uz/profile/${username}`;

    const markdownCode = `[![RoboContest Stats](${badgeUrl})](${profileUrl})`;

    markdownOutput.textContent = markdownCode;
    previewOutput.innerHTML = `<a href="${profileUrl}"><img src="${badgeUrl}" alt="RoboContest Stats Badge"></a>`;

    resultContainer.classList.remove('hidden');
});

copyButton.addEventListener('click', () => {
    navigator.clipboard.writeText(markdownOutput.textContent).then(() => {
        copyButton.textContent = 'Copied!';
        setTimeout(() => {
            copyButton.textContent = 'Copy';
        }, 2000);
    });
});
