// Get references to the HTML elements we need to interact with
const form = document.getElementById('username-form');
const usernameInput = document.getElementById('username-input');
const resultContainer = document.getElementById('result-container');
const markdownOutput = document.getElementById('markdown-output');
const previewOutput = document.getElementById('preview-output');
const copyButton = document.getElementById('copy-button');

// Listen for the form to be submitted
form.addEventListener('submit', (event) => {
    event.preventDefault(); // Prevent the page from reloading

    const username = usernameInput.value.trim();
    if (!username) {
        return; // Do nothing if the input is empty
    }

    // This dynamically gets the base URL of our deployed Vercel app
    const baseUrl = window.location.origin;

    // Construct the two URLs needed for the Markdown
    const badgeUrl = `${baseUrl}/api/badge?username=${username}`;
    const profileUrl = `https://robocontest.uz/profile/${username}`;

    // Create the final Markdown string
    const markdownCode = `[![RoboContest Stats](${badgeUrl})](${profileUrl})`;

    // Display the generated markdown and the preview
    markdownOutput.textContent = markdownCode;
    previewOutput.innerHTML = `<a href="${profileUrl}"><img src="${badgeUrl}" alt="RoboContest Stats Badge"></a>`;

    // Show the results container
    resultContainer.classList.remove('hidden');
});

// Add logic for the copy button
copyButton.addEventListener('click', () => {
    navigator.clipboard.writeText(markdownOutput.textContent).then(() => {
        // Give user feedback that text was copied
        copyButton.textContent = 'Copied!';
        setTimeout(() => {
            copyButton.textContent = 'Copy';
        }, 2000); // Reset button text after 2 seconds
    });
});
