# uzu-account-app

This is the official API documentation for the uzu-accounts-app Django Application.

uzu-accounts-app is a generic django application tailored to Single Page Applications that abstracts user authentication and verification from the rest of your project.

uzu-accounts-app will use the model set with `AUTH_USER_MODEL` in settings.py of your django project or the default user model of `django.contrib.auth`


## Installation

Download and install the package from PyPi:
````bash
pip install uzu-accounts-app
````

Add `AccountsApp.urls` to your project's URLConf
````Python
urlpatterns = [
	...
	path("accounts/", include("AccountsApp.controllers"))
]
````

Add the AccountsApp to your `INSTALLED_APPS`:
````Python
INSTALLED_APPS = [
	...
	"AccountsApp.apps.AccountsappConfig"
]
````

Setup the `ACCOUNTS_APP` settings variable in settings.py
````Python
ACCOUNTS_APP = {
	"base_url": "",			# Base url pattern for the AccountsApp urls
	"redirect_link": "", 	# Link redirected to after link verification 
	"code_length": 3, 		# specifies the length of the verification code
	"sign_in_after_verification": False		# Specify if to sign in after verification is successful
}
````

Then apply migrations

````Bash
python manage.py migrate
````
## API 
The app communicates with the client-side using basic api calls. 

API responses have the following basic format:
````typescript
{
	data: Object,  			 //  payload
	error: {summary: string, fields: {[key: string]: string[]}}            //  error string in case an error occurs (status == False)
}
````


### API List

NB: The illustrations below assume that the app's urls were mapped to the `accounts/` path.

#### 1. sign-in

````typescript
axios.post("/accounts/sign_in/", {
	...accountFields,
	keep_signed_in: true 		// keeps the user signed in (optional)
})
````


#### 2. sign-up

````typescript
axios.post("/accounts/sign_up/", {
	...accountFields,
	keep_signed_in: true 		// keeps the user signed in (optional)
})
````


#### 3. sign-out
````typescript
axios.get("/accounts/sign_out/")
````


#### 4. authenticate
````typescript
axios.post("/accounts/authenticate/", {
	password: ""
})
````


#### 5. reset-password
````typescript
axios.post("/accounts/reset_password/", {
	username: "",		// field value used for authentication as set by user_model.USERNAME_FIELD
	code: "",			// verification code. This comes from send-verification-code 
	new_password: "",
})
````


#### 6. change-password
````typescript
axios.post("/accounts/change_password/", {
	new_password: "",
	old_password: ""
})
````

#### 7. send-verification-code
````typescript
axios.post("/accounts/send_verification_code/", {
	username: "",		// optional username (will use request.user.username if a user is signed in when this field is not specified. Fails otherwise)
	mode: "",			// (send || resend) optional mode (will use 'resend' by default, if set to 'send', the verification code is updated before sending) 
})
````

#### 8. send-verification-link
````typescript
axios.post("/accounts/send_verification_link/", {
	username: "",		// optional username (will use request.user.username if a user is signed in when this field is not specified. Fails otherwise)
	mode: "",			// (send || resend) optional mode (will use 'resend' by default, if set to 'send', the verification code is updated before sending) 
})
````

#### 9. verify-code
````typescript
axios.post("/accounts/verify_code/", {
	username: "",		
	code: "",			
})
````