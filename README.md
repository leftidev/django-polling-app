This app is a [basic poll application](https://docs.djangoproject.com/en/5.1/intro/tutorial01/) and uses Python and Django with SQlite3.

The project's goal is to construct software with security flaws, point out the flaws in the project, and provide the steps to fix them.

***NOTE: The project uses a local SQlite database, and SHOULD NOT be used in production environment.***

How to run the app: 
- Run command: python manage.py runserver
- Open browser: http://127.0.0.1/polls/

# Security flaws and steps to fix them

### Security flaw 1: Broken Access Control
[link to flaw 1](https://github.com/leftidev/django-polling-app/blob/65fbb9a125008a55220ab8da0302dbf14d7d859f/pollingapp/views.py#L11)

First flaw is OWASP A01:2021-Broken Access Control. The OWASP site for this flaw describes that "access control enforces policy such that users cannot act outside of their intended permissions". My project has access control vulnerability called an elevation of privileges, which means acting as a user without being logged in or acting as an admin when logged in as a user.

The polling app uses Django's basic authentication backend with Django users database. I have created a superuser admin and user bob. The app has a broken access control flaw in source file "views.py" in function def index(request). The app should only allow logged in users to view the page http://127.0.0.1:8000/polls/. The flaw allows acting as a user without being logged in. 

The fix for the broken access control flaw is to add authentication via Django's authentication system, where authenticate() is used to verify a set of credentials. It takes credentials as keyword arguments, username and password, checks them against each authentication backend, and returns a User object if the credentials are valid for a backend. In the project, the valid username is "bob" and valid password is "squarepants". With "user = authenticate()" and the following if-else commented out, there is no authentication at all when viewing the page http://127.0.0.1:8000/polls/. For code fix in file "pollingapp/views.py": Uncomment lines 11, 12, 16 and 17.


### Security flaw 2: Security Misconfiguration
[link#1 to flaw 2](https://github.com/leftidev/django-polling-app/blob/9e81e9e563528180f56d428a91497a51e4ef1d17/leftisite/urls.py#L6)

[link#2 to flaw 2](https://github.com/leftidev/django-polling-app/blob/9e81e9e563528180f56d428a91497a51e4ef1d17/leftisite/settings.py#L35)

Second flaw is OWASP A05:2021-Security Misconfiguration. The OWASP site for this flaw lists that application might be vulnerable if the application has e.g. unnecessary features that are enabled or installed (e.g., unnecessary ports, services, pages, accounts, or privileges) or default accounts and their passwords are still enabled and unchanged.

My project uses the default Django Admin for automating creation of admin interface for database models, including users. Additionally, the superuser admin has a very vulnerable username/password combination of "admin/admin". This admin console with default admin account can be easily used to create/delete new users or poll questions by an attacker. The admin interface can be viewed from page http://127.0.0.1:8000/admin/.

There are two fixes for the security misconfiguration that can be applied. First approach is by disabling the admin console and using something else than the built-in admin interface. The second approach involves changing the password of the default superuser admin or deleting it and creating a new superuser entirely. You can disable the admin interface by commenting out line 35 in file "leftisite/settings.py" ('django.contrib.admin',) and line 6 in file "leftisite/urls.py" (path('admin/', admin.site.urls),). Creating a new superuser can be done by running command "python manage.py createsuperuser" and entering username, email address and password. Changing the password for an existing superuser can be done by running the command "python manage.py changepassword <superusername>" and entering the new password. Deleting a superuser can be done in the Python shell by running the command "python manage.py shell" and entering the next lines of code:
    from django.contrib.auth.models import User
    User.objects.get(username="admin", is_superuser=True).delete()


### Security flaw 3: Identification and Authentication Failures
[link#1 to flaw 3](https://github.com/leftidev/django-polling-app/blob/413712c0ffc8304d8af71134d6706ebca8f67cfc/leftisite/settings.py#L127)

[link#2 to flaw 3](https://github.com/leftidev/django-polling-app/blob/413712c0ffc8304d8af71134d6706ebca8f67cfc/leftisite/settings.py#L130)

Third flaw is OWASP A07:2021-Identification and Authentication Failures. The OWASP site for this flaw describes that "confirmation of the user's identity, authentication, and session management is critical to protect against authentication-related attacks". There may be authentication weaknesses if the application e.g. does not correctly invalidate Session IDs. User sessions or authentication tokens (mainly single sign-on (SSO) tokens) aren't properly invalidated during logout or a period of inactivity. This means that if e.g. a user has used a public computer for an application and simply closes the browser without logging out, an attacker could use the same browser an hour later and the user is still authenticated. My project's admin interface (http://127.0.0.1:8000/admin/) does not correctly invalidate a session cookie after a certain time has passed or the browser has been closed.

The fix for identification and authentication failures in the polling app can be applied by implementing session timeouts in Django. Django offers built-in setting to control session expiration in "settings.py". SESSION_COOKIE_AGE controls how long the session cookie will last in seconds after the last user interaction and SESSION_EXPIRE_AT_BROWSER_CLOSE expires the session when user closes the browser. For code fix in file "leftisite/settings.py": Uncomment lines 127 and 130.


### Security flaw 4: Security Logging and Monitoring failures
[link to flaw 4](https://github.com/leftidev/django-polling-app/blob/3e1ea6e34d2960a81fe934615021a2ed681f553c/pollingapp/apps.py#L8)

Fourth flaw is OWASP A09:2021-Security Logging and Monitoring Failures. The OWASP site for this flaw describes that "this category is to help detect, escalate, and respond to active breaches. Without logging and monitoring, breaches cannot be detected". Insufficient logging, detection, monitoring, and active response occurs any time e.g. auditable events, such as logins, failed logins, and high-value transactions, are not logged and logs are only stored locally. My project's admin console (http://127.0.0.1:8000/admin/) has no logging at all for users trying to log in.

The fix for security logging and monitoring failures in the polling app can be applied by creating logging functionality for successful and failed login-attempts when someone tries to log in to the admin console. Django has a built-in module signals. Using this, I created a signal handler "pollingapp/signals.py" to trigger a function whenever a user logs in or when a user fails a log in attempt. Then, the signal needs to be connected to the app when the app is ready; as in fully loaded and starts handling requests. For code fix in file "pollingapp/apps.py": Uncomment lines 8 and 9. Note that this fixes only the case of no logging at all, but the logging is only done to console. This fix does not address the fact that the logging is still insufficient, because the logs are not saved to a secure place (e.g. a cloud database).


### Security flaw 5: Cross Site Request Forgery (CSRF)
[link to flaw 5](https://github.com/leftidev/django-polling-app/blob/5ea057d3abb0e3732039094d80150babb4a8f133/leftisite/settings.py#L47)

Fifth flaw is Cross Site Request Forgery (CSRF). It is not on the OWASP site, because it is rare due to secure web frameworks which handle protection against it. CSRF attack happens when a malicious website contains a form button, link or JavaScript that intends to perform some action on your website. It uses the credentials of a logged-in user visiting the malicious site in their browser. Django has a built-in CSRF protection in Django project settings: (MIDDLEWARE: 'django.middleware.csrf.CsrfViewMiddleware'). When this is enabled the user can implement CSRF protection by using Django's CSRF template tag {% csrf_token %} in a HTML form.

The fix for CSRF vulnerability is by ensuring that GET requests are side effect free, and requests via 'unsafe' methods, such as POST, PUT, and DELETE are protected by the web frameworks built-in CSRF protection [1]. However, if not using a framework with CSRF protection, it has to be implemented manually. This is a complicated process that involves e.g. generating unique CSRF tokens for each user session, including the token as a hidden field in HTML or HTTP header and verifying the token on form submission [2]. In my project, the CsrfViewMiddlware is disabled. For code fix in file "leftisite/settings.py": Uncomment line 47.

References:

[1] https://docs.djangoproject.com/en/5.1/ref/csrf/

[2] https://portswigger.net/web-security/csrf/preventing