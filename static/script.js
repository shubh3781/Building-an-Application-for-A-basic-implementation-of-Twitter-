'use strict';


window.addEventListener('load', function () {

    document.getElementById('sign-out').onclick = function() {
        document.cookie.split(";").forEach(function(c) { document.cookie = c.replace(/^ +/, "").replace(/=.*/, "=;expires=" + new Date().toUTCString() + ";path=/"); });
        firebase.auth().signOut();

        window.location.href='/signin';
        window.location.reload;

    };

    var uiConfig = {
        signInSuccessUrl: '/',  // where in the application we will redirect to on a successful user login
        signInOptions: [
            firebase.auth.EmailAuthProvider.PROVIDER_ID
        ]
    };

    // javascript that will react to whenever the firebase authentication state changes
    firebase.auth().onAuthStateChanged(function(user) {
        // determine if a user is signed in or not
        if(user) {
            console.log(user['name'])
            console.log(`Signed in as ${user.displayName} (${user.email})`);
            console.log(user)
            user.getIdToken().then(function(token) {
                document.cookie = "token=" + token + ";path=/";
            });
        } else {
            var ui = new firebaseui.auth.AuthUI(firebase.auth());
            ui.start('#firebase-auth-container', uiConfig);
            console.log(user)
       }
    }, function(error) {
        // if something goes wrong then log the error to console and state the user could not be logged in
        console.log(error);
        alert('Unable to log in: ' + error);
    });
});
