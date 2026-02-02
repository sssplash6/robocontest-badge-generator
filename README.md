# Dynamic RoboContest.uz GitHub Stats Card

A free, open-source web application that generates dynamic, shareable SVG stats cards for any `robocontest.uz` user profile. Perfect for showcasing your competitive programming stats on your GitHub profile or personal website.

![RoboContest Stats Card](https://robocontest-badge-generator-five.vercel.app/api/badge?username=nesamandar)
*(Live example for the user 'nesamandar')*

---

## ✨ Features

- **Dynamic Data:** Stats are scraped in real-time and are always up-to-date.
- **Customizable:** Simply change the `username` parameter to generate a card for any user.
- **SVG Format:** Crisp, scalable vector images that look great on any web.
- **Dark Mode:** A sleek, modern design inspired by GitHub's dark theme.
- **Free & Serverless:** Deployed on Vercel's Hobby plan at no cost.

---

## 🚀 Live Demo & Usage

It's incredibly simple to get your own stats card.

1.  **Visit the website:**
    **[robocontest-badge-generator-five.vercel.app](https://robocontest-badge-generator-five.vercel.app/)**  

2.  **Enter Your Username:** Type your `robocontest.uz` username into the input field.

3.  **Copy the Code:** Click the "Copy" button to copy the generated markdown code.

4.  **Paste It:** Paste the code into your GitHub profile's `README.md` file.

---

## 🛠️ How It Works?

This project is a complete web application built with a modern, serverless architecture.

*   **Frontend:**
    *   Built with plain **HTML, CSS, and JavaScript** for a lightweight and fast user experience.
    *   Features a responsive design with an automatic dark/light mode toggle that respects user system preferences.

*   **Backend (Serverless Function):**
    *   A single Python serverless function hosted on Vercel.
    *   **Web Scraping:** Uses the `requests` and `BeautifulSoup4` libraries to fetch and parse the `robocontest.uz` profile page in real-time.
    *   **Dynamic SVG Generation:** The Python function generates a custom SVG image as a string, dynamically embedding the scraped stats and calculating the progress bar percentage. This SVG is then sent directly to the browser.

*   **Deployment:**
    *   **Vercel:** The entire project (both frontend and backend) is deployed on Vercel.
    *   **Continuous Deployment (CI/CD):** Vercel is linked to this GitHub repository. Any push to the `main` branch automatically triggers a new deployment, ensuring the live application is always running the latest version of the code.

---

## 🔧 Local Development

To run this project on your local machine:

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/ssspplash6/robocontest-badge-generator.git
    cd robocontest-badge-generator
    ```

2.  **Install dependencies:**
    Make sure you have Python 3.9+ installed.
    ```bash
    pip install -r requirements.txt
    ```

3.  **Install the Vercel CLI:**
    ```bash
    npm install -g vercel
    ```

4.  **Run the development server:**
    This command simulates the Vercel environment perfectly.
    ```bash
    vercel dev
    ```
    The application will be available at `http://localhost:3000`.

---

## ⚖️ License

This project is open-source and available under the [MIT License](LICENSE).
