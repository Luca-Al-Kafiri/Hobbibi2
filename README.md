# Hobbibi

Hobbibi is a mobile-responsive website that helps users to find people in their city who have the same hobbies and makes it easier to communicate with them.
The project utilize Django on the back-end and JavaScript on the front-end.

##### Files:
- admin.py: Contains registered models.
- models.py: Contains the four models used in the project.
- urls.py - All URLs.
- views.py: Contains all application views.

##### Templates directory:
- layout.html: Contains the general structure.
- index.html: Welcome page.
- register.html: Register page.
- login.html: Login page.
- profile.html: Contains user details and messages between users / adding hobbies.
- search.html: Shows users who have the same hobbies with an option to filter the results.

##### Static directory:
- hobbi.js: JS code that run in profile.html for adding and deleting hobbies.
- js.js: JS code that run in search.html for filtering the results in the search page by hobby.
- message.js: JS code that run in profile.html for sending and deleting messages.
- style.css: Handles the style of the website.
