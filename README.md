<h2>Hello, User! Flask App</h2>
<hr>
On the main page of the project there is a form for entering a user`s email and a button "Привітатись".
When you press the button, if the e-mail met for the first time, the message "Привіт, <code>email</code>" is displayed.
If such email has already been met, the message "Вже бачилися, <code>email</code>" is displayed. Also, on the main page 
there is a link, by clicking on which you can get a list of users
who have already been greeted.

For memory optimization, with the expectation that all Internet users will come to greet us, the email is stored in the database for an hour.
At the first appearance, the email gets an expiration time of 1 hour. After this time expires, the email is removed from the database by thread, 
which runs in parallel to the main application.

The project is wrapped in Docker and was deployed to Heroku using GitHub Actions.

<h2>Website hosted on heroku</h2>
<hr>

https://hello-user-email.herokuapp.com/

https://hello-user-email.herokuapp.com/all_emails to get a list of users who have already been greeted
