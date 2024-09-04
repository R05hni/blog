# Django Blog Website

A simple and customizable blog website built with Django, allowing users to create, edit, and delete posts, comment on posts, and interact with other users' content. The project also includes user authentication, TinyMCE editor integration, and data export functionality.

## Features

- User authentication (Signup, Login, Logout)
- Create, read, update, and delete (CRUD) posts
- Commenting system with AJAX for dynamic interactions
- TinyMCE integration for rich-text editing in posts
- Export posts and comments to an Excel file
- Responsive design with custom CSS
- Image upload and display in posts
- Comment and post interaction counts
- Data export with image resizing in Excel



## Installation

### Prerequisites

- Python 3.x
- Django 3.x or 4.x
- Virtualenv (optional, but recommended)

### Setup

1. **Clone the repository:**

   

2. **Create a virtual environment:**

    ```bash
    python -m venv venv
    ```

3. **Activate the virtual environment:**

    - On Windows:

      ```bash
      venv\Scripts\activate
      ```

    - On macOS/Linux:

      ```bash
      source venv/bin/activate
      ```

4. **Install the dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

5. **Apply migrations:**

    ```bash
    python manage.py migrate
    ```

6. **Create a superuser:**

    ```bash
    python manage.py createsuperuser
    ```

7. **Run the development server:**

    ```bash
    python manage.py runserver
    ```

8. **Access the website:**

    Open your browser and go to `http://127.0.0.1:8000/`.

## Usage

- **Creating Posts:** Users can create posts with a title, content, and optional image using a rich text editor powered by TinyMCE.
- **Commenting:** Users can comment on posts. AJAX is used to dynamically add, edit, and delete comments without reloading the page.
- **Data Export:** Users can export posts and comments to an Excel file with images included.

## Project Structure

```
your-repo-name/
│
├── blog/                   # Main app
│   ├── migrations/         # Database migrations
│   ├── static/             # Static files (CSS, JS, images)
│   ├── templates/          # HTML templates
│   ├── views.py            # View functions and classes
│   ├── models.py           # Database models
│   ├── urls.py             # URL routing
│   ├── forms.py            # Forms for posts and comments
│   └── admin.py            # Admin panel customizations
│
├── static/                 # Global static files
│
├── templates/              # Global templates (base.html, etc.)
│
├── manage.py               # Django management script
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation
├── .gitignore              # Git ignore file
└── db.sqlite3              # SQLite database (for development)
```

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes and commit (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a new Pull Request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For any questions, suggestions, or issues, feel free to contact me:


