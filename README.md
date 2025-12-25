# Community-Driven Neighborhood Cleanliness Platform (CleanIt)

CleanIt is a community-focused web application designed to help citizens organize and participate in neighborhood clean-up initiatives. The platform provides a structured environment where users can highlight locations that need cleaning, share motivation stories, organize clean-up drives, and coordinate volunteers.

---

## Project Structure

* **Project Name:** cleanit
* **App Name:** saaf
* **Repository:** community_cleanliness_project_saaf

All core functionality is implemented inside the `saaf` Django app.

---

## Key Features

* **Clean-Up Invitations**
  Users can create invitations for locations that require cleaning. Each invitation includes a motivation story and an optional image.

* **Motivation Stories**
  Personal descriptions explaining why a location matters, encouraging community participation.

* **Clean-Up Drives (Events)**
  Organized clean-up drives linked to invitations, displaying date, time, and location details.

* **Volunteer Suggestions**
  Users can add suggestions or coordination messages under invitations.

* **Participation Tracking**
  Volunteers can join clean-up drives, with the system ensuring unique participation per user.

* **Location-Based Event Discovery**
  Nearby clean-up drives can be discovered using the Browser Geolocation API.

* **AI-Based Motivation Story Enhancer (Optional)**
  Integrates Google Gemini API to enhance user-written motivation stories. The application works fully without this feature enabled.

---

## Tech Stack

* **Backend:** Django (Python)
* **Frontend:** HTML, CSS, JavaScript, Tailwind CSS
* **Database:** SQLite
* **Authentication:** Django built-in authentication system
* **AI Integration:** Google Gemini API (optional)
* **Version Control:** Git & GitHub

---

## Live Deployment

The application is deployed for demonstration purposes at:

[https://sky7.pythonanywhere.com](https://sky7.pythonanywhere.com)

* Hosted on PythonAnywhere
* Intended for academic and demo use, not production-scale deployment

---

## Environment Variables

Create a `.env` file in the project root and configure the following:

```
SECRET_KEY=your_django_secret_key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
GEMINI_API_KEY=your_gemini_api_key
```

`GEMINI_API_KEY` is optional. The application runs normally without AI features enabled.

---

## Setup & Run Instructions

1. Clone the repository

```
git clone https://github.com/s-k-y-7/community_cleanliness_project_saaf.git
cd community_cleanliness_project_saaf
```

2. Create and activate a virtual environment

```
python -m venv venv
venv\Scripts\activate
```

3. Install dependencies

```
pip install -r requirements.txt
```

4. Apply database migrations

```
python manage.py migrate
```

5. Run the development server

```
python manage.py runserver
```

6. Open in browser

```
http://127.0.0.1:8000/
```

---

## Media Files

Uploaded images are stored using Django’s `MEDIA_ROOT`.
The `media/` directory is not included in the repository and must be created locally for image uploads to work.

---

## User Access

* Open registration is enabled
* Any user can sign up and use the platform
* Admin users can moderate content via Django admin panel

---

## Academic Context

* Intended for learning, evaluation, and demonstration
* Not a production-ready system

---

## Future Scope

* Real-time notifications and updates
* Map-based location visualization
* Mobile application support
* Gamification for volunteer engagement
* Advanced AI-based recommendations
* Before-and-after photo comparison

---

## License

This project is intended for academic and educational use.
