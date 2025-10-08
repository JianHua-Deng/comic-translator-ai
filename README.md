# ComicTranslate AI

This is an application that uses Optical Character Recognition (OCR) and other open sourced machine learning models to translate text on comic and manga pages.

---

## About The Project

This project allows users to upload multiple images of a comic page. The backend pipeline then processes the image, detects text bubbles, extracts the text using OCR, and translates it using advanced AI models. The translated text is then overlaid and re-rendered back to the image.

---

## Project Structure

This repository is a monorepo that contains both the frontend and backend services for the application.

-   `/backend`: Contains the server-side code, including the OCR and translation AI pipeline. For detailed instructions on setting up the environment and running the server, please see the `README.md` file inside this folder.

-   `/frontend`: Contains the client-side user interface code. For instructions on installing dependencies and launching the web application, please refer to the `README.md` file inside this folder.

---

## Getting Started

To get a local copy up and running, you will need to set up both the frontend and backend services.

1.  **Clone the repository:**
2.  **Set up the Backend:** Navigate to the `/backend` directory and follow the instructions in its `README.md` file.
3.  **Set up the Frontend:** Navigate to the `/frontend` directory and follow the instructions in its `README.md` file.
